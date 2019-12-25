import numpy as np
import math

class DataGenerator:


    # Set the function to generate data
    def __init__(self, function):
        self.function = function


    # Generate the dataset for ChartJS to graph on the frontend
    def generate_data(self, x_initial, x_final, step, precision):
        # Initialize the array to store values
        values = []

        # Generate the set of values to evaluate the function over
        for x in np.arange(x_initial, x_final, step):
            # Find the function's value at this x-value
            try:
                y = self.function(x)

                # Make sure that y is a number; otherwise, it will not graph
                if not math.isnan(y):
                    # Generate a ChartJS-style coordinate dictionary
                    coordinates = {'x': round(x, precision), 'y': round(y, precision)}

                # Add the value into the dataset array
                values.append(coordinates)

            # Prevent errors when large values or asymptotes show up
            except OverflowError:
                y = 0
        # Return the dataset for use on the frontend
        return values
