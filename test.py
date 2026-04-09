# Authors: Alex Fahnestock 
# Date: 3/25/26
# Project: CS 4500 small group project 2 
# summary: automated tests for SG2_Program

import testing_utilities
import SG2_Program

import matplotlib as mp

def over(*args):
	for arg in args:
		print(arg)

import matplotlib.pyplot as plot

import importlib.util
from types import ModuleType
from typing import Callable,List,Type
import inspect



import pathlib 

from collections.abc import Buffer as ReadableBuffer




#def gen_write_patch()->callable[]:


#pp({ k:v for k,v in vars(SG2_Program).items() if (len(str(v))<80) })


#basic sim test
def test1():

	class dummy_file():
		def __enter__(self):
			return self
		
		def __exit__(self,exc_type, exc_value, traceback):
			pass

		def write(self,s: ReadableBuffer,/) -> int:
			print(s)
			return 0


	def dummy_open(*args,**kwargs): 
		"""
		patch for the file factory function Path.open. Allows us to swap out 
		the file object with our own dummy version.
		"""
		return dummy_file()
	
	def dummy_show():
		return
	revert_input_patch=testing_utilities.simulate_input(SG2_Program,["10","1000","50",""])
	revert_noshow_patch=testing_utilities.patch_module(SG2_Program.simulation_analysis_and_histogram,"plt.show",dummy_show)
	revert_nowrite_patch=testing_utilities.patch_module(SG2_Program.write_results,"Path.open",dummy_open)
	
	try:
		SG2_Program.main()
	finally:
		revert_noshow_patch()
		revert_nowrite_patch()
		revert_input_patch()
	


def main():
	test1()



if __name__=="__main__":
    main()