import numpy as np


# ODE solution generator
class ODECalculator:


    # Initialize the calculator with the ODE parameters
    def __init__(self, initial_conditions, get_highest_order, dt):
        # Insert 0,0 to represent that the highest order derivative does not need an initial value
        initial_conditions.insert(0,0)

        self.initial_conditions = initial_conditions
        self.get_highest_order = get_highest_order
        self.dt = dt


    # Solve the ODE at a particular point
    def solution(self, x):
        # Start each derivative value (and y) at the initial conditions
        instance_values = list(self.initial_conditions)
        # The number of initial conditions is the same as the equation order or degree
        equation_degree = len(instance_values) - 1

        # Generate the range of values for numeric integration with a Reimann sum
        for t in np.arange(0, x, self.dt):
            # Calculate each derivative (and y) in instance values
            for i in range(equation_degree + 1):
                if i == 0:
                    # For the highest derivative, use the user-defined function to calculate it
                    instance_values[i] = self.get_highest_order(instance_values, t)
                else:
                    # For the higher derivatives (and y), increment by the previous derivative, numerically integrating
                    instance_values[i] += instance_values[i - 1] * self.dt

        # Return the highest instance value index, which is y
        return instance_values[equation_degree]
