from sympy import preorder_traversal, numbers

## Filters on expressions
##
## TODO turn this into a filter which takes a list of functions

def filter_models(models, filters):
	ret = []
	for modl in models:
		if not filter_model(modl, filters):
			ret.append(modl)
	return ret

def filter_model(expr, filters):
	for e in preorder_traversal(expr):
		for f in filters:
			if f(e):
				return True
	return False


def filter_has_int_coeff(modl):
	expr = modl.orig
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

def filter_has_big_pow(modl,big=6):
	expr = modl.orig
	if expr.is_Pow:
		B,E = expr.as_base_exp()
		if abs(E) > big:
			return True
	return False

default_filters = [filter_has_int_coeff,filter_has_big_pow]

