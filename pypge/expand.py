from __future__ import division

from sympy import *
init_printing(use_unicode=True)

from itertools import combinations, combinations_with_replacement as combos


BASIC_MISC = (Abs, sqrt, log, exp)
BASIC_TRIG = (cos, sin, tan)
HYPER_TRIG = (cosh, sinh, tanh)


def GenBases(xs_str, max_combo, funcs):
	# xs_str = " ".join(["x_" + str(x) for x in range(num_xs)])

	C = symbols('C')
	xs = symbols(xs_str)

	# if only one variable, turn into list
	if type(xs) is Symbol:
		xs = [xs]

	solo_exprs = [ C * x for x in xs ]
	mul_exprs = [ C * tpl[0] * tpl[1] for tpl in combos(xs, 2)]

	func_exprs = []
	if funcs is not None:
		func_exprs = [ C*f(x) for f in funcs for x in xs]

	mid_exprs = solo_exprs + mul_exprs + func_exprs

	add_exprs = [ Add( tpl[0], tpl[1], evaluate=False ) for tpl in combinations(mid_exprs, 2)]

	plus_C_exprs = [ Add( expr, C ) for expr in mid_exprs + add_exprs]

	ret_exprs = [C] + mid_exprs + add_exprs + plus_C_exprs

	return ret_exprs



def gen_basic_trig(xs):
	return [ C*f(x) for f in BASIC_TRIG for x in xs]

def gen_basic_trig_nonlin(xs):
	return [ C*f(C*x + C) for f in BASIC_TRIG for x in xs]


# num_xs = 3
# xs_str = " ".join(["x_" + str(x) for x in range(num_xs)])
# xs = symbols(xs_str)
# # print xs

# ts = gen_basic_trig(xs)
# ts_nl = gen_basic_trig_nonlin(xs)
# fxs = ts + ts_nl
# print fxs

# import sys
# sys.exit()

# add_exprs = [ C*tpl[0] + C*tpl[1] for tpl in combos(xs, 2)]
# mul_exprs = [ C * tpl[0] * tpl[1] for tpl in combos(xs, 2)]


# print "add bases:"
# for i, expr in enumerate(add_exprs):
# 	print i, expr

# print "mul bases:"
# for i, expr in enumerate(mul_exprs):
# 	print i, expr


# these should be rewritten via tree recursion on abstract 'C'
# num_cs = 3
# cs_str = " ".join(["c_" + str(c) for c in range(num_cs)])
# cs = symbols(cs_str)
# print cs

