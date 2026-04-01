#*************************************************************************************************
#   Language - Python 3.10
#   IDE -
#       Tressa - Primarily programmed using PyCharm for its
#                version control tools, later tested in Thonny
#



#     NOTE FROM TRESSA
#     I'm using Pycharm to program, mostly because Thonny
#     runs terribly on my machine; I figure if we are all
#     using a different IDE, we can just list them separately.
#     If it turns out we are all using Pycharm, then nevermind lol
#
#     ALSO- I have it listed as Python 3.10 because thats the version of
#     python that comes preinstalled with Thonny. Its probably safest, but
#     if we need features exclusive to a later version we can look into it
#



#   Python Packages REQUIRED - (must be installed with Thonny IDE, "Tools>Manage Packages")
#       - NumPy
#       - Matplotlib
#
#   Authors -
#       - Alex Fahnestock
#       - Jackie Herbstreit
#       - Tressa Millering
#       - May Salahaldin
#       - AJ Soma Ravichandran
#
#
#   Important Dates -
#       Repository created 03/11/2026
#       Rough Design Drafted 03/15/2026
#       Basic Simulation Implemented 03/24/2026
#
#   Course -
#        CS 4500 - Intro to the Software Profession
#
#
#   Program Explanation -
#
#
#   Outside Sources:
#
#       https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html
#           - Used to determine the direction of a given movement without floating point comparisons
#
#*************************************************************************************************

import numpy as np
import matplotlib.pyplot as plt





#************************************************
#Prints an array in a single line
#If you just do print(np-array), each element is a new line.
# This is just prettier for testing.
#Code is taken from Tressa's SG1 and slightly modified
#Parameters: array -> the array being printed
#            label -> an optional prefix for clarity in output
def print_array(array, label=""):
    print(label + (":" if (label != "") else ""))
    for _ in range(0, len(array)):
        print(array[_], end=" ")
    print("\n")

#*******************************************


#*******************************************
#
#REMOVE FOR FINAL SUBMISSION
#
#Checks to see if a random location on the grid
#  has the same number of occurrences in meeting_locations
#  and the heatmap. Also verifies the number of values
#  in all data structures
#Basically just checks for an obvious logical error
#Parameters are all values returned by run_simulations
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

#*******************************************


#********************************************
#Displays a visual progress bar during simulation execution.
#Called once per simulation inside run_simulations().
#Calculates percent completion and updates the same console line in-place.
#Code is originally from Tressa's SG1
#Parameters: sim -> the current simulation
#            R ---> the total number of simulations
def loading_screen(sim, R):
    bar_length = 30
    progress = sim / R
    filled = int(progress * bar_length)
    empty = bar_length - filled

    bar = "█" * filled + "░" * empty
    percent = progress * 100

    print(f"\r{bar}  ---  {percent:.3f}%", end="")

#********************************************


#********************************************
#Runs R simulations & displays a loading screen to show progress
#Returns an array of simulation lengths (in ticks),
#    an array of tuples representing meeting locations,
#    and a 2D array representing the heatmap.
#Parameters:  N -> grid size
#             T -> ticks per simulation
#             R -> simulation count
def run_simulations(N, T, R):
    print("\nRunning simulations...\n")
    heatmap = np.zeros((N, N), dtype=int)
    simulation_lengths = []
    meeting_locations = []
    for sim in range(0, R):
        loading_screen(sim + 1, R)  # +1 ensures it reaches 100%
        ticks, loc = single_simulation(N, T)
        if (ticks != None):
            simulation_lengths.append(ticks)
            meeting_locations.append(loc)
            heatmap[loc[0]][loc[1]] += 1

    print("\nSimulations complete!\n")

    lengths_array = np.array(simulation_lengths)
    meetings_array = np.array(meeting_locations)
    return meetings_array, lengths_array, heatmap

#********************************************


#********************************************
#Helper function that generates a random direction
#  in the form of grid coordinates. Effectively works by
#  flipping two coins, one for positive or negative
#  movement, and one for x or y movement.
#  Returns a tuple representing a 2D movement vector.
def get_direction():
    magnitude = 1
    if (np.random.randint(0, 2) == 0):
        magnitude = -1

    if (np.random.randint(0, 2) == 0):
        return (0, magnitude)
    else:
        return (magnitude, 0)

#********************************************


#********************************************
#Helper function that checks if a move is valid,
#  and moves the subject if so.
#Parameters: position --> tuple of current position
#            direction -> tuple of how much to move position by
#            N ---------> grid size
#Returns updated position + direction if valid, position if not
def update_position(position, direction, N):
    if (0 <= position[0] + direction[0] <= N-1) and (0 <= position[1] + direction[1] <= N-1):
        return (position[0] + direction[0], position[1] + direction[1])
    else:
        return position

#********************************************


#********************************************
#Runs a single simulation of the two wanderers.
#   Works by storing the position of each person
#   in their own variable, then running a loop
#   that updates each position once per iteration,
#   breaking at T iterations or if the two positions
#   are found to be equal
#Parameters: N -> grid size
#            T -> max ticks per simulation
#If simulation ends without a meeting, returns
#   a tuple null values if unsuccessful
#If a meeting occurs, returns the current tick and
#   the location of the meeting
def single_simulation(N, T):
    person_a = (0,0)
    person_b = (N - 1, N - 1)
    for tick in range(1, T):
        person_a = update_position(person_a, get_direction(), N)
        person_b = update_position(person_b, get_direction(), N)
        if person_a == person_b:
            return tick, person_a

    return None, None

# ********************************************


# ********************************************
def main():
    #program explanation
    #get N
    N = 100

    #get R
    R = 100

    #get T
    T = 10000

    #run simulations
    meeting_locations, simulation_lengths, heatmap = run_simulations(N, T, R)

    #SIMPLE TESTBENCH
    test_bench(N, meeting_locations, simulation_lengths, heatmap)

    #output data
    #prompt user to hit enter to continue
    #on enter hit, write to text file and exit prog


# ********************************************

if __name__ == "__main__":
    main()
