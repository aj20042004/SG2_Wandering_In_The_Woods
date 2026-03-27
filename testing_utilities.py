# Authors: Alex Fahnestock 
# Date: 3/25/26
# Project: General utility 
# summary: self explanitory 

from typing import Iterable
from collections import deque
from types import ModuleType


# This is setup weird because we only ever want one.
class InputAutofeed():
	"""
	Testing utility that simulates user input whenever the built in input
	function is called.
	"""
	_feed_tape:deque[str]=deque()
	_loaded_module:ModuleType|None=None

	@staticmethod
	def _patched_input(Prompt=None):
		if InputAutofeed._feed_tape:
			return InputAutofeed._feed_tape.popleft()
		raise IndexError("Unexpectedly ran into end of feed tape.")

		
	@classmethod
	def enable_simulated_input(cls,module_to_patch:ModuleType,feed_tape:Iterable[str]):
		"""
		Enables simulated input to be used in place of user input
	
		:param module_to_patch: module we want to shadow the input function in.
		:param feed_tape: simulated input to feed when input is requested. 
		 Input is fed FILO (starts at index 0).
		:raises IndexError: whenever the module tries to call the input function 
		more times than feed_tape has simulated inputs
		"""
		cls._feed_tape=deque(feed_tape)
		setattr(module_to_patch,"input",cls._patched_input)
		
	
	@classmethod 
	def disable_simulated_input(cls):
		"""unnecisary but still nice to clean up"""
		if not cls._loaded_module:return
		delattr(cls._loaded_module,"input")
		cls._loaded_module=None


	def __init__(self):
		raise TypeError(f"{self.__class__.__name__} is not instantiable")
	
