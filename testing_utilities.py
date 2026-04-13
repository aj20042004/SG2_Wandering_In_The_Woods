
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
from types import ModuleType,TracebackType
from collections.abc import Iterator,Callable
import inspect
from sys import modules,_getframe
from dataclasses import dataclass, field,InitVar
import builtins
import code
import traceback
#TODO: (Personal) add color printing to pv pdb alias
#pp({ k:v for k,v in vars(SG2_Program).items() if (len(str(v))<80) })


#pp({ k:v if (len(str(v))<80) else "..." for k,v in a.items() })
#! from pprint import pformat;from re import sub;
#print(sub(r"[\']", "", pformat(  { k:v if (len(str(v))<80) else "..." for k,v in a.items() } )))






def _copy_module_to_class(source:ModuleType,dest:Type):

	for name, obj in inspect.getmembers(source):

		#check that object originates from source 
		if inspect.getmodule(obj)==inspect.getmodule(source ):
			setattr(dest, name, obj)



#============== UTILITY ===========================
class box[T]():
	"""generic storage location. None corresponds to a uninitialized state"""

	def __init__(self,init_val:T|None=None):
		self._val:T|None=None
		
	@property
	def val(self)->T:
		if not self._val: raise AttributeError("var is marked as uninitialized (None)")
		return self._val
	
	@val.setter
	def val(self,value:T|None)->None:
		self._val=value
		

	
	


#=========================== PUBLIC INTERFACE ================================
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

#========================================= UNIT TESTING =========================================================
@dataclass 
class TestResult():
	"""
	Result of a unit,system, or integration test
	"""
	test_name:str
	func:InitVar[Callable] 

	func_name:str=field(init=False)
	passed:bool=field(init=False)
	

	e:Exception|None=None
	tb:TracebackType|None= field(init=False)
	st:str|None=field(init=False)
	

	def __post_init__(self,func:Callable):
		self.func_name=func.__name__
		self.passed = self.e is None 
		self.tb= self.e.__traceback__ if self.e is not None else None
		self.st= traceback.format_exc() if self.e is not None else None

	def __str__(self):
		result= '\033[1;32mPASSED' if self.passed else '\033[1;91mFAILED'
		return f"\033[1m{self.test_name} \033[0m{self.func_name}: \033[1m{result}\033[0m"



class TestModule():



	# prevent instance creation. This class is just a container
	def __new__(cls, *args, **kwargs)->list[TestResult]: #type:ignore
		test_funcs=[value for name, value in vars(cls).items() if hasattr(value,"_unit_test")]
		object.__new__(cls)
		results:list[TestResult]=[]
		for test in test_funcs:
			try:
				test()
				results.append(TestResult(test._unit_test,test))
			except UnitTestAssertionError as e:
				results.append(TestResult(test._unit_test,test,e))
		return results







#we need a decorator anyways for a staticmethod so we may as well mark them
def unit_test(test_name:str)->Callable:
	def _inner(func:Callable[[],None])->staticmethod:
		
		#TODO: implement more sophisticated checks like if is in a TestModule specificly 
		if not "." in func.__qualname__:
			raise SyntaxError("unit_test decorator used outside of class")

		ret=staticmethod(func)
		setattr(ret,"_unit_test",test_name) #set marker
		return ret
	return _inner


def run_unit_tests(tests:list[TestModule]):
	
	results:list[TestResult]=[]
	for test in tests:
		results += test()#type:ignore

	errors= [r for r in results if r.passed==False]

	cat="================================================================\n"
	for r in results: cat+=f"{r}\n"
	cat+="---------------------------------------------------------------\n"
	cat+=f"{len(errors)} errors: inspect errors (or alias e) var for more details\n"
	cat+="use pm( i ) to start a debugging session for error e[i] \n"
	cat+="run function \033[1mhelp()\033[0m] for more aliases\n"
	cat+="===============================================================\n"
	
	print(cat)
	if errors:
		#setup convience aliases in enviorment 
		from pdb import post_mortem 
		from pprint import pprint as pp
		p=print
		e=errors
		def pm(i):post_mortem(e[i].tb)
		def st():
			for x in e:print(x.st,"-"*80)
		
		def help():
			print('Aliases:' 
				'\n\te[i] = errors[i]'
				'\n\tp() = print()'
				'\n\tpm(i) = pdb.post_mortem(e[i].tb) (debug error i)'
				'\n\tpp() = pprint.pprint() (pretty print)'
				'\n\tst() = print all stack traces in e')

		#launch interactive console so we can start debugging 
		code.interact(banner="",local=locals())





#========================= ASSERTATIONS ==============================


class UnitTestAssertionError(Exception):
    """Exception used when a unit test fails or something IDK"""
    pass


def assertEqual(a,b):
	if a != b:
		try:
			raise 
		except:
			e= UnitTestAssertionError(f"assertion {a} == {b} is False")
			raise e from None
		finally:
			 e.__traceback__ = e.__traceback__.tb_next
		

def assertNotEqual(a,b):
	if a==b:
		
		try:
			raise 
		except:
			e=UnitTestAssertionError(f"assertion {a} != {b} is False") 
			raise e from None
		finally:
			 e.__traceback__ = e.__traceback__.tb_next
			

class assertRaises():
	"""Raise a UnitTestAssertionException if we dont raise an exception. Use as a context manager"""

	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc, tb):
		if exc is None:
			try:
				raise 
			except:
				e= UnitTestAssertionError(f"assertion raises {self.exc_types}is False") 
				raise e from None
			finally:
				e.__traceback__ = tb
		elif self.exc_types and exc_type in self.exc_types:
			return True
		elif not self.exc_types and exc is not None:
			return True
		
	def __init__(self,filter_exceptions:list[Type[Exception]]|None=None):
		""":param filter_exception: filter down from all exceptions to just this specific type of exception"""
		self.exc_types=filter_exceptions



class assertNotRaises():
	"""Raise a UnitTestAssertionException if we raise an exception. Use as a context manager"""

	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc, tb):
		if exc is None:
			return True
		
		elif self.exc_types and exc_type in self.exc_types:
				try:
					raise 
				except:
					e= UnitTestAssertionError(f"assertion raises {self.exc_types}is False") 
					raise e from None
				finally:
					e.__traceback__ = tb
		elif not self.exc_types and exc is not None:
				try:
					raise 
				except:
					e= UnitTestAssertionError(f"assertion raises {self.exc_types}is False") 
					raise e from None
				finally:
					e.__traceback__ = tb
				
		
	def __init__(self,filter_exceptions:list[Type[Exception]]|None=None):
		""":param filter_exception: filter down from all exceptions to just this specific type of exception"""
		self.exc_types=filter_exceptions

#========================================================================





# new private internal version 
def _simulate_input(scope,feed_tape:Iterator[str]|Iterable[str])->Callable[[],None]:
	
	_feed_tape=iter(feed_tape)
	def _patched_input(Prompt=None):
		return next(_feed_tape)
	return monkey_patch_func(scope,"input",_patched_input)





#def storage():
#	toplevel_name=original_func.__name__
#	is_builtin=not hasattr(scope,toplevel_name) and hasattr(builtins,toplevel_name)


def wrap_patch(scope:ModuleType|Callable,patch: Callable,original_func:Callable)->Callable:
	"""
	wraps a patch in a context switch that inspects the calling function and 
	redirects execution to our patch if it's the correct scope
	"""

	#check to ensure that original_func is a function
	if not inspect.isfunction(scope) : return patch

	FV_caller_name=scope.__name__	# free variable
	def _context_switch(*args, **kwargs):
		is_in_scope=_getframe(1).f_code.co_name ==FV_caller_name
		return patch(*args,**kwargs) if(is_in_scope) else original_func(*args,**kwargs)
		
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
		_copy_module_to_class(apply_module,dummy_module_class)


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
