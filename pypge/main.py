from search import PGE

import expand

from benchmarks import explicit 

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


def main():
	print "hello pypge!\n"

	prob = explicit.Nguyen_12(0.1)
	print prob['name'] + ":  ", prob['eqn'], "\n"

	pge = PGE(
		system_type = "explicit",
		search_vars = "y",
		usable_vars = prob['xs_str'],
		# usable_funcs = expand.BASIC_BASE,
		pop_count = 3,
		peek_count = 9,
		max_iter = 4,
		workers = 1
		)

	pge.fit(prob['xpts'], prob['ypts'])


main()
