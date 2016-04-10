#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

import operator
import math
import random

import numpy

from sklearn import linear_model


from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

samples = numpy.linspace(-1, 1, 10000)
values = samples**4 + samples**3 + samples**2 + samples

print(samples.shape, values.shape)
# values = 0.3*samples**4 + 1.2*samples**3 + 2.3*samples**2 + 0.2*samples
# values = 3.3*numpy.sin(samples**2)*numpy.cos(samples)-1.0

def evalSymbReg(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the sum of squared difference between the expression
    # and the real function values : x**4 + x**3 + x**2 + x 
    diff = numpy.sum((func(samples) - values)**2)
    return diff,

toolbox.register("evaluate", evalSymbReg)
# toolbox.register("select", tools.selNSGA2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePointLeafBiased, termpb=0.1)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

toolbox.register("migrate", tools.migRing, k=2, selection=tools.selBest, replacement=tools.selWorst)



def main():
    random.seed(223)

    NBR_DEMES = 8
    MU = 200
    NGEN = 50
    CXPB = 0.5
    MUTPB = 0.2
    MIG_RATE = 3    

    demes = [toolbox.population(n=MU) for _ in range(NBR_DEMES)]
    hof = tools.HallOfFame(10)


    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    # stats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    stats = stats_fit
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "deme", "evals", "std", "min", "avg", "max"
    
    for idx, deme in enumerate(demes):
        for ind in deme:
            ind.fitness.values = toolbox.evaluate(ind)
        logbook.record(gen=0, deme=idx, evals=len(deme), **stats.compile(deme))
        hof.update(deme)
    print(logbook.stream)
    
    gen = 1
    # while gen <= NGEN and logbook[-1]["max"] < 100.0:
    while gen <= NGEN:
        for idx, deme in enumerate(demes):
            deme[:] = toolbox.select(deme, len(deme))
            deme[:] = algorithms.varAnd(deme, toolbox, cxpb=CXPB, mutpb=MUTPB)
            # parents = toolbox.select(deme, len(deme))
            # offspring = algorithms.varAnd(parents, toolbox, cxpb=CXPB, mutpb=MUTPB)
            
            invalid_ind = [ind for ind in deme if not ind.fitness.valid]
            for ind in invalid_ind:
                ind.fitness.values = toolbox.evaluate(ind)

            # deme[:] = toolbox.select(deme + offspring, len(deme))
            
            logbook.record(gen=gen, deme=idx, evals=len(deme), **stats.compile(deme))
            hof.update(deme)
        print(logbook.stream)
            
        if gen % MIG_RATE == 0:
            toolbox.migrate(demes)
        gen += 1
    
    # print(hof)
    for i,h in enumerate(hof):
        print(i,h)

    return demes, logbook, hof

    


if __name__ == "__main__":
    main()