from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

from sklearn import svm

import data as DATA



def run_explicit_loop():
	for problem in DATA.explicit_problems:
		prob,target = problem.split(";")
		df = DATA.read_datafile("explicit", prob)

		cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
		ins = df[cols].as_matrix()
		outs = df[target].values    

		print("\n\n", prob, target, ins.shape, outs.shape, "\n=======================\n")


		svr_rbf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)

		svr_rbf.fit(ins,outs)
		print_model("svr - rbf", svr_rbf, ins,outs)

	for problem in DATA.diffeq_problems:
		prob,target = problem.split(";")
		df = DATA.read_datafile("diffeq", prob)

		cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
		ins = df[cols].as_matrix()
		outs = df[target].values    

		print("\n\n", prob, target, ins.shape, outs.shape, "\n=======================\n")


		svr_rbf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)

		svr_rbf.fit(ins,outs)
		print_model("svr - rbf", svr_rbf, ins,outs)




		# svr_lin = svm.SVR(kernel='linear', C=1e3)
		# svr_poly2 = svm.SVR(kernel='poly', C=1e3, degree=2)
		# svr_poly3 = svm.SVR(kernel='poly', C=1e3, degree=2)

		# svr_lin.fit(ins,outs)
		# print_model("svr - linear", svr_lin, ins,outs)

		# svr_poly2.fit(ins,outs)
		# print_model("svr - poly 2", svr_poly2, ins,outs)
		
		# svr_poly3.fit(ins,outs)
		# print_model("svr - poly 3", svr_poly3, ins,outs)



def print_model(name, regr, ins, outs):
	print("  ",name,"\n--------------")

	# The mean square error
	yhat = regr.predict(ins)
	print("   Residual:     %g" % np.mean((yhat - outs) ** 2))
	# Explained variance score: 1 is perfect prediction
	r2 = r2_score(outs, yhat)
	print('   R2:           %g' % r2)
	print()



run_explicit_loop()
