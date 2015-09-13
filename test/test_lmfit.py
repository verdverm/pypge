from __future__ import division

import sympy
sympy.init_printing(use_unicode=True)

import numpy as np
np.random.seed(23)

from lmfit import minimize, Parameters, report_fit

from sklearn.metrics import mean_squared_error

x = sympy.symbols('x')
xs = [x]
cs = sympy.symbols('C_:4')
my_params = Parameters()
for i,c in enumerate(cs):
	my_params.add('C_'+str(i), value=1.0)


F_1 =   2.0  -   4.2 * x  +   1.5 * x**2  -   3.7 * x**3
f_1 = cs[0]  - cs[1] * x  + cs[2] * x**2  - cs[3] * x**3

F_1_X = np.linspace(-5., 5., num=200)
F_1_Y_pure = sympy.lambdify(x,F_1,"numpy")(F_1_X)
F_1_Y = F_1_Y_pure + np.random.normal(0, 0.05, 200)

S_1 = mean_squared_error(F_1_Y_pure,F_1_Y)

def fit(expr, params, X_train, Y_train):

	def fcn2min(params, x_train, y_train):

		c_sub = [ (str(c), params[str(c)].value) for c in cs ]
		evlr = expr.subs(c_sub)

		# print evlr

		f = sympy.lambdify(xs, evlr, "numpy")
		y_pred = f(x_train)

		return y_pred - y_train

	result = minimize(fcn2min, my_params, args=(X_train,Y_train))
	return result


def test_fit():
	result = fit(f_1,[x],F_1_X,F_1_Y)
	y_pred = F_1_Y + result.residual
	s_1 = mean_squared_error(y_pred,F_1_Y)
	assert s_1 == 0.002412569621973993
