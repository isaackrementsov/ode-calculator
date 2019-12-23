
# ODE-Calculator

### ODE Grapher Web App using Flask
Check it out online [here](http://odecalculator.pythonanywhere.com)

### How it works
This is a way to graph any Ordinary Differential Equation, based on the code from [3Blue1Brown's video](https://www.youtube.com/watch?v=p_di4Zn4wz4)

Let's say you have the equation
<p style="text-align: center"><img src="https://latex.codecogs.com/svg.latex?y''=-0.5y-4.9sin(y)"></p>
<p style="text-align: right"><b>(eq 1)</b></p>
This is an equation that can be used to model damped pendulum motion over time, where <i>y</i> is position, <i>y'</i> is velocity, and <i>y''</i> is acceleration.
Instead of attempting to use algebraic techniques and theorems to solve the equation (which is near impossible in this case), this program uses numeric integration.
The goal here is to find <i>y</i> as a function of an input variable, which can be denoted <i>T</i>. Based on the Fundamental Theorem of Calculus,
<p style="text-align: center"><img src="https://latex.codecogs.com/svg.latex?y(T)=\int_0^Ty'dt&plus;y(0)"></p>
<p style="text-align: right"><b>(eq 2)</b></p>
<p style="text-align: center"><img src="https://latex.codecogs.com/svg.latex?y'(T)=\int_0^Ty''dt&plus;y'(0)"></p>
<p style="text-align: right"><b>(eq 3)</b></p>
Finally, we know the definition of <i>y''</i> from equation 1. All of these values are defined in terms of each other, which would seem problematic at first.
However, this issue is solved by starting with <i>y'(0)</i> and <i>y(0)</i> in equation 3. Then, one step of numeric integration is performed using equation 2.
<i>y'</i> is incremented by <i>y''dt</i>, where <i>dt</i> is a very small input step. Then, <i>y'</i> is used to increment <i>y</i> in equation 3 the same way.
Once <i>y'</i> and <i>y</i> are incremented, their values are plugged into equation 1 again. This process continues until <i>T</i> is reached.
<br><br>
Thus, a function for <i>y(T)</i>, the solution to the differential equation, can be determined. It is not algebraically defined, but running the numeric algorithm for
any <i>T</i> value that needs to be found gives a close approximation. This web application evaluates the function over a range of values to generate a graph.
The closer the timestep is to 0, the more accurate the approximation becomes.
