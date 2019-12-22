
# ODE-Calculator

### ODE Grapher Web App using Flask
Check it out online [here](http://odecalculator.pythonanywhere.com)

### How it works
This is a way to graph any Ordinary Differential Equation, based on the code from [3Blue1Brown's video](https://www.youtube.com/watch?v=p_di4Zn4wz4)

Let's say you have the equation
<p style="text-align: center"><img src="https://latex.codecogs.com/svg.latex?y''=-0.5y-4.9sin(y)"></p>
<p style="text-align: right">**(eq 1)**</p>
This is an equation that can be used to model damped pendulum motion over time, where *y* is position, *y'* is velocity, and *y''* is acceleration.
Instead of attempting to use algebraic techniques and theorems to solve the equation (which is near impossible in this case), this program uses numeric integration.
The goal here is to find y as a function of an input variable, which can be denoted *T*. Based on the Fundamental Theorem of Calculus,
<p style="text-align: center"><img src="https://latex.codecogs.com/svg.latex?y(T)=\int_0^Ty'dt&plus;y(0)"></p>
<p style="text-align: right">**(eq 2)**</p>
<p style="text-align: center"><img src="https://latex.codecogs.com/svg.latex?y'(T)=\int_0^Ty''dt&plus;y'(0)"></p>
<p style="text-align: right">**(eq 3)**</p>
Finally, we know the definition of *y''* from equation 1. All of these values are defined in terms of each other, which would seem problematic at first.
However, this issue is solved by starting with *y'(0)* and *y(0)* in equation 3. Then, one step of numeric integration is performed using equation 2.
*y'* is incremented by *y''dt*, where *dt* is a very small time step. Then, *y'* is used to increment *y* in equation 3 the same way.
Once *y'* and *y* are incremented, their values are plugged into equation 1 again. This process continues until *T* is reached.
<br><br>
Thus, a function for *y(T)*, the solution to the differential equation, can be determined. It is not algebraically defined, but running the numeric algorithm for
any *T* value that needs to be found gives a close approximation. This web application evaluates the function over a range of values to generate a graph.
The closer the timestep is to 0, the more accurate the approximation becomes.
