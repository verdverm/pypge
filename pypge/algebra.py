import sympy
from sympy.strategies.tree import greedy, brute
sympy.init_printing(use_unicode=True)

import model

#### Code below here was pulled from another project

def tree_size(eq):
	i = 0
	for e in sympy.preorder_traversal(self.expr):
		if e.is_Integer:
			i += int(abs(e))
			continue
		i+=1
	return i

# funcs = [sympy.simplify, sympy.expand, sympy.factor, sympy.fu, sympy.powsimp, sympy.sqrtdenest]
# objective = lambda x: len(str(x))

# https://github.com/sympy/sympy/blob/master/sympy/strategies/tree.py
# megasimp = greedy((funcs, funcs), objective)
# megasimp = greedy((funcs, funcs), tree_size)


def manip_model(modl, method):
	expr, err = do_simp(modl.expr, method)
	if err is not None:
		return None, err
	if expr is None:
		print "NONE: ", modl.expr, method, " to None"
		print "  shouldn't get here [ algebra.manip_model() ]"
		return None, None

	if expr == modl.expr:
		return None, "same"

	ret_modl = model.Model(expr, xs=modl.xs, cs=modl.cs)
	return ret_modl, None


def do_simp(expr, method):
	### Module Reference
	### http://docs.sympy.org/latest/modules/simplify/simplify.html

	if method == "simplify":
		simp = sympy.simplify(expr)
	elif method == "expand":
		simp = sympy.expand(expr)
	elif method == "factor":
		simp = sympy.factor(expr)
	else:
		return None, "unknown method"
	return simp, None


	### The goto intelligent simplify function
	#  http://docs.sympy.org/latest/tutorial/simplification.html#simplify
	# if method == "simplify":
	# 	simp = sympy.simplify(expr)


	### Polynomial/Rational Function Manipulations
	#  http://docs.sympy.org/latest/tutorial/simplification.html#polynomial-rational-function-simplification
	# elif method == "expand":
	# 	simp = sympy.expand(expr)
	# elif method == "factor":
	# 	simp = sympy.factor(expr)
	# elif method == "collect":
	# 	simp = sympy.collect(expr)
	# elif method == "cancel":
	# 	simp = sympy.cancel(expr)
	# elif method == "apart":
	# 	simp = sympy.apart(expr)


	### Triginomic Manipulatiosn
	# http://docs.sympy.org/latest/tutorial/simplification.html#trigonometric-simplification
	# elif method == "trigsimp":
	# 	simp = sympy.trigsimp(expr)
	# elif method == "expand_trig":
	# 	simp = sympy.expand_trig(expr)


	### Powers manipulations
	# http://docs.sympy.org/latest/tutorial/simplification.html#powers
	# elif method == "powsimp":
	# 	simp = sympy.powsimp(expr)
	# elif method == "expand_power_base":
	# 	simp = sympy.expand_power_base(expr)
	# elif method == "expand_power_exp":
	# 	simp = sympy.expand_power_exp(expr)
	# elif method == "powdenest":
	# 	simp = sympy.powdenest(expr)


	### Exponentials and Logarithms
	# elif method == "expand_log":
	# 	simp = sympy.expand_func(expr)
	# elif method == "logcombine":
	# 	simp = sympy.logcombine(expr)



	# elif method == "rcollect":
	# 	simp = sympy.rcollect(expr)

	# elif method == "separatevars":
	# 	simp = sympy.separatevars(expr)




	# elif method == "ratsimp":
	# 	simp = sympy.ratsimp(expr)
	# elif method == "radsimp":
	# 	simp = sympy.radsimp(expr)


	# elif method == "signsimp":
	# 	simp = sympy.signsimp(expr)




	# There is a REWRITE function
	# for rewriting one funciton in terms of another
	# tan(x).rewrite(sin) -> (2*sin^2(x)) / (sin(2*x))


	# elif method == "expand_mul":
	# 	simp = sympy.expand_mul(expr)
	# elif method == "expand_func":
	# 	simp = sympy.expand_func(expr)
	# elif method == "expand_multinomial":
	# 	simp = sympy.expand_multinomial(expr)

	# elif method == "fu":
	# 	simp = sympy.fu(expr)

	# # these are meta or aggrigate
	# elif method == "megasimp":
	# 	simp = megasimp(expr)
	# elif method == "list":
	# 	for f in funcs:
	# 		simp = f(expr)
	# elif method == "all":
	# 	for f in funcs:
	# 		simp = f(expr)
	# 		simp = megasimp(expr)

