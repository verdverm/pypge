from search import PGE

import expand

from benchmarks import explicit 

import pandas
import numpy
import sympy


###  TODOS
#
#   objective 1. Pull method for expression generation
#   objective 2. Use more graph & algebra et all... 
#   objective 3. Build interactive visualization in IPython
#   objective N. Build in stats & logging while dev'n previous 2
#
#
# - Ipython notebook examples
#   - D3, or similar
#   - plot geneology on pareto fronts
#   - interactive visualizations
#
# - networkx & relations for ...
# - algebra
#   - growing / initing policies
#   - simplification / expansions
#   - filtering policies
#   - +C ???
#   - OTHER ISSUE:  
#     - dealing with C vs C_# && 
#     - model.orig vs model.expr && 
#     - init'n vs manip'n
#
# - logging
# - statistics
#   - memotree
#   - within model
#   - for expansions
#   - what's improving and not
#   - subexpressions#
#
# - scikit learn
#   - pandas DFs
#   - get/set parameters
#   - pipelining
#   - gridsearch
#
# - run on the GPU with theano
# - distributing to the cloud, pyspark
#
#
#
# - diffeqs
#   - problems with default parameters
#   - need to toggle on system type ???
#
# - other system types
#   - invarients
#   - hidden
#   - pdes
#
# - abstract expressions / memoization
#   - when / where coefficients
#   - domain alphabet
#   - sub-expression frequencies in population
#
#
#

import time

def main():
	print "hello pypge!\n"

	start = time.time()

	# prob = explicit.Nguyen_12(0.1)
	# print prob['name'] + ":  ", prob['eqn'], "\n"

	# pge = PGE(
	# 	system_type = "explicit",
	# 	search_vars = "y",
	# 	usable_vars = prob['xs_str'],
	# 	# usable_funcs = expand.BASIC_BASE,
	# 	pop_count = 3,
	# 	peek_count = 20,
	# 	algebra_methods = None,
	# 	max_iter = 10,
	# 	workers = 2,
	# 	print_timing = True
	# 	)

	# pge.fit(prob['xpts'], prob['ypts'])



	df = pandas.read_csv("~/Downloads/dataset4.csv", header=None, names=["m", "l", "n", "s", "y"], delim_whitespace=True)
	ins = numpy.array([df['m'].values, df['l'].values, df['n'].values, df['s'].values])
	outs = df['y'].values

	pge = PGE(
		system_type = "explicit",
		search_vars = "y",
		usable_vars = "m l n s",
		#usable_funcs = (log, sin, cos, exp, tan),
		usable_funcs = [sympy.sin, sympy.cos],
		# usable_funcs = expand.BASIC_BASE,
		algebra_methods = None,
		pop_count = 3,
		peek_count = 20,
		max_iter = 30,
		workers = 2,
		print_timing = True
		)

	pge.fit(ins, outs)


	end = time.time()
	print "\n\nTotal Runtime: ", end - start, "seconds\n\n"


main()
