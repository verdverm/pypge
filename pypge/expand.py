from __future__ import division

import sympy
sympy.init_printing(use_unicode=True)

from itertools import combinations, combinations_with_replacement as combos

import filters
import model

BASIC_BASE = (sympy.exp, sympy.cos, sympy.sin)
BASIC_MISC = (sympy.Abs, sympy.sqrt, sympy.log, sympy.exp)
BASIC_TRIG = (sympy.cos, sympy.sin, sympy.tan)
HYPER_TRIG = (sympy.cosh, sympy.sinh, sympy.tanh)

C = sympy.symbols('C')


class Grower:

	def __init__(self,xs, funcs):
	
		# if only one variable, turn into list
		if type(xs) is sympy.Symbol:
			xs = [xs]
	
		self.xs = xs
		self.funcs = funcs

		self.solo_xs = [ x**p for p in [-2,-1,1,2] for x in xs]
		self.solo_muls = [ C * x for x in xs ]
		self.double_muls = [ C * tpl[0] * tpl[1] for tpl in combos(xs, 2)]
		self.triple_muls = [ C * tpl[0] * tpl[1] * tpl[2] for tpl in combos(xs, 3)]
		
		self.noc_funcs = []
		self.lin_funcs = []
		self.nonlin_funcs = []
		if funcs is not None:
			self.noc_funcs = [ f(x) for f in funcs for x in xs]
			self.lin_funcs = [ C*f(x) for f in funcs for x in xs]
			self.nonlin_funcs = [ C*f(C*x+C) for f in funcs for x in xs]

		## these are the same as above, minus the C
		self.var_sub_xs = [ tpl[0] * tpl[1] for tpl in combos(xs, 2) ]
		self.var_sub_fs = []
		if funcs is not None:
			self.var_sub_fs = [ f(x) for f in funcs for x in xs ]

		self.var_sub_terms   = self.var_sub_xs + self.var_sub_fs
		self.add_extnd_terms = self.solo_muls + self.double_muls + self.lin_funcs
		self.mul_extnd_terms = self.solo_xs + self.noc_funcs


	def first_exprs(self):

		mul_exprs = self.double_muls
		if len(self.xs) < 3:
			mul_exprs += self.triple_muls
		func_exprs = self.lin_funcs

		mid_exprs = self.solo_muls + mul_exprs + func_exprs
		add_exprs = [ sympy.Add( tpl[0], tpl[1], evaluate=False ) for tpl in combinations(mid_exprs, 2)]
		plus_C_exprs = [ sympy.Add( expr, C ) for expr in mid_exprs + add_exprs]

		ret_exprs = mid_exprs + add_exprs + plus_C_exprs

		models = [model.Model(e, xs=self.xs) for e in ret_exprs]
		for m in models:
			m.gen_relation = "first_gen"
			m.parent_id = -1

		return models


	def grow(self, M):
		var_expands = self._var_sub(M.orig)
		add_expands = self._add_extend(M.orig)
		mul_expands = self._mul_extend(M.orig)

		var_models = [model.Model(e, p_id=M.id, reln="var_xpnd") for e in var_expands if e != C]
		add_models = [model.Model(e, p_id=M.id, reln="add_xpnd") for e in add_expands if e != C]
		mul_models = [model.Model(e, p_id=M.id, reln="mul_xpnd") for e in mul_expands if e != C]

		models = var_models + add_models + mul_models
		return models


	def _var_sub(self, expr, limit_sub=False):
		vsubs = []
		# only worry about non-atoms, cause we have to replace args
		if not expr.is_Atom:
			# make a list of args to this non-atom
			# each member of the list is the original expr's args with one substitution made
			args_sets = []
			for i,e in enumerate(expr.args):
				# if the current arg is also a non-atom, recurse
				if not e.is_Atom:
					lim_sub = limit_sub or not (e.is_Add or e.is_Mul)
					# for each expr returned, we need to clone the current args
					# and make the substitution, sorta like flattening?
					ee = self._var_sub(e, lim_sub)
					if len(ee) > 0:
						# We made a substitution(s) on a variable down this branch!!
						for vs in ee:
							# clone current args
							cloned_args = list(expr.args)
							# replace this term in each
							cloned_args[i] = vs
							# append to the args_sets
							args_sets.append(cloned_args)

				elif e in self.xs:
					## Lets make a variable substitution !!
					# loop over self.var_sub_terms
					sub_terms = self.var_sub_terms
					if limit_sub:
						sub_terms = self.var_sub_xs
					for vs in sub_terms:
						# clone current args
						cloned_args = list(expr.args)
						# replace this term in each
						cloned_args[i] = vs
						# append to the args_sets
						args_sets.append(cloned_args)
				else:
					# we don't have to do anything, probably?
					pass

			# finally, create all of the clones at the current level of recursion
			for args in args_sets:
				args = tuple(args)
				tmp = expr.func(*args)
				vsubs.append(tmp)

		return vsubs

		# if e.is_Symbol and e in self.xs:
		

	def _add_extend(self, expr):
		vsubs = []
		# only worry about non-atoms, cause we extend args
		if not expr.is_Atom:
			args_sets = []
			# however we have 2 cases here (as opposed to _var_sub)
			# 1. extend this expression if it's an Add
			if expr.is_Add:
				for term in self.add_extnd_terms:
					# has_match skips extending an add with a term that is already present 
					has_match = False
					for e in expr.args:
						if e == term:
							has_match = True
							break
					if has_match:
						continue
					
					cloned_args = list(expr.args)
					cloned_args.append(term)
					args_sets.append(cloned_args)

			# 2. do the recursion
			for i,e in enumerate(expr.args):
				if not e.is_Atom:
					ee = self._add_extend(e)
					if len(ee) > 0:
						# We made a substitution(s) on a variable down this branch!!
						for vs in ee:
							# clone current args
							cloned_args = list(expr.args)
							# replace this term in each
							cloned_args[i] = vs
							# append to the args_sets
							args_sets.append(cloned_args)


			# finally, create all of the clones at the current level of recursion
			for args in args_sets:
				args = tuple(args)
				tmp = expr.func(*args)
				vsubs.append(tmp)

		return vsubs

	def _mul_extend(self, expr):
		vsubs = []
		# only worry about non-atoms, cause we extend args
		if not expr.is_Atom:
			args_sets = []
			# however we have 2 cases here (as opposed to _var_sub)
			# 1. extend this expression if it's an Add
			if expr.is_Mul:
				for term in self.mul_extnd_terms:
					cloned_args = list(expr.args)
					cloned_args.append(term)
					args_sets.append(cloned_args)

			# 2. do the recursion
			for i,e in enumerate(expr.args):
				if not e.is_Atom:
					ee = self._mul_extend(e)
					if len(ee) > 0:
						# We made a substitution(s) on a variable down this branch!!
						for vs in ee:
							# clone current args
							cloned_args = list(expr.args)
							# replace this term in each
							cloned_args[i] = vs
							# append to the args_sets
							args_sets.append(cloned_args)


			# finally, create all of the clones at the current level of recursion
			for args in args_sets:
				args = tuple(args)
				tmp = expr.func(*args)
				vsubs.append(tmp)

		return vsubs





