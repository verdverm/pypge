from sympy import preorder_traversal, numbers, Symbol
import sympy

C = Symbol("C")
## Filters on expressions
#
#  Each filter should take both a model and expression
#  So that the API is uniform, but we can access both
#  the model attributes and the (sub)expressions recursively


def filter_models(models, filters):
	ret = []
	for modl in models:
		if not filter_model(modl, modl.orig, filters):
			ret.append(modl)
	return ret

def filter_model(modl, expr, filters):
	for e in preorder_traversal(expr):
		for f in filters:
			if f(modl, e):
				return True
	return False


def filter_just_C(modl,expr):
	if modl.orig is C or modl.orig == C or modl.orig.is_Number:
		return True
	return False

def filter_no_C(modl,expr):
	if len(modl.cs) == 0:
		return True
	return False

def filter_too_big(modl, expr, big=64):
	if modl.size() > big:
		return True
	return False

def filter_has_int_coeff(modl, expr):
	if expr.is_Mul:
			cs, _ = expr.as_coeff_Mul()
			if type(cs) != numbers.One:
				return True
	if expr.is_Add:
		cs, _ = expr.as_coeff_Add()
		if type(cs) != numbers.Zero:
			return True
	return False

def filter_has_big_pow(modl, expr, big=6):
	if expr.is_Pow:
		B,E = expr.as_base_exp()
		if abs(E) > big:
			return True
	return False

def filter_has_coeff_pow(modl, expr):
	if expr.is_Pow:
		B,E = expr.as_base_exp()
		if B is C or B == C or B.is_Number:
			return True
	return False


default_filters = [
	filter_too_big,
	filter_has_int_coeff,
	filter_has_big_pow,
	filter_just_C,
	filter_no_C,
	filter_has_coeff_pow
]
