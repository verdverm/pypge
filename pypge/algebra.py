from __future__ import division

from sympy import *
from sympy.strategies.tree import greedy, brute
init_printing(use_unicode=True)

## Filters on expressions
##
## TODO turn this into a filter which takes a list of functions

def filter_expr_list(expr_list, filters):
	ret = []
	for expr in expr_list:
		if not filter_expr(expr, filters):
			ret.append(expr)
	return ret

def filter_expr(expr, filters):
	for e in preorder_traversal(expr):
		for f in filters:
			if f(e):
				return True
	return False

def filter_has_int_coeff(expr):
	if expr.is_Mul:
			cs, _ = expr.as_coeff_Mul()
			# print "   ** ", cs, cs == numbers.One, type(cs)
			if type(cs) != numbers.One:
				return True
	if expr.is_Add:
		cs, _ = expr.as_coeff_Add()
		# print "   ++ ", cs, cs == numbers.Zero, type(cs)
		if type(cs) != numbers.Zero:
			return True
	return False

def filter_has_big_pow(expr,big=6):
	if expr.is_Pow:
		B,E = expr.as_base_exp()
		if abs(E) > big:
			return True
	return False

default_filters = [filter_has_int_coeff,filter_has_big_pow]



# Code below here was pulled from another project

def tree_size(eq):
	i = 0
	for e in preorder_traversal(eq):
		if e.is_Pow:
			B,E = e.as_base_exp()
			i += abs(E) # cause it's going to be counted when it's 'e' itself
		i+=1
	return i

funcs = [simplify, expand, factor, fu, powsimp, sqrtdenest]
# objective = lambda x: len(str(x))
# megasimp = greedy((funcs, funcs), objective)
megasimp = greedy((funcs, funcs), tree_size)

def do_simp(expr, method):

	# do some simplification
	# 'switch' on submethods or loop
	if method == "simplify":
		simp = simplify(expr)

	elif method == "expand":
		simp = expand(expr)
	elif method == "factor":
		simp = factor(expr)
	elif method == "collect":
		simp = collect(expr)
	elif method == "cancel":
		simp = cancel(expr)


	elif method == "rcollect":
		simp = rcollect(expr)

	elif method == "separatevars":
		simp = separatevars(expr)

	elif method == "apart":
		simp = apart(expr)


	elif method == "ratsimp":
		simp = ratsimp(expr)
	elif method == "radsimp":
		simp = radsimp(expr)


	elif method == "signsimp":
		simp = signsimp(expr)
	elif method == "trigsimp":
		simp = trigsimp(expr)
	elif method == "expand_trig":
		simp = expand_trig(expr)



	elif method == "powsimp":
		simp = powsimp(expr)
	elif method == "powdenest":
		simp = powdenest(expr)

	elif method == "logcombine":
		simp = logcombine(expr)


	# There is a REWRITE function
	# for rewriting one funciton in terms of another
	# tan(x).rewrite(sin) -> (2*sin^2(x)) / (sin(2*x))


	elif method == "expand_mul":
		simp = expand_mul(expr)
	elif method == "expand_func":
		simp = expand_func(expr)
	elif method == "expand_log":
		simp = expand_func(expr)
	elif method == "expand_multinomial":
		simp = expand_multinomial(expr)
	elif method == "expand_power_base":
		simp = expand_power_base(expr)
	elif method == "expand_power_exp":
		simp = expand_power_exp(expr)

	elif method == "fu":
		simp = fu(expr)



	elif method == "megasimp":
		simp = megasimp(expr)
	elif method == "list":
		for f in funcs:
			simp = f(expr)
	elif method == "all":
		for f in funcs:
			simp = f(expr)
			simp = megasimp(expr)
	else:
		simp = simplify(expr)

