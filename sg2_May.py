# input validation
def get_valid_input(prompt, min_value, max_value):
    while True:
        user_input = input(prompt)
        
        if not user_input.isdigit():
            print("Error: please enter a number.")
            continue
        
        value = int(user_input)
        
        # check range
        if value < min_value or value > max_value:
            print(f"Error: must be between {min_value} and {max_value}.")
        else:
            return value


def get_user_inputs():
    print("\nEnter values for the simulation:")
    
    N = get_valid_input("Enter grid size N (2-100): ", 2, 100)
    T = get_valid_input("Enter time limit T (2-1000000): ", 2, 1000000)
    R = get_valid_input("Enter number of simulations R (1-100000): ", 1, 100000)
    
    return N, T, R


# test
N, T, R = get_user_inputs()
print("Values:", N, T, R)
