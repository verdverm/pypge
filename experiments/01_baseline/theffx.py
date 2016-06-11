from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

import ffx

import data as DATA



def run_explicit_loop():
	for problem in DATA.explicit_problems:
		prob,target = problem.split(";")
		df = DATA.read_datafile("explicit", prob)

		cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
		ins = df[cols].as_matrix()
		outs = df[target].values    

		print("\n\n", prob, target, ins.shape, outs.shape, "\n=======================\n")


		models = ffx.run(ins,outs, ins,outs, cols)
		for model in models:
			print_model(model.complexity(), model, ins, outs)


	for problem in DATA.diffeq_problems:
		prob,target = problem.split(";")
		df = DATA.read_datafile("diffeq", prob)

		cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
		ins = df[cols].as_matrix()
		outs = df[target].values    

		print("\n\n", prob, target, ins.shape, outs.shape, "\n=======================\n")


		models = ffx.run(ins,outs, ins,outs, cols)
		for model in models:
			print_model(model.complexity(), model, ins, outs)




def print_model(size, regr, ins, outs):
	print("  ",size, "  ", regr,"\n--------------")
	# The coefficients
	# print('   Coefficients: ', regr.intercept_, regr.coef_)
	# The mean square error
	yhat = regr.simulate(ins)
	print("   Residual:     %g" % np.mean((yhat - outs) ** 2))
	# Explained variance score: 1 is perfect prediction
	r2 = r2_score(outs, yhat)
	print('   R2:           %g' % r2)
	print()



run_explicit_loop()
