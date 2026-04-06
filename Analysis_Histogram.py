import matplotlib as plt
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