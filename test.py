# Authors: Alex Fahnestock 
# Date: 3/25/26
# Project: CS 4500 small group project 2 
# summary: automated tests for SG2_Program

import testing_utilities
import SG2_Program



def main():
	testing_utilities.InputAutofeed.enable_simulated_input(SG2_Program,["a","b"])
	SG2_Program.main()
	testing_utilities.InputAutofeed.disable_simulated_input()




if __name__=="__main__":
    main()