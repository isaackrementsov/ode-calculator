from flask import Flask, render_template, request
import re

from ODECalculator import ODECalculator
from DataGenerator import DataGenerator

app = Flask(__name__)

@app.route('/')
def calculator():
    equation_input = request.values.get('equation')

    if equation_input:
        get_highest_order, equation_degree = parse_equation(equation_input)

        dataset_step = float(request.values.get('dataset_step'))
        dataset_xmin = int(request.values.get('dataset_xmin'))
        dataset_xmax = int(request.values.get('dataset_xmax'))
        initial_condition_input = request.values.get('initial_conditions')
        initial_conditions = map(int, initial_condition_input.split(','))
        initial_conditions = list(initial_conditions)
        initial_conditions.insert(0, 0)

        if len(initial_conditions) >= equation_degree - 1:
            calculator = ODECalculator(initial_conditions, get_highest_order, dataset_step)
            data_generator = DataGenerator(calculator.solution)

            dataset = data_generator.generate_data(dataset_xmin, dataset_xmax, dataset_step)

            return render_template('calculator.html', dataset=dataset)

    else:
        return render_template('calculator.html')

def parse_equation(equation_string):
    derivative_degrees = re.findall('\[[0-9]+\]', equation_string)

    for i, degree in enumerate(derivative_degrees):
        derivative_degrees[i] = re.sub('\[|\]', '', degree)

    derivative_degrees = map(int, derivative_degrees)

    equation_max_degree = max(derivative_degrees)

    def choose_instance_index(match):
        index_number = int(re.sub('\[|\]', '', match.group()))
        correct_index = equation_max_degree - index_number

        return '[' + str(correct_index) + ']'

    equation_string = re.sub('\[[0-9]+\]', choose_instance_index, equation_string)
    equation_string = re.sub('(sin|tan|cos|arcsin|arctan|arccos)\(', add_np, equation_string)
    equation_string = equation_string.replace('^', '**')
    equation_string = equation_string.replace('ln(', 'np.log(')
    equation_string = equation_string.replace('log(', 'np.log10(')

    def get_highest_order(instance_values, t):
        right_side = equation_string.split('=')[1]

        return eval(right_side)

    return get_highest_order, equation_max_degree

def add_np(match):
    with_np = 'np.' + match.group()
    return with_np

if __name__ == 'main':
    app.run()
