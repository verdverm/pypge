from search import PGE

import expand

from benchmarks import explicit

###  TODOS
#
#
# - clean up model class
#
# - diffeqs
#   - models
#   - evaluation RK4
#   - benchmarks
#
#
# - final processing & output(s)
#   - mid process too?
# - logging
# - statistics
# - checkpointing
# - peek eval (others from 2nd paper)
#
#
# - networkx
# - algebra
#   - growing / filtering policies
#   - simplification / expansions
#   - +C ???
#
#
# - Ipython notebook examples
# - scikit learn
#   - pandas DFs
#   - get/set parameters
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

	prob = explicit.Nguyen_12(0.1)
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
