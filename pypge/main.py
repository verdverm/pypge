from search import PGE

import expand
import tests


def main():
	print "hello pypge!\n"

	pge_1_var = PGE(
		system_type = "explicit",
		search_vars = "y",
		usable_vars = "x",
		usable_funcs = expand.BASIC_TRIG,
		max_iter = 10
		)

	print ""

	pge_2_var = PGE(
		system_type = "explicit",
		search_vars = "y",
		usable_vars = "x w",
		usable_funcs = expand.BASIC_TRIG,
		max_iter = 10
		)

	# pge.fit( tests.F_2_X, tests.F_2_Y)

main()