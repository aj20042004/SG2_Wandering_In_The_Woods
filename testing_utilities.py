
"""
====================================================================
	ABANDON HOPE ALL YE WHO ENTER HERE
=====================================================================
	this file is currently filled with all sorts of 
	garbage due to me having to downgrade patch_module 
	to a previous iteration. It should serve our purposes 
	for now 
======================================================================
"""

# Authors: Alex Fahnestock 
# Date: 3/25/26
# Project: General utility 
# summary: self explanitory 

from typing import Iterable,Type,Any,TypedDict,Optional,Literal
from collections import deque
from types import ModuleType
from collections.abc import Iterator,Callable
import inspect
from sys import modules,_getframe
from dataclasses import dataclass
import builtins





def copy_module_to_class(source:ModuleType,dest:Type):

	for name, obj in inspect.getmembers(source):

		#check that object originates from source 
		if inspect.getmodule(obj)==inspect.getmodule(source ):
			setattr(dest, name, obj)





@dataclass
class PatchEntry():
	id:int
	apply_to:str
	label:str
	restore_callback:Callable[[],None]
	original_func:Callable



#========== PUBLIC INTERFACE =====================================================

class Patch():
	

	

	def __init__(self,scope: ModuleType|Callable,apply_to:str,patch: Callable)->None:
		self._scope=scope
		self._apply_to=apply_to
		self._patch_func=patch
		self._callback:Optional[Callable[[],None]]=None

	def __enter__(self)->None:
		self._callback=patch_module(self._scope,self._apply_to,self._patch_func)
		return None
	
	def __exit__(self, exc_type, exc, tb)-> Literal[False]:
		if self._callback:self._callback()
		return False



class SimulatedInput():
	

	def __init__(self,scope: ModuleType|Callable,feed_tape:Iterator[str]|Iterable[str]):
		self._scope=scope
		self._feed_tape=feed_tape
		self._callback:Optional[Callable[[],None]]=None

	def __enter__(self)->None:
		self._callback=_simulate_input(self._scope,self._feed_tape)
		return None
	
	def __exit__(self, exc_type, exc, tb)-> Literal[False]:
		if self._callback:self._callback()
		return False




def simulate_input(scope,feed_tape:Iterator[str]|Iterable[str]):
	print("\033[33m" + "Warning: this function is depreciated. use SimulatedInput context manager instead" + "\033[0m")
	return _simulate_input(scope,feed_tape)



#========================================================================

# new private internal version 
def _simulate_input(scope,feed_tape:Iterator[str]|Iterable[str])->Callable[[],None]:
	_feed_tape=iter(feed_tape)
	def _patched_input(Prompt=None):
		return next(_feed_tape)
	return monkey_patch_func(scope,"input",_patched_input)





def storage():
	toplevel_name=original_func.__name__
	is_builtin=not hasattr(scope,toplevel_name) and hasattr(builtins,toplevel_name)


def wrap_patch(scope:ModuleType|Callable,patch: Callable,original_func:Callable)->Callable:

	#check to ensure that original_func is a function


	if not inspect.isfunction(scope) : return patch

	caller_name=scope.__name__
	def _context_switch(*args, **kwargs):
		if(_getframe(1).f_code.co_name ==caller_name):
			return patch(*args,**kwargs)
		else:
			return original_func(*args,**kwargs)
		
	return _context_switch


def patch_module(scope:ModuleType|Callable,apply_to:str,patch:Callable)->Callable[[],None]:
	
	
	#divert to monkey patch when patching a function without any attribute lookup
	if len(apply_to.split("."))<=1:
		return monkey_patch_func(scope,apply_to,patch)


	#wallrus operator allows for assignment without getting in way of condition
	if not(scope_module := inspect.getmodule(scope)):
		raise TypeError("Scope must be a module or function")
	

	#from this point on we are assuming apply_to is module.function



	try:
		apply_module_name,apply_func_name=apply_to.rsplit('.',1)
	except ValueError:
		raise ValueError("apply_to must contain moudle part")
	

	apply_module:ModuleType=getattr(scope_module,apply_module_name)
	original_func:Callable=getattr(apply_module,apply_func_name)


	dummy_module_class:type
	if inspect.isclass(apply_module):
		dummy_module_class=type(f"_{apply_module_name}_dummy",(apply_module,),{})

	else:
		#if its not already loaded load dummy_module_class with real module attributes here
		dummy_module_class=type(f"_{apply_module_name}_dummy",(),{})
		copy_module_to_class(apply_module,dummy_module_class)



	#if we want to limit the scope of our patch to a function we need to wrap 
	#the patch function in a wrapper that inspects the call stack and 
	#dispatches to the correct function for that context


	wrapped_patch:Callable=wrap_patch(scope,patch,original_func)







	setattr(dummy_module_class,apply_func_name,wrapped_patch)
	#replace imported module with our dummy class 
	setattr(scope_module,apply_module_name,dummy_module_class)
	

	def revert_patch():
			delattr(scope_module,apply_module_name)
			setattr(scope_module,apply_module_name,apply_module)



	

	return revert_patch
	







#provides some limited additional safety 
def monkey_patch_func(scope:ModuleType|Callable,apply_to:str,patch_function:Callable)->Callable[[],None]:
	patch=patch_function


	if not(scope_module := inspect.getmodule(scope)):
		raise TypeError("Scope must be a module or function")

	
	#check if we are shadowing an existing function
	try:
		old_function=getattr(scope_module,apply_to)
		patch=wrap_patch(scope_module,patch_function,old_function)
		def revert_patch():
			delattr(scope_module,apply_to)
			setattr(scope_module,apply_to,old_function)
			

	except AttributeError:
		def revert_patch():
			delattr(scope_module,apply_to)



	setattr(scope_module,apply_to,patch)

	return revert_patch
