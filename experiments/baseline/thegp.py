from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

import data as DATA

import operator
import math
import random

import numpy

import multiprocessing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


fobj = open("gp_results.txt", "a")



def run_explicit_loop():
    for problem in DATA.explicit_problems:
        prob,target = problem.split(";")
        df = DATA.read_datafile("explicit", prob)

        cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
        ins = df[cols].as_matrix()
        outs = df[target].values    



        for i in  range(10):
            seed = 23*i
            print("\n\n", prob, target, ins.shape, outs.shape, "\n=======================\n")
            score,r2, gen = run_gp(ins,outs, seed, problem)
            print(i, problem, seed, gen, score, r2, file=fobj)

        print("\n", file=fobj)





def run_gp(ins,outs, rseed, problem_name):

    def protectedDiv(left, right):
        with numpy.errstate(divide='ignore',invalid='ignore'):
            x = numpy.divide(left, right)
            if isinstance(x, numpy.ndarray):
                x[numpy.isinf(x)] = 1
                x[numpy.isnan(x)] = 1
            elif numpy.isinf(x) or numpy.isnan(x):
                x = 1
        return x

    pset = gp.PrimitiveSet("MAIN", len(ins[0]))
    pset.addPrimitive(numpy.add, 2, name="vadd")
    pset.addPrimitive(numpy.subtract, 2, name="vsub")
    pset.addPrimitive(numpy.multiply, 2, name="vmul")
    pset.addPrimitive(protectedDiv, 2)
    pset.addPrimitive(numpy.negative, 1, name="vneg")
    pset.addPrimitive(numpy.cos, 1, name="vcos")
    pset.addPrimitive(numpy.sin, 1, name="vsin")
    cname = problem_name+"_"+str(rseed)
    pset.addEphemeralConstant(cname, lambda: random.randint(-1,1))

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)

    samples = [col.reshape(len(outs),1) for col in ins.T ]
    for s in samples:
        print(s.shape)
    values = outs.reshape(len(outs),1)

    def evalSymbReg(individual):
        func = toolbox.compile(expr=individual)
        yhat = func(*samples)
        diff = numpy.mean((yhat - values)**2)
        return (diff, len(individual))

    toolbox.register("evaluate", evalSymbReg)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("mate", gp.cxOnePointLeafBiased, termpb=0.1)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
    toolbox.register("migrate", tools.migRing, k=2, selection=tools.selBest, replacement=tools.selWorst)

    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

    random.seed(rseed)

 
    NBR_DEMES = 8
    MU = 200
    NGEN = 100
    MIN_ERR = 1.0e-10
    CXPB = 1.0
    MUTPB = 0.5
    MIG_RATE = 5    

    demes = [toolbox.population(n=MU) for _ in range(NBR_DEMES)]
    hof = tools.HallOfFame(1)


    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    stats.register("min", numpy.min)
    stats.register("avg", numpy.mean)
    stats.register("max", numpy.max)
    stats.register("std", numpy.std)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "deme", "evals", "fitness", "size"
    logbook.chapters["fitness"].header = "min", "avg", "max", "std"
    logbook.chapters["size"].header = "min", "avg", "max", "std"
    
    for idx, deme in enumerate(demes):
        for ind in deme:
            ind.fitness.values = toolbox.evaluate(ind)
        logbook.record(gen=0, deme=idx, evals=len(deme), **stats.compile(deme))
        hof.update(deme)
    print(logbook.stream)
    print()
    
    gen = 1
    min_reached = 5
    while gen <= NGEN and min_reached > 0:
        for idx, deme in enumerate(demes):
            parents = toolbox.select(deme, len(deme))
            offspring1 = algorithms.varAnd(parents, toolbox, cxpb=CXPB, mutpb=MUTPB)
            offspring2 = algorithms.varAnd(parents, toolbox, cxpb=CXPB, mutpb=MUTPB)
            offspring = offspring1 + offspring2
            
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            for ind in invalid_ind:
                ind.fitness.values = toolbox.evaluate(ind)

            deme[:] = toolbox.select(deme + offspring, len(deme))
            logbook.record(gen=gen, deme=idx, evals=len(invalid_ind), **stats.compile(deme))
            
            hof.update(deme)
        print(logbook.stream)
        print()

        for row in logbook.chapters["fitness"][-NBR_DEMES:]:
            if row["min"] < MIN_ERR:
                min_reached -= 1
                break
            
        if gen % MIG_RATE == 0:
            toolbox.migrate(demes)
        gen += 1
    
    score = hof[0].fitness.values[0]
    F = toolbox.compile(expr=hof[0])
    yhat = F(*samples)
    r2 = r2_score(values, yhat)

    return score, r2, gen



run_explicit_loop()
