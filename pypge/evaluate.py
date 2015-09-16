from __future__ import division

import sympy

from lmfit import minimize, Parameters

from sklearn.metrics import mean_squared_error


def Fit(model, xs, X_train, Y_train):
	expr = model.expr

	def fcn2min(params, x_train, y_train):

		c_sub = [ (str(c), params[str(c)].value) for c in model.cs ]
		evlr = expr.subs(c_sub)

		# print evlr

		f = sympy.lambdify(xs, evlr, "numpy")
		y_pred = f(x_train)

		return y_pred - y_train

	result = None
	try:
		result = minimize(fcn2min, model.params, args=(X_train,Y_train))
	except Exception, e:
		model.error = "error"

	model.fit_result = result

	if model.error == "error":
		model.error = "numeric error during fitting"
	elif not result.success:
		model.error = "Error fitting: " + str(result.ier) + "  " + result.message


def Eval(model, xs, X_input):
	c_sub = [ (str(c), model.params[str(c)].value) for c in model.cs ]
	evlr = model.expr.subs(c_sub)

	f = sympy.lambdify(xs, evlr, "numpy")
	y_pred = f(X_input)
	return y_pred

def Score(y_true, y_pred):
	try:
		result = mean_squared_error(y_true, y_pred)
		return (result, None)
	except Exception, e:
		return (-1, "error: " + str(e))





##  KEEP BELOW HERE AS AN EXAMPLE   ##
##  ALSO FOR THE MIN/MAX ON PARAMS  ##
##  WANT TO EMULATE THE SHIFT FOR TRIG

# from lmfit import minimize, Parameters, report_fit
# import numpy as np

# # create data to be fitted
# x = np.linspace(0, 15, 301)
# data = (5. * np.sin(2 * x - 0.1) * np.exp(-x*x*0.025) +
#         np.random.normal(size=len(x), scale=0.2) )

# # define objective function: returns the array to be minimized
# def fcn2min(params, x, data):
#     """ model decaying sine wave, subtract data"""
#     amp = params['amp'].value
#     shift = params['shift'].value
#     omega = params['omega'].value
#     decay = params['decay'].value

#     model = amp * np.sin(x * omega + shift) * np.exp(-x*x*decay)
#     return model - data

# # create a set of Parameters
# params = Parameters()
# params.add('amp',   value= 10,  min=0)
# params.add('decay', value= 0.1)
# params.add('shift', value= 0.0, min=-np.pi/2., max=np.pi/2)
# params.add('omega', value= 3.0)


# # do fit, here with leastsq model
# result = minimize(fcn2min, params, args=(x, data))

# # calculate final result
# final = data + result.residual

# # write error report
# report_fit(params)

# # try to plot results
# try:
#     import pylab
#     pylab.plot(x, data, 'k+')
#     pylab.plot(x, final, 'r')
#     pylab.show()
# except:
#     pass
