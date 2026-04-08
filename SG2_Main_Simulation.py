# ****************************************************************************************************************************************************************
# Developed using Python 3.10 and tested in Thonny. 
# 
# Authors: 
# Alex Fahnestock, Jackie Herbstreit, Tressa Millering, May Salahaldin, AJ Soma Ravichandran
#
# Course: CMP SCI 4500
# Important Dates:
#    1. Repository Created: 03/11/2026
#    2. Rough Design Drafted: 03/15/2026
#    3. Basic Simulation Implemented: 03/24/2026
#    4. Final Version Submitted: [ADD DATE]
#
# Program Description:
# This program simulates two strangers moving randomly on an N x N grid to determine
# if and when they meet. They start at opposite corners and move each time step (T).
# The simulation runs R times to collect statistical data.
#
# The program:
#   - Takes validated inputs for N (grid size), T (time limit), and R (runs)
#   - Runs R simulations of random movement
#   - Records ending time, meeting occurrence, and meeting locations
#   - Displays max, min, and average times, a histogram, and a heat map
#   - Saves results to a timestamped output file
#
# Simulation Logic:
#   - Each step, both individuals move randomly (up, down, left, right, or stay if blocked)
#   - If both land on the same cell, they meet and the simulation ends
#   - Otherwise, the simulation continues until time reaches T
#
# Data Structures:
#   - times_list: Stores the number of steps taken for each simulation.
#   - meet_count: Tracks how many simulations resulted in a meeting.
#   - no_meet_count: Tracks how many simulations ended without meeting.
#   - heat_map: 2D array (N x N) storing counts of meeting locations.
#   - histogram_data: Stores frequency distribution of ending times.ion
#  
# External Resources:
#   1. numpy.random.randint - Used to determine the direction of a given movement without 
#                              floating point comparisons (https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html)
#           
# Python Packages Required - (must be installed with Thonny IDE, "Tools -> Manage Packages")
#    - NumPy
#    - Matplotlib
#
# ****************************************************************************************************************************************************************

# Import necessary libraries
from datetime import datetime
from pathlib import Path
from typing import Any,Literal,cast

import numpy as np
import matplotlib.pyplot as plt
import random 

# Define type aliases for readability
type Coord=tuple[int,int]  # type alias for readability
type MovementVector=tuple[Literal[-1,0,1],Literal[-1,0,1]] 
type Box[T] = list[T]
type NumpyArray2D[T:np.generic]=np.ndarray[tuple[int, int], np.dtype[T]]

# Define a mapping of random integers to movement vectors (up, down, left, right)
DIRECTION_TABLE:dict[Literal[0,1,2,3],MovementVector]={0:(0,1) ,1:(0,-1),2:(-1,0),3:(1,0)}


# ****************************************************************************************************************************************************************
# Prints an array on a single line (for cleaner output during testing)
# Instead of printing each element on a new line (default NumPy behavior),
# this function prints all elements in one row.
#
# Parameters:
#   array -> the array to print
#   label -> optional label printed before the array
def print_array(array, label=""):
	print(label + (":" if (label != "") else ""))
	for _ in range(0, len(array)):
		print(array[_], end=" ")
	print("\n")



# ****************************************************************************************************************************************************************
# TEST BENCH (REMOVE FOR FINAL SUBMISSION)
#
# Verifies basic correctness of simulation outputs by:
#   - Checking consistency between meeting_locations, simulation_lengths, and heatmap
#   - Comparing random positions in meeting_locations with heatmap counts
#
# Parameters:
#   N ----------------> grid size
#   meeting_locations -> list of meeting coordinates
#   simulation_lengths -> list of simulation durations
#   heatmap ----------> 2D array of meeting counts
def test_bench(N, meeting_locations, simulation_lengths, heatmap):
	buffer = ""
	print("Running tests...\n")

	if (len(meeting_locations) != len(simulation_lengths) and len(meeting_locations) != np.sum(heatmap)):
		buffer += ("VALUE COUNT-- FAILED: ", len(meeting_locations), len(simulation_lengths), np.sum(heatmap))

	for _ in range(0, len(meeting_locations)//2):
		test = (np.random.randint(0, N), np.random.randint(0, N))
		count = 0
		for loc in meeting_locations:
			if (loc[0] == test[0] and loc[1] == test[1]):
				count += 1
		if (count != (heatmap[test[0]][test[1]])):
			buffer += ("HEATMAP VS LOC COUNT-- FAILED AT: ", test, count, (heatmap[test[0]][test[1]]))
		loading_screen(_, -1+len(meeting_locations)//2)

	if (buffer == ""):
		print("\nAll tests passed!")
	else:
		print(buffer)



# ****************************************************************************************************************************************************************
# Displays a progress bar while simulations are running.
# Updates the same console line to show completion percentage.
#
# Parameters:
#   sim -> current simulation number
#   R   -> total number of simulations
def loading_screen(sim, R):
	bar_length = 30
	progress = sim / R
	filled = int(progress * bar_length)
	empty = bar_length - filled

	bar = "█" * filled + "░" * empty
	percent = progress * 100

	print(f"\r{bar}  ---  {percent:.3f}%", end="")


# ****************************************************************************************************************************************************************
# Runs R simulations and tracks results.
#
# Returns:
#   meeting_locations -> list of meeting coordinates
#   simulation_lengths -> list of ticks until meeting
#   heatmap ----------> 2D array counting meeting locations
#
# Parameters:
#   N -> grid size
#   T -> max ticks per simulation
#   R -> number of simulations

def run_simulations(N:int, T:int, R:int)->tuple[list[Coord],list[int],NumpyArray2D[np.integer]]:
	"""
	Runs R simulations & displays a loading screen to show progress

	:param N: grid size
	:param T: number of ticks to run before we timeout
	:param R: simulation count

	:return: 
	"""

	print("\nRunning simulations...\n")

    # Heatmap stores number of meetings at each grid position
	heatmap = np.zeros((N, N), dtype= np.uint32) 
	
	simulation_lengths:list[int] = []
	meeting_locations:list[Coord] = []
	for sim in range(0, R):
		loading_screen(sim + 1, R)  # +1 ensures it reaches 100%
		ticks, loc = single_simulation(N, T)

		if ticks is None or loc is None:
			continue

		simulation_lengths.append(ticks)
		meeting_locations.append(loc)
		heatmap[loc[0]][loc[1]] += 1

	print("\nSimulations complete!\n")

	return meeting_locations,simulation_lengths, heatmap


# ****************************************************************************************************************************************************************
# Generates a random movement direction.
#
# Returns:
#   A tuple representing movement
def get_direction()-> MovementVector:
	"""
	Helper function that generates a random direction in the form of grid coordinates

	:return: a tuple representing a 2D movement vector.
	"""
	return DIRECTION_TABLE[random.choice([0,1,2,3])]



# ****************************************************************************************************************************************************************
# Updates position if move stays within grid boundaries.
#
# Parameters:
#   position  -> current 
#   direction -> movement vector
#   N --------> grid size
#
# Returns:
#   New position if valid, otherwise original position   
def update_position(position, direction, N):
	if (0 <= position[0] + direction[0] <= N-1) and (0 <= position[1] + direction[1] <= N-1):
		return (position[0] + direction[0], position[1] + direction[1])
	else:
		return position


# ****************************************************************************************************************************************************************
# Runs a single simulation of two wanderers.
#
# Logic:
#   - Start at opposite corners
#   - Move both individuals each tick
#   - Stop if they meet or time limit is reached
#
# Returns:
#   (tick, location) if meeting occurs
#   (None, None) if no meeting
#
# Parameters:
#   N -> grid size
#   T -> max ticks
def single_simulation(N, T)-> tuple[int,Coord]|tuple[None,None]:
	person_a:Coord = (0,0)
	person_b:Coord = (N - 1, N - 1)
	for tick in range(1, T):
		person_a = update_position(person_a, get_direction(), N)
		person_b = update_position(person_b, get_direction(), N)
		if person_a == person_b:
			return tick, person_a

	return None, None

# ****************************************************************************************************************************************************************
# Analyzes simulation results and displays statistics + histogram.
#
# Parameters:
#   simulation_lengths -> list of meeting times
#   R -----------------> total simulations
def simulation_analysis_and_histogram(simulation_lengths, R):
    """
    Performs simulation analysis and displays results + histogram.

    Parameters:
        simulation_lengths (array/list): lengths of simulations where meetings occurred
        R (int): total number of simulations
    """

    # Convert to regular Python list (handles NumPy array)
    lengths = [int(x) for x in simulation_lengths]

    if len(lengths) == 0:
        print("\n--- Simulation Analysis ---")
        print("No meetings occurred in any simulation.")
        print(f"Total simulations: {R}")
        print(f"Meetings: 0")
        print(f"No meetings: {R}")
        return

    max_time = max(lengths)
    min_time = min(lengths)
    avg_time = sum(lengths) / len(lengths)

    meeting_count = len(lengths)
    no_meeting_count = R - meeting_count

    # --- PRINT RESULTS ---
    print("\n--- Simulation Analysis ---")
    print(f"Total simulations: {R}")
    print(f"Meetings: {meeting_count}")
    print(f"No meetings: {no_meeting_count}")
    print(f"Max time: {max_time}")
    print(f"Min time: {min_time}")
    print(f"Average time: {avg_time:.2f}")

    # --- HISTOGRAM ---
    plt.figure()
    plt.hist(lengths, bins=20)
    plt.title("Histogram of Simulation Ending Times")
    plt.xlabel("Time Steps")
    plt.ylabel("Frequency")
    plt.grid()
    plt.show()


# ****************************************************************************************************************************************************************
# Writes simulation results to a timestamped text file.
# Expects lengths to contain one entry per simulation.
# Parameters: N -------------> grid size
#             T -------------> max ticks per simulation
#             R -------------> number of simulations
#             lengths -------> list/array of simulation lengths
#             heatmap -------> 2D array of meeting counts
#             meeting_count -> number of successful meetings
#             group_names ---> list of group member names
def write_results(N, T, R, lengths, heatmap, meeting_count, group_names):
	
	# Convert NumPy array (or iterable) of lengths into a standard Python list of integers
	lengths_list = lengths
	
	# Sort group member names alphabetically for consistent output
	sorted_names = sorted(group_names)

	# Calculate statistics if data exists
	if lengths_list:
		max_length = max(lengths_list)
		min_length = min(lengths_list)
		average_length = sum(lengths_list) / R if R != 0 else 0
	else:
		# Handle edge case where no simulations succeeded
		max_length = "N/A"
		min_length = "N/A"
		average_length = 0
	
	# Initialize histogram array to count frequency of each tick value
	histogram = [0] * (T + 1)
	
	for tick in lengths_list:
		if 0 <= tick <= T:
			histogram[tick] += 1

	# Generate timestamp for unique filename
	timestamp = datetime.now()
	filename = f"WANDERING_{timestamp:%Y%m%d}_{timestamp:%H%M%S}.txt"
	
	# Determine directory where file will be saved
	script_directory = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
	output_path = script_directory / filename

	# Open file for writing results
	with output_path.open("w", encoding="utf-8") as result_file:
		result_file.write("Group Members: " + ", ".join(sorted_names) + "\n")
		result_file.write(f"N={N}, T={T}, R={R}\n")
		result_file.write(f"Max: {max_length} Min: {min_length} Avg: {average_length}\n")
		result_file.write(f"Meetings: {meeting_count} No meetings: {R - meeting_count}\n")
		result_file.write("Histogram:\n")

		for tick in range(0, T + 1):
			if histogram[tick] > 0:
				result_file.write(f"{tick}: {'*' * histogram[tick]}\n")

		result_file.write("Heatmap:\n")
		for row in heatmap:
			result_file.write(" ".join(str(int(value)) for value in row) + "\n")

	print(f"Results written to {output_path}")
	input("Press ENTER to exit")
	
	# Return file path for potential further use
	return output_path

# ****************************************************************************************************************************************************************
# Main function: controls program execution
def main():
    
	#program explanation
	#get N
	N = 100

	#get R
	R = 100

	#get T
	T = 10000

	#run simulations
	group_names = ["Alex Fahnestock", "Jackie Herbstreit", "Tressa Millering", "May Salahaldin", "AJ Soma Ravichandran"]
	meeting_locations, simulation_lengths, heatmap = run_simulations(N, T, R)
	simulation_analysis_and_histogram(simulation_lengths, R)
	write_results(N, T, R, simulation_lengths, heatmap, len(meeting_locations), group_names)

	#SIMPLE TESTBENCH
	#test_bench(N, meeting_locations, simulation_lengths, heatmap)



# ****************************************************************************************************************************************************************
if __name__ == "__main__":
	main()
