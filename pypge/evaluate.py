from __future__ import division

import sympy

from sklearn.metrics import mean_squared_error

def Eval(vs, expr, points):
	f = sympy.lambdify(vs, expr, "numpy")
	r = f(points)
	return r

def Score(y_true, y_pred):
	return mean_squared_error(y_true, y_pred)