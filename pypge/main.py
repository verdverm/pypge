from __future__ import division

from sympy import *
init_printing(use_unicode=True)

import numpy as np

from evaluate import Eval, Score

def main():
	print "hello pypge!\n"

	VARS = symbols('x y')

	# print VARS

	expr = VARS[0] * VARS[1]
	# print expr

	# print x == VARS[0]


	xs = np.arange(10.)
	ys = np.arange(10.)
	X,Y = np.meshgrid(xs,ys)
	pts = (X,Y)
	# print pts

	result = Eval(VARS,expr,pts)
	# print result

main()