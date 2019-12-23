# ODE calculator
# Isaac Krementsov
# Created 12/20/2019
# A graphing calculator to display solutions to differential equations


from flask import Flask, render_template, request
import numpy as np
import decimal
import re


# Import the internal modules for solving the ODE and generating data
from ODECalculator import ODECalculator
from DataGenerator import DataGenerator


# Initialize a new Flask application
app = Flask(__name__)


# This is an SPA, so / is the only route mapping
@app.route('/')
def calculator():
    # Get the equation entered by the user if they are submitting the form
    equation_input = request.values.get('equation')
    equation_original = request.values.get('equation_original')

    try:
        # If the user entered form data, respond with the ODE solution
        if equation_input:
            # Parse the equation string to a usable function and record the equation's highest order derivative, or degree
            get_highest_order, equation_degree = parse_equation(equation_input)

            # Get the graph resolution for generating data as a float
            dataset_step_string = request.values.get('dataset_step');
            dataset_step = float(dataset_step_string)
            # Find the decimal precision of this step for rounding
            precision = -decimal.Decimal(dataset_step_string).as_tuple().exponent

            # Get the t-interval or step to solve by numeric integration
            t_step = float(request.values.get('t_step'))

            # Get the t-range to graph the ODE solution over
            dataset_tmin = int(request.values.get('dataset_tmin'))
            dataset_tmax = int(request.values.get('dataset_tmax'))

            # Get the initial conditions of the differential equation and parse them into a list
            initial_condition_input = request.values.get('initial_conditions')
            initial_conditions = map(int, initial_condition_input.split(','))
            initial_conditions = list(initial_conditions)

            # Make sure that the initial conditions match the equation degree (ex. a 2nd order ODE needs y(0), y'(0))
            if len(initial_conditions) == equation_degree:
                # Initilize the calcuator
                calculator = ODECalculator(initial_conditions, get_highest_order, t_step)
                # Plug in the ODE solution as the function for the data generator to evaluate
                data_generator = DataGenerator(calculator.solution)

                # Use the data generator to create a set of coordinates usable for ChartJS
                dataset = data_generator.generate_data(dataset_tmin, dataset_tmax, dataset_step, precision)

                # Render the template with data and pass the original parameters back to the user
                return render_template('calculator.html', dataset=dataset, original=equation_original, t_min=dataset_tmin, t_max=dataset_tmax)

            else:
                # If the improper amount of initial conditions were provided, provide the user with an error
                error = 'You need ' + str(equation_degree) + ' initial condition'
                if equation_degree > 1:
                    error += 's'

                return render_template('calculator.html', error=error)
        else:
            # If no form data was sent, simply render the page
            return render_template('calculator.html')

    except ValueError:
        # If there was an error parsing form data, send it to the user
        return render_template('calculator.html', error='Invalid Form Data')

    except Exception as e:
        print(e)
        # If there was another error, it was probably an issue with the server code
        return render_template('calculator.html', error='Sorry, there was a server error')


# Parse a user-entered equation string
# The client side makes this into something like initial_conditions[2]=...initial_conditions[0]...initial_conditions[1]
# The index represents the number of " ' " characters after y, or the order of the derivative
def parse_equation(equation_string):
    # Find all areas where an initial_conditions index was referenced
    derivative_degrees = re.findall('\[[0-9]+\]', equation_string)

    for i, degree in enumerate(derivative_degrees):
        # Each string looks like [x], where x is the degree of the derivative; remove brackets
        derivative_degrees[i] = re.sub('\[|\]', '', degree)

    # Make all degrees integers
    derivative_degrees = map(int, derivative_degrees)
    # Find the maximum of all degrees present
    equation_max_degree = max(derivative_degrees)


    # Callback to reverse the indices so that 0 is the highest derivative and the highest index is y
    # This needs to be a local function so that it can access equation_max_degree
    def choose_instance_index(match):
        # For a REGEX match, remove brackets and get the index number
        index_number = int(re.sub('\[|\]', '', match.group()))
        # Reverse the index
        correct_index = equation_max_degree - index_number

        # Put brackets back on
        return '[' + str(correct_index) + ']'


    # Substitute the equation's indices with the callback
    equation_string = re.sub('\[[0-9]+\]', choose_instance_index, equation_string)
    # Make all functions "np." so that they can be called by the code; replace "^" with "**" for exponentiation
    equation_string = re.sub('(sin|tan|cos|arcsin|arctan|arccos)\(', add_np, equation_string)
    equation_string = re.sub('e(?!(_|s))', '2.71828', equation_string)
    equation_string = equation_string.replace('pi', '3.14159')
    equation_string = equation_string.replace('^', '**')

    # Change the log functions because numpy uses log instead of ln and log10 instead of log
    equation_string = equation_string.replace('ln(', 'np.log(')
    equation_string = equation_string.replace('log(', 'np.log10(')

    # Evaluate the right side of the function to calculate the highest order derivative in the ODE
    def get_highest_order(instance_values, t):
        right_side = equation_string.split('=')[1]
        return eval(right_side)


    return get_highest_order, equation_max_degree


# Add "np." to mathematical functions
def add_np(match):
    with_np = 'np.' + match.group()
    return with_np


# Run the app on port 5000 by default
if __name__ == 'main':
    app.run()
