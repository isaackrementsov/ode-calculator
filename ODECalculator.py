import numpy as np

class ODECalculator:
    def __init__(self, initial_conditions, get_highest_order, dt):
        self.initial_conditions = initial_conditions
        self.get_highest_order = get_highest_order
        self.dt = dt

    def solution(self, x):
        instance_values = self.initial_conditions
        equation_degree = len(instance_values) - 1

        for t in np.arange(0, x, self.dt):
            for i in range(equation_degree + 1):
                if i == 0:
                    instance_values[i] = self.get_highest_order(instance_values, t)
                else:
                    instance_values[i] += instance_values[i - 1] * self.dt

        return instance_values[equation_degree]
