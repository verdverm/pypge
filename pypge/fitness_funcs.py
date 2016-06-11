# functions in this class are applied to all models just prior to selection
# they must take a list of models, this way we can have both
#   fitness_funcs which operate on models independently
#   and those which operate on all, such as calculating nomalized values
from __future__ import print_function

import numpy as np
from pypge import base, creator


def build_fitness_calc(params):
	print("fitness parameters: ", params)
	norm = False
	if "normalize" in params:
		norm = True
		params = [p for p in params if p != "normalize"]

	build_fitness_class(params)
	extractor = build_value_extractor(params)

	if norm:
		return fitness_calc_norm(extractor)
	else:
		return fitness_calc_raw(extractor)

def fitness_calc_raw(extractor):
	def calculator(models):
		for modl in models:
			vals = extractor(modl)
			modl.fitness = creator.FitnessCalculator()
			modl.fitness.setValues( vals )
	return calculator

def fitness_calc_norm(extractor):
	def calculator(models):
	
		vals = []
		for modl in models:
			vs = extractor(modl)
			vals.append(vs)

		# print(vals)
		npvals = np.array(vals).T

		normed = []
		for col in npvals:
			# print("COL: ", col)
			norm = col / np.linalg.norm(col)
			normed.append(norm)

		normd_vals = np.array(normed).T

		for i,modl in enumerate(models):
			vals = tuple(normd_vals[i])
			modl.fitness = creator.FitnessCalculator()
			modl.fitness.setValues( vals )


	return calculator


def build_fitness_class(params):
	weights = build_fitness_weights(params)
	creator.create("FitnessCalculator", base.Fitness, weights=weights)

def build_fitness_weights(params):
	weights = []
	for p in params:
		W = 1.0
		if "(" in p and ")" in p:
			lp = p.index("(")
			rp = p.index(")")
			W = float(p[lp+1:rp])
		if p[0] == "-":
			weights.append(-1.0 * W)
		elif p[0] == "+":
			weights.append(1.0 * W)
		else:
			print("UNSIGNED FITNESS PARAMETER!!!")
	print("weights: ", weights)
	return tuple(weights)

def build_value_extractor(params):
	ps = []

	for i,p in enumerate(params):
		if ")" in p:
			rp = p.index(")") + 1
			params[i] = p[rp:]
		else:
			params[i] = p[1:]

	ps = [p for p in params]
	print("PS: ", ps)
	

	def extractor(modl):
		vals = []
		for p in ps:
			v = getattr(modl, p)
			vals.append(v)
		return tuple(vals)
	return extractor
