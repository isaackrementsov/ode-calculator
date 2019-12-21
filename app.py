from flask import Flask, render_template, request
import re

from ODECalculator import ODECalculator
from DataGenerator from DataGenerator

app = Flask(__name__)

@app.route('/')
def calculator():
    equation_input = request.values.get('equation')

    if equation_input:
        get_highest_order, equation_degree = parse_equation(equation_input)

        initial_condition_input = request.values.get('initial_values')
        initial_conditions = initial_condition_input.split(',')
        initial_conditions = list(map(int, initial_values))

        if initial_values.length >= equation_degree - 1:
            calculator = ODECalculator(initial_conditions, get_highest_order, 0.01)
            data_generator = DataGenerator(calculator.solution)

            dataset = data_generator.generate_data()

            return render_template('calculator.html', dataset=dataset)

    else:
        return render_template('calculator.html')

def parse_equation(equation_string):
    equation_string = re.sub("y(')\1{0,}", replace_y_prime)

def replace_y_prime(match):


if __name__ == 'main':
    app.run()
