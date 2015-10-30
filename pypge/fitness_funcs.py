# functions in this class are applied to all models just prior to selection
# they must take a list of models, this way we can have both
#   fitness_funcs which operate on models independently
#   and those which operate on all, such as calculating nomalized values

import numpy as np
from deap import base, creator


def get_fitness_calc(name):
	if name == "size_score":
		return size_score
	elif name == "size_evar":
		return size_evar
	elif name == "size_r2":
		return size_r2
	elif name == "normed_size_score" or name == "normalized_size_score":
		return normalized_size_score
	elif name == "normed_size_evar" or name == "normalized_size_evar":
		return normalized_size_evar
	elif name == "normed_size_r2" or name == "normalized_size_r2":
		return normalized_size_r2

	elif name == "size_score_Iredchi":
		return size_score_Iredchi
	elif name == "normed_size_score_Iredchi" or name == "normalized_size_score_Iredchi":
		return normalized_size_score_Iredchi
	else:
		raise Exception("unknown fitness function")



##  size, score
creator.create("FitnessMinMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("FitnessMinMax", base.Fitness, weights=(-1.0, 1.0))

creator.create("FitnessMinMinMax", base.Fitness, weights=(-1.0, -1.0, 1.0))

def size_score_Iredchi(models):
	for modl in models:
		vals = (modl.size(), modl.score, modl.improved_redchi)
		modl.fitness = creator.FitnessMinMinMax()
		modl.fitness.setValues( vals )

def normalized_size_score_Iredchi(models):
	sizes = np.zeros(len(models))
	scores = np.zeros(len(models))
	redchi = np.zeros(len(models))
	for i,modl in enumerate(models):
		sizes[i] = modl.size()
		scores[i] = modl.score
		redchi[i] = modl.improved_redchi
	
	normSizes = sizes / np.linalg.norm(sizes)
	normScores = scores / np.linalg.norm(scores)
	normRedchi = redchi / np.linalg.norm(redchi)

	for i,modl in enumerate(models):
		vals = (normSizes[i], normScores[i], normRedchi[i])
		modl.fitness = creator.FitnessMinMinMax()
		modl.fitness.setValues( vals )




def size_score(models):
	for modl in models:
		vals = (modl.size(), modl.score)
		modl.fitness = creator.FitnessMinMin()
		modl.fitness.setValues( vals )

def size_evar(models):
	for modl in models:
		vals = (modl.size(), modl.evar)
		modl.fitness = creator.FitnessMinMin()
		modl.fitness.setValues( vals )

def size_r2(models):
	for modl in models:
		vals = (modl.size(), modl.r2)
		modl.fitness = creator.FitnessMinMin()
		modl.fitness.setValues( vals )


def normalized_size_score(models):
	sizes = np.zeros(len(models))
	scores = np.zeros(len(models))
	for i,modl in enumerate(models):
		sizes[i] = modl.size()
		scores[i] = modl.score
	
	normSizes = sizes / np.linalg.norm(sizes)
	normScores = scores / np.linalg.norm(scores)

	for i,modl in enumerate(models):
		vals = (normSizes[i], normScores[i])
		modl.fitness = creator.FitnessMinMin()
		modl.fitness.setValues( vals )

def normalized_size_evar(models):
	sizes = np.zeros(len(models))
	scores = np.zeros(len(models))
	for i,modl in enumerate(models):
		sizes[i] = modl.size()
		scores[i] = modl.evar
	
	normSizes = sizes / np.linalg.norm(sizes)
	normScores = scores / np.linalg.norm(scores)

	for i,modl in enumerate(models):
		vals = (normSizes[i], normScores[i])
		modl.fitness = creator.FitnessMinMax()
		modl.fitness.setValues( vals )

def normalized_size_r2(models):
	sizes = np.zeros(len(models))
	scores = np.zeros(len(models))
	for i,modl in enumerate(models):
		sizes[i] = modl.size()
		scores[i] = modl.r2
	
	normSizes = sizes / np.linalg.norm(sizes)
	normScores = scores / np.linalg.norm(scores)

	for i,modl in enumerate(models):
		vals = (normSizes[i], normScores[i])
		modl.fitness = creator.FitnessMinMax()
		modl.fitness.setValues( vals )
