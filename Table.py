import numpy as np

class Table:
    def __init__(self, function):
        self.function = function

    def generate_table(self, x_initial, x_final, step):
        values = dict()

        for x in range(x_initial, x_final, step):
            values[x] = self.function(x)
