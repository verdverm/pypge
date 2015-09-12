from __future__ import division

from sympy import *
init_printing(use_unicode=True)

import numpy as np
np.random.seed(23)

from evaluate import Eval, Score

x, w = symbols('x w')

F_1 = 1.5 * x**2 - x**3
F_2 = exp(Abs(x)) * sin(x)
F_3 = x**2 * exp(sin(x)) + x + sin(pi/4.0 - x**3)

F_1_X = np.linspace(-5., 5., num=200)
F_2_X = np.linspace(-3., 3., num=200)
F_3_X = np.linspace(-10., 10., num=200)

F_1_Y_pure = Eval(x,F_1,F_1_X)
F_2_Y_pure = Eval(x,F_2,F_2_X)
F_3_Y_pure = Eval(x,F_3,F_3_X)

F_1_Y = F_1_Y_pure + np.random.normal(0, 0.05, 200)
F_2_Y = F_2_Y_pure + np.random.normal(0, 0.05, 200)
F_3_Y = F_3_Y_pure + np.random.normal(0, 0.05, 200)

S_1 = Score(F_1_Y_pure,F_1_Y)
S_2 = Score(F_2_Y_pure,F_2_Y)
S_3 = Score(F_3_Y_pure,F_3_Y)

# print S_1, F_1
# print S_2, F_2
# print S_3, F_3

# C = symbols('C')
# F = 1.5 * x**2 - x**3

# xs = symbols('x y z')

# if x in xs:
# 	print "found x"
# else:
# 	print "no x..."

# print dir(C), "\n\n"

# import memoize
# memo = memoize.Memoizer([x,w])

# import expand
# bases = expand.GenBases("x",2,expand.BASIC_TRIG)

# for i,e in enumerate(bases):
# 	# if i > 3:
# 	# 	break

# 	iis, ffs = memo.encode(e)
# 	# print i,e,iis
# 	r1 = memo.lookup_encoded(iis)
# 	r2 = memo.insert_encoded(iis)
# 	r3 = memo.lookup_encoded(iis)
# 	print i, "  ",r1,r2,r3,"\n"


