from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

import data as DATA



def run_explicit_loop():
	for problem in DATA.explicit_problems:
		prob,target = problem.split(";")
		df = DATA.read_datafile("explicit", prob)

		print("\n\n", prob, target, df.shape,"\n=======================\n")


		cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
		ins = df[cols].as_matrix()
		outs = df[target].values    

		theline_model(ins,outs)
		elastic_model(ins,outs,0.1,0.7)
		

	for problem in DATA.diffeq_problems:
		prob,target = problem.split(";")
		df = DATA.read_datafile("diffeq", prob)

		print("\n\n", prob, target, df.shape,"\n=======================\n")


		cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
		ins = df[cols].as_matrix()
		outs = df[target].values    

		theline_model(ins,outs)
		elastic_model(ins,outs,0.1,0.7)
		






def print_model(name, regr, ins, outs):
	print("  ",name,"\n--------------")
	# The coefficients
	print('   Coefficients: ', regr.intercept_, regr.coef_)

	# The mean square error
	yhat = regr.predict(ins)
	print("   Residual:     %g" % np.mean((yhat - outs) ** 2))
	# Explained variance score: 1 is perfect prediction
	r2 = r2_score(outs, yhat)
	print('   R2:           %g' % r2)
	print()


def theline_model(ins,outs):
	regr = linear_model.LinearRegression()
	regr.fit(ins, outs)
	print_model("theline", regr, ins, outs)


def ridge_model(ins,outs, alpha):
	regr = linear_model.Ridge(alpha = alpha)
	regr.fit(ins, outs)
	print_model("ridge", regr, ins, outs)

def lasso_model(ins,outs, alpha):
	regr = linear_model.Lasso(alpha = alpha)
	regr.fit(ins, outs)
	print_model("lasso", regr, ins, outs)

def elastic_model(ins,outs,alpha,l1_ratio):
	regr = linear_model.ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
	regr.fit(ins, outs)
	print_model("elastic", regr, ins, outs)

def poly_model(ins,outs,degrees):
	poly   = PolynomialFeatures(degree=degrees)
	X = poly.fit_transform(ins)

	regr = linear_model.LinearRegression()
	regr.fit(X, outs)
	print_model("poly-"+str(degrees), regr, X, outs)


run_explicit_loop()
