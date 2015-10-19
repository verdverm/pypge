# functions in this class are applied to all models just prior to selection
# they must take a list of models, this way we can have both
#   fitness_funcs which operate on models independently
#   and those which operate on all, such as calculating nomalized values

import numpy as np
from deap import base, creator

##  size, score
creator.create("FitnessMinMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("FitnessMinMax", base.Fitness, weights=(-1.0, 1.0))

def size_score(models):
	for modl in models:
		vals = (modl.size(), modl.score)
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
