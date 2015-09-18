from search import PGE

import expand
import tests

###  TODOS
#
# - benchmarks
#   - functions
# - scikit learn
#   - pandas DFs
# - more error metrics
# - diffeqs
#   - models
#   - evaluation RK4
# - other system types
#   - invarients
#   - hidden
#   - pdes
# - algebra
#   - growing / filtering policies
#   - simplification / expansions
#   - +C ???
# - networkx
# - logging
# - checkpointing
# - statistics
# - Ipython notebook examples
# - abstract expressions / memoization
#   - when / where coefficients
#   - domain alphabet
#   - sub-expression frequencies in population
# - distributing to the cloud

def main():
	print "hello pypge!\n"

	pge_1_var = PGE(
		system_type = "explicit",
		search_vars = "y",
		usable_vars = "x",
		# usable_funcs = expand.BASIC_BASE,
		pop_count = 4,
		max_iter = 5
		)

	pge_1_var.loop()

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
