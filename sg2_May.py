# input validation

# gets a valid number from the user within a range
def get_valid_input(prompt, min_value, max_value, name):
    while True:
        user_input = input(prompt)
        
        # check if input is a number
        if not user_input.isdigit():
            print(f"Error: {name} must be a number.")
            continue
        
        value = int(user_input)
        
        
        # check if value is in range
        if value < min_value or value > max_value:
            print(f"Error: {name} must be between {min_value} and {max_value}.")
        else:
            return value

# ask user to enter N, T, R values
def get_user_inputs():
    print("\nEnter values for the simulation:")
    
    N = get_valid_input("Enter grid size N (2-100): ", 2, 100,	"N")
    T = get_valid_input("Enter time limit T (2-1000000): ", 2, 1000000,	"T")
    R = get_valid_input("Enter number of simulations R (1-100000): ", 1, 100000, "R")
    
    return N, T, R


# test
N, T, R = get_user_inputs()
print("Values:", N, T, R)
