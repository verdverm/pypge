from search import PGE

import expand

from benchmarks import explicit

###  TODOS
#
# - diffeqs
#   - datagen with RK4
#   - numerical evaluation
#   - benchmarks with point eval
#
# - logging
# - statistics
#   - memotree
#   - within model
#   - for expansions
#   - what's improving and not
#   - subexpressions#
#
# - networkx & relations for ...
# - algebra
#   - growing / initing policies
#   - simplification / expansions
#   - filtering policies
#   - +C ???
#
# - check states being set properly
# - distributing to the cloud, pyspark
#
# - Ipython notebook examples
# - scikit learn
#   - pandas DFs
#   - get/set parameters
#   - pipelining
#   - gridsearch
#
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
		max_iter = 12,
		workers = 4
		)

	pge.fit(prob['xpts'], prob['ypts'])


main()
