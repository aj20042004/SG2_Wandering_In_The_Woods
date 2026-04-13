# Authors: Alex Fahnestock 
# Date: 3/25/26
# Project: CS 4500 small group project 2 
# summary: automated tests for SG2_Program

import testing_utilities
from testing_utilities import TestResult,unit_test,box,SimulatedInput,Patch,TestModule
from testing_utilities import assertEqual,assertNotEqual,assertRaises
import SG2_Program

import matplotlib as mp

def over(*args):
	for arg in args:
		print(arg)

import matplotlib.pyplot as plot

import importlib.util
from types import ModuleType
from typing import Callable,List,Type,NoReturn,Generator,Optional,Any
import inspect



import pathlib 

from collections.abc import Buffer as ReadableBuffer

import logging
import sys




#======================= Patches ======================================
class dummy_file():
	def __enter__(self):
		return self
	
	def __exit__(self,exc_type, exc_value, traceback):
		pass

	def write(self,s: ReadableBuffer,/) -> int:
		
		self.output_buffer.val+=str(s) #type:ignore
		return 0
	
	def __init__(self,output_buffer:box[str]):
		""":param box[str] output_buffer: location to store the written data instead of writing to a file"""
		self.output_buffer=output_buffer


def dummy_open(*args,**kwargs): 
	return dummy_file()

def dummy_print(*args,**kwargs):
	return

def dummy_show():
	plot.close('all') #flush out unshown graphs
	return

#=======================================================================

#basic sim test
def test1():

	

	
	#plot.ion()

	revert_input_patch=testing_utilities.simulate_input(SG2_Program,["10","1000","50",""])
	revert_suppress_matplot_show_patch=testing_utilities.patch_module(SG2_Program.simulation_analysis_and_histogram,"plt.show",dummy_show)
	revert_nowrite_patch=testing_utilities.patch_module(SG2_Program.write_results,"Path.open",dummy_open)
	revert_suppress_print=testing_utilities.monkey_patch_func(SG2_Program.main,"print",dummy_print)
	try:
	
		SG2_Program.main()
		
	finally:
		revert_suppress_print()
		revert_suppress_matplot_show_patch()
		revert_nowrite_patch()
		revert_input_patch()
	input("PRESS ENTER TO EXIT")
	#plot.close("all") #in-case we are running in interactive




# test public interface
def test2():
	tape1=["10","1000","50",""]
	tape2=["100","1000","50",""]
	suppress_show =  Patch(SG2_Program.simulation_analysis_and_histogram,"plt.show",dummy_show)
	simulated_input = SimulatedInput(SG2_Program,tape1)
	suppress_main_print = Patch(SG2_Program.main,"print",dummy_print)
	redirect_write = Patch(SG2_Program.write_results,"Path.open",dummy_open)
	plot.ion()

	# Uses context managers for easy cleanup
	with simulated_input,suppress_main_print,redirect_write:
		SG2_Program.main()

	input("PRESS ENTER TO EXIT")
	plot.close("all") #in-case we are running in interactive





def gen_test_tape(N_buffer:box[str],T_buffer:box[str],R_buffer:box[str])->Generator[str,Any, NoReturn]:
		#generate range lower to upper and then holds at upper value for subsequent calls
		def	gen_range_hold(lower:int,upper:int):
			val=lower
			while True: 
				yield str((val:=val+1) if val+1<upper else val)
		
		N_gen=gen_range_hold(2,100)
		T_gen=gen_range_hold(2,1_000_000)
		R_gen=gen_range_hold(1,100_000)

		# interleave values 
		while True:
			N_buffer.val=N=next(N_gen) #ugly but compact. I miss my macros
			yield N
			T_buffer.val=T=next(T_gen)
			yield T
			R_buffer.val=R=next(R_gen)
			yield R
		

# we just want to use a class to organize our functions into a namespace
# and as an easy way to run multiple related tests
class unit_test_input_validation(TestModule):

	#get_user_inputs
	@unit_test(test_name="Exhaustive Valid Input")
	def ut_exhaustive_valid_input()->None:
		"""exhaustively test all valid inputs"""
		
		# boxes to store copies of generated inputs
		N_buffer:box=box[str]()
		T_buffer:box=box[str]()
		R_buffer:box=box[str]()

		test_tape =  gen_test_tape(N_buffer,T_buffer,R_buffer)
		simulated_input =  SimulatedInput(SG2_Program,test_tape)
		suppress_print =  Patch(SG2_Program,"print",dummy_print)

		with simulated_input,suppress_print:
			output =  SG2_Program.get_user_inputs()
			expected =  (int(N_buffer.val),int(T_buffer.val),int(R_buffer.val)) 

			assertEqual(output,expected)

			R_buffer.val=T_buffer.val=N_buffer.val=None # rest buffers 



	@unit_test(test_name="Different categories of invalid input")
	def ut_categories_invalid_input()->None:
		pass


	@unit_test(test_name="Numbers out of valid range")
	def ut_out_of_range_inputs()->None:
		pass
	



def main():
	
	# add what test modules you want to run here 
	test_modules=[unit_test_input_validation]
	
	testing_utilities.run_unit_tests(test_modules)
	
		


if __name__=="__main__":
    main()