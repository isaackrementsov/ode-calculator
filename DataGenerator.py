import numpy as np

class DataGenerator:
    def __init__(self, function):
        self.function = function

    def generate_data(self, x_initial, x_final, step):
        values = []

        for x in np.arange(x_initial, x_final, step):
            coordinates = {'x': x, 'y': self.function(x)}

            values.append(coordinates)

        return values
