#!/usr/bin/env python
"""
Program to plot the motion of a "springy pendulum".

(kindly taken from: http://julianoliver.com/share/free-science-books/comp-phys-python.pdf [page 102-103])

We actually have FOUR parameters to track, here:
L, L dot, theta, and theta dot.
So instead of the usual Nx2 array, make it Nx4.
Each 4-element row will be used for the state of
the system at one instant, and each instant is
separated by time dt. I'll use the order given above.
"""

import numpy as np
import scipy
from scipy.integrate import odeint

## Nx4
N = 1000 # number of steps to take
y = np.zeros([4])

Lo = 1.0 # unstretched spring length
L  = 1.0 # Initial stretch of spring
vo = 0.0 # initial velocity
thetao = 0.3 # radians
omegao = 0.0 # initial angular velocity

y[0] = L # set initial state
y[1] = vo
y[2] = thetao
y[3] = omegao
time = np.linspace(0, 25, N)

k = 3.5 # spring constant, in N/m
m = 0.2 # mass, in kg
gravity = 9.8 # g, in m/s^2

def springpendulum(y, time):
	"""
	This defines the set of differential equations
	we are solving. Note that there are more than
	just the usual two derivatives!
	"""
	g0 = y[1]
	g1 = (Lo+y[0])*y[3]*y[3] - k/m*y[0] + gravity*np.cos(y[2])
	g2 = y[3]
	g3 = -(gravity*np.sin(y[2]) + 2.0*y[1]*y[3]) / (Lo + y[0])
	return np.array([g0,g1,g2,g3])


# Now we do the calculations.
answer = scipy.integrate.odeint(springpendulum, y, time)

# Now graph the results.
# rather than graph in terms of t, I'm going
# to graph the track the mass takes in 2D.
# This will require that I change L,theta data
# to x,y data.
xdata =  (Lo + answer[:,0])*np.sin(answer[:,2])
ydata = -(Lo + answer[:,0])*np.cos(answer[:,2])

import os

if os.getenv("TRAVIS", "false") != "true":
	import matplotlib.pyplot as plt

	plt.plot(xdata, ydata, 'r-')
	plt.xlabel("Horizontal position")
	plt.ylabel("Vertical position")

	# plt.show()

