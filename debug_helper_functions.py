import numpy as np


"""
Displays a progress bar while simulations are running. 
Updates the same console line to show completion percentage.
	:param sim: current simulation number
	:param R:   total number of simulations
"""
def loading_screen(sim, R):
    bar_length = 30
    progress = sim / R
    filled = int(progress * bar_length)
    empty = bar_length - filled

    bar = "█" * filled + "░" * empty
    percent = progress * 100

    print(f"\r{bar}  ---  {percent:.3f}%", end="")


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

