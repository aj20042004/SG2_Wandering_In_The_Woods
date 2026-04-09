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



def test1():
	revert_input_patch=testing_utilities.simulate_input(SG2_Program,["a","b"])
	SG2_Program.main()
	revert_input_patch()

def test2():
	reel=[["a","b"],["b","c"],["c","d"]]
	for tape in reel:
		revert_input_patch=testing_utilities.simulate_input(SG2_Program,["a","b"])
		SG2_Program.main()
		revert_input_patch()


def test3():
	
	revert=testing_utilities.patch_module(SG2_Program.main,"plt.subplots")
	SG2_Program.main()
	revert()






class dummy_file():
	def __enter__(self):
		return self
	
	def __exit__(self,exc_type, exc_value, traceback):
		pass

	def write(self,s: ReadableBuffer,/) -> int:
		print(s)
		return 0


def dummy_open(*args,**kwargs): 
	return dummy_file()





def test4():
	""" Test patching instances via hijacking a factory method. Patches a file instances write method."""
	#possible interface? scope,instance constructor,instance_method_to_patch,patch
	
	revert_intercept=testing_utilities.patch_module(SG2_Program.write_results,"Path.open",dummy_open)
	
	try:
		SG2_Program.main()
	finally:                                                             
		revert_intercept()
		


#basic sim test
def test5():
	
	print(SG2_Program.run_simulations(50,1000,300))


def main():
	print("dummy")

	#testing_utilities.monkey_patch_func(SG2_Program.plt,"subplots",wrapper)
	#testing_utilities.monkey_patch_func(mp.axes.Axes,"hist",over)
	#testing_utilities.monkey_patch_func(SG2_Program.main,"ax",new_ax)

	#load(plot,plt)
	#print(plt.subplots)
	#setattr(SG2_Program.main,"plt",plt)
	




if __name__=="__main__":
    main()