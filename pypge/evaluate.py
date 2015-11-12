from __future__ import print_function
from __future__ import division

import sympy
import numpy as np

from lmfit import minimize, Parameters, fit_report
from sklearn import metrics


def Fit(modl, xs, X_train, Y_train, MAXFEV=100):
	expr = modl.expr
	ONES = np.ones(len(Y_train))

	def fcn2min(params, x_train, y_train):
		modl.params = params
		y_pred = Eval(modl, xs, x_train)
		return y_pred - y_train

	def dfunc(params, x_train, y_train):
		try:
			modl.params = params
			y_pred = []
			for i, jeqn in enumerate(modl.jac):

				if jeqn is sympy.numbers.One or jeqn == 1:
					y_pred.append(ONES)
				
				elif jeqn in modl.cs:
					# print("JUST A COEFF", len(ONES), params)
					pval = params[str(modl.cs[i])].value
					ys=np.empty(len(ONES))
					ys.fill(pval)
					y_pred.append(ys)

				else:
					ys = EvalJac(modl, jeqn, xs, x_train)
					y_pred.append(ys)

			ret = np.array(y_pred)
			return ret
		except Exception as e:
			print("dfunc error: ", e, type(e), e.args)


	result = None
	try:
		result = minimize(fcn2min, modl.params, args=(X_train,Y_train), Dfun=dfunc, col_deriv=1, maxfev=MAXFEV)
		# print(fit_report(result))

	except Exception as e:
		modl.exception = str(e)
		modl.error = "error"
		# print("ERROR HERE: ", e, type(e), modl.id, modl.expr, modl.jac)

	modl.fit_result = result

	# print("GOT HERE...", modl.id, modl.fit_result.success, result.ier)
	# print(fit_report(modl.fit_result))

	if modl.error == "error":
		modl.error = "numeric error during fitting"
	elif result.ier is not None and result.ier == 5:
		modl.fit_result.success = True
		# print(fit_report(modl.fit_result))
	elif not result.success:
		modl.error = "Error fitting: " + str(result.ier) + "  " + result.message
		# print("GOT HERE 2: ", modl.error)

	# print("returning: ", modl.id)


def Eval(modl, xs, X_input):
	c_sub = [ (str(c), modl.params[str(c)].value) for c in modl.cs ]
	eqn = modl.expr.subs(c_sub)

	f = sympy.lambdify(xs, eqn, "numpy")
	y_pred = f(*X_input)
	return y_pred

def EvalJac(modl, jac_eqn, xs, X_input):
	c_sub = [ (str(c), modl.params[str(c)].value) for c in modl.cs ]
	eqn = jac_eqn.subs(c_sub)

	f = sympy.lambdify(xs, eqn, "numpy")
	y_pred = f(*X_input)
	return y_pred


def Score(y_true, y_pred, err_metric):
	try:
		if err_metric == "r2":
			result = metrics.r2_score(y_true, y_pred)
		elif err_metric == "evar":
			result = metrics.explained_variance_score(y_true, y_pred)

		elif err_metric == "mae":
			result = metrics.mean_absolute_error(y_true, y_pred)
		elif err_metric == "mse":
			result = metrics.mean_squared_error(y_true, y_pred)
		elif err_metric == "rmae":
			result = metrics.mean_absolute_error(y_true, y_pred)
			result = np.sqrt(result)
		elif err_metric == "rmse":
			result = metrics.mean_squared_error(y_true, y_pred)
			result = np.sqrt(result)

		else:
			return (None, "error: unknown error metric")

		return (result, None)
	except Exception as e:
		return (None, "error: " + str(e))





def eval_model(modl, vars, X_train, Y_train, err_method, MAXFEV=100):

	# fit the modl
	Fit(modl, vars, X_train, Y_train, MAXFEV=MAXFEV)
	if modl.error or not modl.fit_result.success:
		modl.error = "errored while fitting: " + modl.error
		modl.errored = True
		return False
	
	# score the modl
	y_pred = Eval(modl, vars, X_train)

	modl.score, err = Score(Y_train, y_pred, err_method)
	if err is not None:
		modl.error = "errored while scoring: " + modl.error
		modl.errored = True
		return False
	
	modl.r2, err = Score(Y_train, y_pred, "r2")
	if err is not None:
		modl.error = "errored while r2'n: " + modl.error
		modl.errored = True
		return False
	
	modl.evar, err = Score(Y_train, y_pred, "evar")
	if err is not None:
		modl.error = "errored while evar'n: " + modl.error
		modl.errored = True
		return False


	modl.aic = modl.fit_result.aic
	modl.bic = modl.fit_result.bic
	modl.chisqr = modl.fit_result.chisqr
	modl.redchi = modl.fit_result.redchi

	# modl.evaluated = True

	return True # passed

