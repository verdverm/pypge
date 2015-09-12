from __future__ import division

import sympy

import lmfit

from sklearn.metrics import mean_squared_error


def Fit(xs, cs, expr, points):
	pass

def Eval(xs, expr, points):
	f = sympy.lambdify(xs, expr, "numpy")
	r = f(points)
	return r

def Score(y_true, y_pred):
	return mean_squared_error(y_true, y_pred)