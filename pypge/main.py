from search import PGE

import expand
import tests

from benchmarks import explicit

###  TODOS
#
# - benchmarks
#   - functions
#   - multi-dimensional
#
# - clean up model class
#
# - diffeqs
#   - models
#   - evaluation RK4
#
# - final output(s)
# - logging
# - statistics
# - checkpointing
#
#
#
# - networkx
# - algebra
#   - growing / filtering policies
#   - simplification / expansions
#   - +C ???
#
# - Ipython notebook examples
# - scikit learn
#   - pandas DFs
#
#
#
# - distributing to the cloud, pyspark
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

def main():
	print "hello pypge!\n"

	xs_ranges = []
	xs_ranges.append( (-4.0,4.0) )
	xs_ranges.append( (-4.0,4.0) )
	xs_ranges.append( (-4.0,4.0) )
	xs_ranges.append( (-4.0,4.0) )
	xs_ranges.append( (-4.0,4.0) )

	prob = explicit.Korns_01(xs_ranges, 200,0.1)
	print prob['name'], prob['eqn']

	pge_1_var = PGE(
		system_type = "explicit",
		search_vars = "y",
		usable_vars = prob['xs_str'],
		# usable_funcs = expand.BASIC_BASE,
		pop_count = 3,
		max_iter = 10
		)

	pge_1_var.fit(prob['xpts'], prob['ypts'])

	print ""

	# pge_2_var = PGE(
	# 	system_type = "explicit",
	# 	search_vars = "y",
	# 	usable_vars = "x w",
	# 	usable_funcs = expand.BASIC_TRIG,
	# 	max_iter = 10
	# 	)

	# pge.fit( tests.F_2_X, tests.F_2_Y)

main()
