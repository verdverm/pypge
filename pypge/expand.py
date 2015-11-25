from __future__ import print_function
from __future__ import division

import sympy
sympy.init_printing(use_unicode=True)

from itertools import (
	combinations as combos_woutR, 
	combinations_with_replacement as combos_withR
)

from pypge import filters
from pypge import model

BASIC_BASE = [sympy.exp, sympy.cos, sympy.sin]
BASIC_MISC = [sympy.Abs, sympy.sqrt, sympy.log, sympy.exp]
BASIC_TRIG = [sympy.cos, sympy.sin, sympy.tan]
HYPER_TRIG = [sympy.cosh, sympy.sinh, sympy.tanh]

C = sympy.symbols('C')

def map_names_to_funcs(names):
	funcs = []
	for name in names:

		if name == "sqrt":
			func.append(sympy.sqrt)
		elif name == "abs":
			funcs.append(sympy.Abs)
		elif name == "sin":
			funcs.append(sympy.sin)
		elif name == "cos":
			funcs.append(sympy.cos)
		elif name == "tan":
			funcs.append(sympy.tan)
		elif name == "exp":
			funcs.append(sympy.exp)
		elif name == "log":
			funcs.append(sympy.log)
		elif name == "sinh":
			funcs.append(sympy.sinh)
		elif name == "cosh":
			funcs.append(sympy.cosh)
		elif name == "tanh":
			funcs.append(sympy.tanh)

		else:
			raise Exception("Unknown function name: " + name)

	return funcs


class Grower:

	def __init__(self,xs, funcs, **kwargs):
	
		# if only one variable, turn into list
		if type(xs) is sympy.Symbol:
			xs = [xs]
	
		self.xs = xs
		self.funcs = funcs

		# policy configs
		self.func_level = "linear"     # [linear,nonlin]
		self.init_level = "low"     # [low,med,high]
		self.add_xtop = False
		self.shrinker = False
		self.limiting_depth = 4

		# do grow_level this way so we can override the individual ones if we want
		self.grow_level = kwargs.get("grow_level", "low")   # [low,med,high]
		self.subs_level = self.grow_level     				# [low,med,high]
		self.adds_level = self.grow_level               	# [low,med,high]
		self.muls_level = self.grow_level               	# [low,med,high]

				# override with kwargs
		# --------------------
		for key, value in kwargs.items():
			# print (key, value)
			setattr(self, key, value)
		# --------------------

		print("xs: ", self.xs)
		print("funcs: ", self.funcs)
		print("func_lvl:", self.func_level)
		print("init_lvl:", self.init_level)
		print("grow_lvl:", self.grow_level)
		print("subs_lvl:", self.subs_level)
		print("adds_lvl:", self.adds_level)
		print("muls_lvl:", self.muls_level)
		print("add_xtop:", self.add_xtop)
		print("shrinker:", self.shrinker)
		print("limdepth:", self.limiting_depth)

		self.xs_pow1 = [x**(n*(p+1)) for p in range(1) for n in [-1,1] for x in xs]
		self.xs_pow2 = [x**(n*(p+1)) for p in range(2) for n in [-1,1] for x in xs]
		self.xs_pow3 = [x**(n*(p+1)) for p in range(3) for n in [-1,1] for x in xs]
		self.xs_pow4 = [x**(n*(p+1)) for p in range(4) for n in [-1,1] for x in xs]

		# print("xs_pow1:", self.xs_pow1)
		# print("xs_pow2:", self.xs_pow2)
		# print("xs_pow3:", self.xs_pow3)
		# print("xs_pow4:", self.xs_pow4)


		self.wout_c_xs1_muls = [ x for x in self.xs_pow1 ]
		self.wout_c_xs2_muls = [ tpl[0] * tpl[1] for tpl in combos_withR(self.xs_pow1, 2)] + self.wout_c_xs1_muls
		self.wout_c_xs3_muls = [ tpl[0] * tpl[1] * tpl[2] for tpl in combos_withR(self.xs_pow1, 3)] + self.wout_c_xs2_muls
		self.wout_c_xs4_muls = [ tpl[0] * tpl[1] * tpl[2] * tpl[3] for tpl in combos_withR(self.xs_pow1, 4)] + self.wout_c_xs3_muls

		self.wout_c_xs3_muls = self._uniquify(self.wout_c_xs3_muls)

		self.with_c_xs1_muls = [ C * m for m in self.wout_c_xs1_muls ]
		self.with_c_xs2_muls = [ C * m for m in self.wout_c_xs2_muls ]
		self.with_c_xs3_muls = [ C * m for m in self.wout_c_xs3_muls ]
		self.with_c_xs4_muls = [ C * m for m in self.wout_c_xs4_muls ]

		# print("wout_c_xs1_muls", self.wout_c_xs1_muls)
		# print("wout_c_xs2_muls", self.wout_c_xs2_muls)
		# print("wout_c_xs3_muls", self.wout_c_xs3_muls)
		# print("wout_c_xs4_muls", self.wout_c_xs4_muls)
		# print("with_c_xs1_muls", self.with_c_xs1_muls)
		# print("with_c_xs2_muls", self.with_c_xs2_muls)
		# print("with_c_xs3_muls", self.with_c_xs3_muls)
		# print("with_c_xs4_muls", self.with_c_xs4_muls)
		
		self.wout_c_linear_funcs = []
		self.wout_c_nonlin_funcs = []
		self.with_c_linear_funcs = []
		self.with_c_nonlin_funcs = []
		if funcs is not None:
			self.wout_c_linear_funcs = [ f(x) for f in funcs for x in self.wout_c_xs1_muls]
			self.wout_c_nonlin_funcs = [ f(C*x+C) for f in funcs for x in self.wout_c_xs1_muls]
			self.with_c_linear_funcs = [ C*f(x) for f in funcs for x in self.wout_c_xs1_muls]
			self.with_c_nonlin_funcs = [ C*f(C*x+C) for f in funcs for x in self.wout_c_xs1_muls]

		# print("wout_c_linear_funcs", self.wout_c_linear_funcs)
		# print("wout_c_nonlin_funcs", self.wout_c_nonlin_funcs)
		# print("with_c_linear_funcs", self.with_c_linear_funcs)
		# print("with_c_nonlin_funcs", self.with_c_nonlin_funcs)

		self.with_c_func_exprs = []
		self.wout_c_func_exprs = []
		if self.func_level == "linear":
			self.with_c_func_exprs = self.with_c_linear_funcs + [ f**(-1) for f in self.with_c_linear_funcs ]
			self.wout_c_func_exprs = self.wout_c_linear_funcs + [ f**(-1) for f in self.wout_c_linear_funcs ]
		elif self.func_level in ["nonlin", "nonlinear"]:
			self.with_c_func_exprs = self.with_c_nonlin_funcs + [ f**(-1) for f in self.with_c_nonlin_funcs ]
			self.wout_c_func_exprs = self.wout_c_nonlin_funcs + [ f**(-1) for f in self.wout_c_nonlin_funcs ]
		else:
			print("UNKNOWN FUNC_LEVEL!!")
			return

		self.init_var_subs()
		self.init_add_extends()
		self.init_mul_extends()

	def first_exprs(self):
		
		mul_exprs = []
		if self.init_level == "low":
			if len(self.xs) > 3:
				mul_exprs = self.with_c_xs1_muls
			else:
				mul_exprs = self.with_c_xs2_muls
		elif self.init_level == "med":
			if len(self.xs) > 3:
				mul_exprs = self.with_c_xs1_muls + self.with_c_func_exprs
			elif len(self.xs) > 1:
				mul_exprs = self.with_c_xs2_muls + self.with_c_func_exprs
			else:
				mul_exprs = self.with_c_xs3_muls + self.with_c_func_exprs
		elif self.init_level == "high":
			if len(self.xs) > 3:
				mul_exprs = self.with_c_xs2_muls + self.with_c_func_exprs
			elif len(self.xs) > 1:
				mul_exprs = self.with_c_xs3_muls + self.with_c_func_exprs
			else:
				mul_exprs = self.with_c_xs4_muls + self.with_c_func_exprs
		else:
			print("UNKNOWN INIT_LEVEL!!")
			return

		print("mul_exprs: ", len(mul_exprs), mul_exprs)

		mid_exprs = mul_exprs
		print("mid_exprs: ", len(mid_exprs))
		add_exprs = [ tpl[0] + tpl[1] for tpl in combos_woutR(mid_exprs, 2)]
		if self.init_level == "high":
			add_exprs += [ tpl[0] + tpl[1] + tpl[2] for tpl in combos_woutR(mid_exprs, 3)]
		print("add_exprs: ", len(add_exprs))

		exprs_set = mid_exprs + add_exprs + self.with_c_func_exprs
		print("exprs_set: ", len(exprs_set))

		# always add the plus C
		plus_C_exprs = [ sympy.Add( expr, C ) for expr in exprs_set]
		ret_exprs = exprs_set + plus_C_exprs
		print("ret_exprs", len(ret_exprs))

		## UNIQUIFY THE RESULTS
		ret_exprs = self._uniquify(ret_exprs)

		models = [model.Model(e, xs=self.xs) for e in ret_exprs]
		for m in models:
			m.gen_relation = "first_gen"
			m.parent_id = -1

		return models




	def init_var_subs(self):

		add_terms = [ C*x+C for x in self.xs ]


		# DO + SOMETHING ? HERE = (.)(.)
		self.var_sub_dep_lim_terms = self.wout_c_xs2_muls
		self.var_sub_dep_terms = self.var_sub_dep_lim_terms + self.wout_c_func_exprs

		if self.subs_level == "low":
			self.var_sub_lim_terms = self.wout_c_xs2_muls
			self.var_sub_terms = self.var_sub_lim_terms + self.wout_c_func_exprs

		elif self.subs_level == "med":
			self.var_sub_lim_terms = self.wout_c_xs2_muls + add_terms
			self.var_sub_terms = self.var_sub_lim_terms + self.wout_c_func_exprs

		elif self.subs_level == "high":
			self.var_sub_dep_lim_terms += add_terms
			self.var_sub_dep_terms += add_terms
			self.var_sub_lim_terms = self.wout_c_xs3_muls + add_terms
			self.var_sub_terms = self.var_sub_lim_terms + self.wout_c_func_exprs

		else:
			print("UNKNOWN SUBS_LEVEL!!")

		self.var_sub_terms = self._uniquify(self.var_sub_terms)
		self.var_sub_lim_terms = self._uniquify(self.var_sub_lim_terms)


	def init_add_extends(self):

		if self.adds_level == "low":
			self.add_extend_lim_terms = self.with_c_xs1_muls
			self.add_extend_terms = self.with_c_xs1_muls + self.with_c_func_exprs
		elif self.adds_level == "med":
			self.add_extend_lim_terms = self.with_c_xs2_muls
			self.add_extend_terms = self.with_c_xs2_muls + self.with_c_func_exprs
		elif self.adds_level == "high":
			self.add_extend_lim_terms = self.with_c_xs2_muls
			cross = [x*f for f in self.with_c_func_exprs for x in self.with_c_xs1_muls]
			self.add_extend_terms = self.with_c_xs2_muls + self.with_c_func_exprs + cross
		else:
			print("UNKNOWN EXTEND_LEVEL!!")

		self.add_extend_terms = self._uniquify(self.add_extend_terms)
		self.add_extend_lim_terms = self._uniquify(self.add_extend_lim_terms)

	def init_mul_extends(self):

		if self.muls_level == "low":
			self.mul_extend_lim_terms = self.wout_c_xs1_muls
			self.mul_extend_terms = self.wout_c_xs1_muls + self.wout_c_func_exprs
		elif self.muls_level == "med":
			self.mul_extend_lim_terms = self.wout_c_xs2_muls
			self.mul_extend_terms = self.wout_c_xs2_muls + self.wout_c_func_exprs
		elif self.muls_level == "high":
			self.mul_extend_lim_terms = self.wout_c_xs2_muls
			cross = [x*f for f in self.wout_c_func_exprs for x in self.wout_c_xs1_muls]
			self.mul_extend_terms = self.wout_c_xs2_muls + self.wout_c_func_exprs + cross
		else:
			print("UNKNOWN EXTEND_LEVEL!!")

		self.mul_extend_terms = self._uniquify(self.mul_extend_terms)
		self.mul_extend_lim_terms = self._uniquify(self.mul_extend_lim_terms)




	def grow(self, M):

		var_expands = self._var_sub(M.orig)
		add_expands = self._add_extend(M.orig)
		mul_expands = self._mul_extend(M.orig)

		var_expands_C = [ self._toggle_plus_C(e) for e in var_expands ]
		add_expands_C = [ self._toggle_plus_C(e) for e in add_expands ]
		mul_expands_C = [ self._toggle_plus_C(e) for e in mul_expands ]

		var_expands = self._uniquify(var_expands + var_expands_C)
		add_expands = self._uniquify(add_expands + add_expands_C)
		mul_expands = self._uniquify(mul_expands + mul_expands_C)
		
		add_biggers = []
		if self.add_xtop:
			add_biggers = self._add_extend_top_level(M.orig)
			add_biggers_C = [ self._toggle_plus_C(e) for e in add_biggers ]
			add_biggers = self._uniquify(add_biggers + add_biggers_C)

		shrunk = []
		if self.shrinker:
			shrunk = self._shrinker(M.orig)

		var_models = [model.Model(e, p_id=M.id, reln="var_xpnd") for e in var_expands if e != C]
		big_models = [model.Model(e, p_id=M.id, reln="add_bigr") for e in add_biggers if e != C]
		add_models = [model.Model(e, p_id=M.id, reln="add_xpnd") for e in add_expands if e != C]
		mul_models = [model.Model(e, p_id=M.id, reln="mul_xpnd") for e in mul_expands if e != C]
		shrunk_models = [model.Model(e, p_id=M.id, reln="shrunk") for e in shrunk if e != C]

		models = var_models + big_models + add_models + mul_models + shrunk_models
		return models


	def _var_sub(self, expr, limit_sub=False, depth=1):
		new_exprs = []
		# only worry about non-atoms, cause we have to replace args
		if not expr.is_Atom:
			# make a list of args to this non-atom
			# each member of the list is the original expr's args with one substitution made
			args_sets = []
			for i,e in enumerate(expr.args):
				# if the current arg is also a non-atom, then recursion!
				if not e.is_Atom:
					## check to see if we are in some function besides ADD or MUL
					## if so, limit what we substitute
					lim_sub = limit_sub or not (e.is_Add or e.is_Mul)
					# for each expr returned, we need to clone the current args
					# and make the substitution, sorta like flattening?
					ee = self._var_sub(e, lim_sub, depth=depth+1)
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
					## First, whats the context? what are we going to substitute?
					sub_terms = None
					if depth >= self.limiting_depth:
						sub_terms = self.var_sub_dep_terms
					else:
						sub_terms = self.var_sub_terms
					if limit_sub:
						if depth >= self.limiting_depth:
							sub_terms = self.var_sub_dep_lim_terms
						else:
							sub_terms = self.var_sub_lim_terms

					# loop over sub_terms, subing for and create new arg sets
					for vs in sub_terms:
						# clone current args
						cloned_args = list(expr.args)
						# replace this term in each
						cloned_args[i] = vs
						# append to the args_sets
						args_sets.append(cloned_args)
				else:
					# we don't have to do anything, probably?
					# coefficients?
					pass

			# finally, create all of the clones at the current level of recursion
			for args in args_sets:
				args = tuple(args)
				tmp = expr.func(*args)
				new_exprs.append(tmp)

		ret_exprs = self._uniquify(new_exprs)
		return ret_exprs

	

	def _add_extend_top_level(self, expr):
		"""
		this only extends a top-level addition, but in a more complex way with _mul_extend. NO recursion!
		For each term in the addition, we do all possible mul_expands, and then append to the full Add.
		This will likely create lots of duplicate, need to check on simplification, or at least grouping terms
		"""
		if expr.is_Add:
			new_terms = []

			for e in expr.args:
				if e.is_Mul:
					for term in self.mul_extend_terms:
						cloned_args = list(e.args)
						cloned_args.append(term)
						new_mul = e.func(*cloned_args)
						new_terms.append(new_mul)

			new_exprs = []
			for term in new_terms:
				cloned_args = list(expr.args)
				cloned_args.append(term)
				bigger_add = expr.func(*cloned_args)
				new_exprs.append(bigger_add)

			ret_exprs = self._uniquify(new_exprs)
			return ret_exprs

		else:
			return []

	def _shrinker(self, expr):
		"""
		this modifies an addition, by removing one term at a time
		"""

		if expr.is_Atom:
			return []

		ret_exprs = []
		new_exprs = []

		# handle this being add  (MUL easy by adding 'or expr.is_Mul') [might want to track separately though]
		if expr.is_Add:
			for i,e in enumerate(expr.args):
				cloned_args = list(expr.args)
				del cloned_args[i]
				smaller_add = expr.func(*cloned_args)
				new_exprs.append(smaller_add)
		
		# recursive case
		args_sets = []
		for i,e in enumerate(expr.args):
			if not e.is_Atom:
				ee = self._shrinker(e)
				if len(ee) > 0:
					# We made a removal(s) on an addition down this branch!!
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
			new_exprs.append(tmp)



		ret_exprs = self._uniquify(new_exprs)
		return ret_exprs




	def _add_extend(self, expr, limit_sub=False):
		new_exprs = []
		# only worry about non-atoms, cause we extend args
		if not expr.is_Atom:
			args_sets = []
			# however we have 2 cases here (as opposed to _var_sub)
			# 1. extend this expression if it's an Add
			if expr.is_Add:
				sub_terms = self.add_extend_terms
				if limit_sub:
					sub_terms = self.add_extend_lim_terms
				for term in sub_terms:
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
					lim_sub = limit_sub or not (e.is_Add or e.is_Mul)
					ee = self._add_extend(e,limit_sub=lim_sub)
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
				new_exprs.append(tmp)

		ret_exprs = self._uniquify(new_exprs)
		return ret_exprs



	def _mul_extend(self, expr, limit_sub=False):
		new_exprs = []
		# only worry about non-atoms, cause we extend args
		if not expr.is_Atom:
			args_sets = []
			# however we have 2 cases here (as opposed to _var_sub)
			# 1. extend this expression if it's a Mul
			if expr.is_Mul:
				sub_terms = self.mul_extend_terms
				if limit_sub:
					sub_terms = self.mul_extend_lim_terms
				for term in sub_terms:
					cloned_args = list(expr.args)
					cloned_args.append(term)
					args_sets.append(cloned_args)

			# 2. do the recursion
			for i,e in enumerate(expr.args):
				if not e.is_Atom:
					lim_sub = limit_sub or not (e.is_Add or e.is_Mul)
					ee = self._mul_extend(e,limit_sub=lim_sub)
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
				new_exprs.append(tmp)

		
		ret_exprs = self._uniquify(new_exprs)
		return ret_exprs



	def _uniquify(self,exprs):
		## UNIQUIFY THE RESULTS
		pass_set = set()
		for p in exprs:
			s = p.evalf()
			pass_set.add(s)
		return list(pass_set)


	def _toggle_plus_C(self, expr):
		if expr.is_Add:
			hasC = False
			for e in expr.args:
				if e == C:
					hasC = True
					break
			if not hasC:
				return expr + C
			else:
				args = [e for e in expr.args if e != C]
				args = tuple(args)
				return expr.func(*args)
		else:
			return sympy.Add(expr, C)





