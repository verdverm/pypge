from __future__ import division

from sympy import *
init_printing(use_unicode=True)

from itertools import combinations_with_replacement as combos

C = symbols('C')

num_xs = 3
xs_str = " ".join(["x_" + str(x) for x in range(num_xs)])
xs = symbols(xs_str)
# print xs

add_exprs = [ C*tpl[0] + C*tpl[1] for tpl in combos(xs, 2)]
mul_exprs = [ C * tpl[0] * tpl[1] for tpl in combos(xs, 2)]

print "add bases:"
for i, expr in enumerate(add_exprs):
	print i, expr

print "mul bases:"
for i, expr in enumerate(mul_exprs):
	print i, expr



# these should be rewritten via tree recursion on abstract 'C'
# num_cs = 3
# cs_str = " ".join(["c_" + str(c) for c in range(num_cs)])
# cs = symbols(cs_str)
# print cs

