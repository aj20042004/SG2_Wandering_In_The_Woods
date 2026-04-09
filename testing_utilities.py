
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

from typing import Iterable,Type,Any,TypedDict
from collections import deque
from types import ModuleType
from collections.abc import Iterator,Callable
import inspect
from sys import modules,_getframe
from dataclasses import dataclass







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





# (NOT IMPLEMENTED) apply_to uses proper module names not aliases 
def patch_module(scope:ModuleType|Callable,apply_to:str,patch:Callable)->Callable[[],None]:
	
	
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

	target_caller_name=scope.__name__
	def _context_switch(*args, **kwargs):
		if(target_caller_name==_getframe(1).f_code.co_name):
			return patch(*args,**kwargs)
		else:
			return original_func(*args,**kwargs)

	wrapped_patch:Callable=_context_switch if inspect.isfunction(scope) else patch





	setattr(dummy_module_class,apply_func_name,wrapped_patch)
	#replace imported module with our dummy class 
	setattr(scope_module,apply_module_name,dummy_module_class)
	

	def revert_patch():
			delattr(scope_module,apply_module_name)
			setattr(scope_module,apply_module_name,apply_module)



	

	return revert_patch
	










def simulate_input(scope,feed_tape:Iterator[str]|Iterable[str])->Callable[[],None]:
	_feed_tape=iter(feed_tape)
	def _patched_input(Prompt=None):
		return next(_feed_tape)
	return monkey_patch_func(scope,"input",_patched_input)


#provides some limited additional safety 
#TODO: add ability to limit scope to function
#TODO: add functionality to limit scope to classes
def monkey_patch_func(scope_to_patch:ModuleType|Callable,apply_to:str,patch_function:Callable)->Callable[[],None]:
	

	
	#check if we are shadowing an existing function
	try:
		old_function=getattr(scope_to_patch,apply_to)
		def revert_patch():
			delattr(scope_to_patch,apply_to)
			setattr(scope_to_patch,apply_to,old_function)
				
	except AttributeError:
		def revert_patch():
			delattr(scope_to_patch,apply_to)

	setattr(scope_to_patch,apply_to,patch_function)

	return revert_patch
