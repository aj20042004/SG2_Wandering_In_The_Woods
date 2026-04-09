"""
╔═════════════════════════════════════════════════════════════════════════════════════════════╗
║ SG2                                                                      					  ║
╠━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╣
║ Language: Python 3.10                                                						  ║
║ IDE: Thonny, VSCode, Pycharm                                      						  ║
║ Class: CS 4500 - Intro to the Software Profession                 						  ║
║ Program: SG2 - Wandering in the Woods                             						  ║
║ Group Members:                                                    						  ║
║  - Alex Fahnestock      [afan2211]                                						  ║
║  - Jackie Herbstreit    []                                        						  ║
║  - Tressa Millering     [dtmhg6]                                  						  ║
║  - AJ Soma Ravichandran [aj20042004]                              						  ║
║  - May Salahaldin       []                                        						  ║
╠━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╣
║ Program Description																		  ║
╠---------------------------------------------------------------------------------------------╣
║	This program simulates two strangers moving randomly on an N x N grid to determine		  ║
║	if and when they meet. They start at opposite corners and move each time step (T).        ║
║	The simulation runs R times to collect statistical data.								  ║
║																							  ║
║	The program:																			  ║
║ 	- Takes validated inputs for N (grid size), T (time limit), and R (runs)				  ║
║	- Runs R simulations of random movement													  ║
║	- Records ending time, meeting occurrence, and meeting locations						  ║
║	- Displays max, min, and average times, a histogram, and a heat map						  ║
║	- Saves results to a timestamped output file											  ║
║																						      ║
║	Simulation Logic:																		  ║
║	- Each step, both individuals move randomly (up, down, left, right, or stay if blocked)	  ║
║	- If both land on the same cell, they meet and the simulation ends						  ║
║	- Otherwise, the simulation continues until time reaches T								  ║
║																						      ║
║	Data Structures:																		  ║
║	- times_list: Stores the number of steps taken for each simulation.						  ║
║	- meet_count: Tracks how many simulations resulted in a meeting.						  ║
║	- no_meet_count: Tracks how many simulations ended without meeting.					 	  ║
║	- heat_map: 2D array (N x N) storing counts of meeting locations.						  ║
║	- histogram_data: Stores frequency distribution of ending times.ion						  ║
╠━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╣
║ Revision History     																		  ║
║   - 03/11/2026 (Repository created)														  ║
║	- 03/15/2026 (Rough Design Drafted)														  ║
║	- 03/24/2026 (Basic Simulation Implemented)   											  ║
║																						  	  ║
║    - INSERT DATE (Final Version Submitted)												  ║
║                                                    						                  ║
╟─────────────────────────────────────────────────────────────────────────────────────────────╢
║ Packages Used        																		  ║
║	- Numpy																					  ║
║	- Matplotlib                                  							          		  ║
║                                  							          						  ║
╠━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╣
║ Outside Sources																			  ║
║																							  ║
╚═════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Import necessary libraries
from datetime import datetime
from pathlib import Path
from typing import Any,Literal,cast

import numpy as np
import matplotlib.pyplot as plt
import random 


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Define type aliases for readability
type Coord=tuple[int,int]  # type alias for readability
type MovementVector=tuple[Literal[-1,0,1],Literal[-1,0,1]] 
type Box[T] = list[T]
type NumpyArray2D[T:np.generic]=np.ndarray[tuple[int, int], np.dtype[T]]

# Define a mapping of random integers to movement vectors (up, down, left, right)
DIRECTION_TABLE:dict[Literal[0,1,2,3],MovementVector]={0:(0,1) ,1:(0,-1),2:(-1,0),3:(1,0)}

#Data plot styling
plt.style.use('bmh')
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
Displays a progress bar while simulations are running. 
Updates the same console line to show completion percentage.

	:param sim | (int): current simulation number
	:param R   | (int): total number of simulations
"""
def loading_screen(sim:int, R:int):
    bar_length:int = 30
    progress:float = sim / R
    filled:int = int(progress * bar_length)
    empty:int = bar_length - filled

    bar:str = "█" * filled + "░" * empty
    percent:float = progress * 100

    print(f"\r{bar}  ---  {percent:.3f}%", end="")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

Gets a valid integer input from the user within a given range.

Parameters:
    prompt (str): message shown to the user
    min_value (int): minimum allowed value
    max_value (int): maximum allowed value

Returns:
    int: valid number entered by the user

"""
def get_valid_input(prompt, min_value, max_value):
    while True:
        user_input = input(prompt)
        
        if not user_input.isdigit():
            print("Error: please enter a number.")
            continue
        
        value = int(user_input)
        
       
        if value < min_value:
            print(f"Error: value is too small. Minimum is {min_value}.")
        elif value > max_value:
            print(f"Error: value is too large. Maximum is {max_value}.")
        else:
            return value

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

Asks the user to enter simulation values (N, T, R).

Returns:
    tuple: N (grid size), T (time limit), R (number of simulations)

"""
def get_user_inputs():
    print("--------------------------------------------------------")
    print("            Enter values for the simulation:            ")
    print("--------------------------------------------------------")
    
    N = get_valid_input("Enter grid size N (2-100): ", 2, 100)
    T = get_valid_input("Enter time limit T (2-1000000): ", 2, 1000000)
    R = get_valid_input("Enter number of simulations R (1-100000): ", 1, 100000)
    
    return N, T, R

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
Runs R simulations & displays a loading screen to show progress

    :param N  | (int): grid size
    :param T  | (int): number of ticks to run before we timeout
    :param R  | (int): simulation count

    :return: tuple[list[Coord]: list of meeting coordinates,
                   list[int]: list of simulation lenghts,
                   NumpyArray2d[np.uint32]: 2D array representing heatmap]                
"""
def run_simulations(N:int, T:int, R:int)->tuple[list[Coord],list[int],NumpyArray2D[np.integer]]:
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

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
  Helper function that generates a random direction in the form of grid coordinates

  :return: a tuple representing a 2D movement vector.
"""
def get_direction()->MovementVector:
    return DIRECTION_TABLE[random.choice([0,1,2,3])]

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
Updates position if move stays within grid boundaries.

	:param position  | (Coord): current position of target
	:param direction | (Coord): intended movement vector 
	:param N         |   (int): grid size
	
	:return: if movement is valid, (position + direction)
			 else, position 
"""
def update_position(position:Coord, direction:Coord, N:int)->Coord:
    if (0 <= position[0] + direction[0] <= N-1) and (0 <= position[1] + direction[1] <= N-1):
        return (position[0] + direction[0], position[1] + direction[1])
    else:
        return position

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
Runs a single simulation of two wanderers.
Logic:
  - Start at opposite corners
  - Move both individuals each tick
  - Stop if they meet or time limit is reached

	:param N | (int): grid size
	:param T | (int): maximum ticks per simulation

	:return: Tuple[int:tick, Coord:location] if meeting occurs
  			 Tuple[None, None] if no meeting
"""
def single_simulation(N:int, T:int)-> tuple[int,Coord]|tuple[None,None]:
    person_a:Coord = (0,0)
    person_b:Coord = (N - 1, N - 1)
    for tick in range(1, T):
        person_a = update_position(person_a, get_direction(), N)
        person_b = update_position(person_b, get_direction(), N)
        if person_a == person_b:
            return tick, person_a

    return None, None

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
Analyzes simulation results and displays statistics + histogram.

	:param simulation_lengths | (list): list of meeting times to analyze
	:param R                  |  (int): total number of simulations
"""
def simulation_analysis_and_histogram(simulation_lengths:list[int], R:int):
    if len(simulation_lengths) == 0:
        print("\n    Simulation Analysis    ")
        print("-" * 30)
        print("No meetings occurred in any simulation.")
        print(f"Total simulations: {R}")
        print(f"Meetings: 0")
        print(f"No meetings: {R}")
        return

    max_time = max(simulation_lengths)
    min_time = min(simulation_lengths)
    avg_time = sum(simulation_lengths) / len(simulation_lengths)

    meeting_count = len(simulation_lengths)
    no_meeting_count = R - meeting_count

    # --- PRINT RESULTS ---
    print("--------------------------------------------------------")
    print("                 Simulation Analysis                    ")
    print("--------------------------------------------------------")
    print(f"Total simulations: {R}")
    print(f"Meetings: {meeting_count}")
    print(f"No meetings: {no_meeting_count}")
    print(f"Maximum time: {max_time}")
    print(f"Minimum time: {min_time}")
    print(f"Average time: {avg_time:.2f}")

    # --- HISTOGRAM ---
    plt.figure()
    plt.hist(simulation_lengths, linewidth="1", edgecolor="black", color="skyblue", bins=35)
    plt.title("Histogram of Simulation Ending Times")
    plt.xlabel("Time Steps")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
Writes simulation results to a timestamped text file.
Expects lengths to contain one entry per simulation.

    :param N             |                 (int): grid size
    :param T             |                 (int): max ticks per simulation
    :param R             |                 (int): number of simulations
    :param lengths       |           (list[int]): list/array of simulation lengths
    :param heatmap       | (Np2DArray[int, int]): 2D array of meeting counts
    :param meeting_count |                 (int): number of successful meetings
    :param group_names   |           (list[str]): list of group member names
    
    :return: path to output file
"""
def write_results(N:int, T:int, R:int, lengths:list[int], heatmap, meeting_count:int, group_names:list[str])->Path:

    # Sort group member names alphabetically for consistent output
    sorted_names = sorted(group_names)

    # Calculate statistics if data exists
    if lengths:
        max_length = max(lengths)
        min_length = min(lengths)
        average_length = sum(lengths) / R if R != 0 else 0
    else:
        # Handle edge case where no simulations succeeded
        max_length = "N/A"
        min_length = "N/A"
        average_length = 0

    # Initialize histogram array to count frequency of each tick value
    histogram = [0] * (T + 1)

    for tick in lengths:
        if 0 <= tick <= T:
            histogram[tick] += 1

    # Determine directory where file will be saved
    script_directory = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    existing_files = sorted(
        script_directory.glob("WANDERING_*.txt"),
        key=lambda path: path.stat().st_mtime,
        reverse=True
    )
    timestamp = datetime.now()
    filename = f"WANDERING_{timestamp:%d_%m_%Y}_{timestamp:%H_%M}.txt"
    output_path = script_directory / filename

    if existing_files:
        latest_file = existing_files[0]
        if latest_file != output_path:
            latest_file.unlink()

    # Open file for writing results
    with output_path.open("w", encoding="utf-8") as result_file:
        result_file.write("         SG2 Project: Wandering in the Woods Simulation Results          \n")
        result_file.write("-------------------------------------------------------------------------\n")
        result_file.write("\nGroup Members: " + ", ".join(sorted_names) + "\n")
        result_file.write(f"\nN={N}, T={T}, R={R}\n")
        result_file.write(f"\nMaximum Time: {max_length}, Minimum Time: {min_length}, Average Time: {average_length}\n")
        result_file.write(f"\nMeetings: {meeting_count}, No meetings: {R - meeting_count}\n")
        result_file.write("\nHistogram:\n")
        result_file.write("---------------------------------------------------------------------------------------\n")
        for tick in range(0, T + 1):
            if histogram[tick] > 0:
                result_file.write(f"{tick}: {'*' * histogram[tick]}\n")

        result_file.write("\nHeatmap:\n")
        result_file.write("---------------------------------------------------------------------------------------\n")
        for row in heatmap:
            result_file.write(" ".join(str(int(value)) for value in row) + "\n")

    print(f"\nResults written to {output_path}")
    input("Press ENTER to exit")

    # Return file path for potential further use
    return output_path

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main function: controls program execution
def main():
    
    #program explanation
    print("\n")
    print("-" * 100)
    print("SG2: Wandering in the Woods Simulator")
    print("-" * 100)
    
    print(
"""This program simulates two strangers wandering randomly in a square grid,
to study how long it takes for them to meet.

The simulation takes place on an N x N grid. One person starts in the top-left
corner, and the other starts in the bottom-right corner.

Time progresses in steps (ticks). At each time step:
1. Each person randomly chooses to move up, down, left, or right.
2. If a move would take them off the grid, they stay in place.
3. After both have moved, the program checks if they are in the same square.

If both people land on the same square at the same time, they meet and the
simulation ends. If they do not meet, the simulation continues until the
maximum time limit (T) is reached.

This experiment is repeated R times to gather meaningful statistics.

The program will calculate and display:
1. The maximum time taken for a simulation to end
2. The minimum time taken for a simulation to end
3. The average time taken across all simulations
4. A histogram showing how often simulations ended at each time step
5. A heatmap showing where meetings occurred on the grid

You will now be asked to enter:
1. N - the size of the grid (between 2 and 100)
2. T - the maximum number of time steps (between 2 and 1,000,000)
3. R - the number of simulations to run (between 1 and 100,000)

After all simulations are complete, the results will be displayed,
and a detailed report will be saved to a text file.
"""
)

    # get user inputs
    N, T, R = get_user_inputs()

    # define group member names for output file
    group_names = ["Alex Fahnestock", "Jackie Herbstreit", "Tressa Millering", "May Salahaldin", "AJ Soma Ravichandran"]
    
    # run simulations and collect data
    meeting_locations, simulation_lengths, heatmap = run_simulations(N, T, R)
    
    # analyze results and display statistics + histogram
    simulation_analysis_and_histogram(simulation_lengths, R)
    
    # WWrite results to output file
    write_results(N, T, R, simulation_lengths, heatmap, len(meeting_locations), group_names)


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    main()
