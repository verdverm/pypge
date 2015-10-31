#!/bin/bash

probs=(
	# koza_01
	# koza_02
	koza_03
	# lipson_01
	# lipson_02
	# lipson_03

	# nguyen_01
	# nguyen_02
	# nguyen_03
	# nguyen_04
	# nguyen_05
	# nguyen_06
	# nguyen_07
	# nguyen_08
	# nguyen_09
	# nguyen_10
	# nguyen_11
	# nguyen_12

	# korns_01
	# korns_02
	# korns_03
	# korns_04
	# korns_05
	# korns_06
	# korns_07
	# korns_08
	# korns_09
	# korns_10
	# korns_11
	# korns_12
	# korns_13
	# korns_14
	# korns_15

	# "bacresp;dx"
	# "bacresp;dy"
	# "barmags;dX"
	# "barmags;dY"
	# "glider;dv"
	# "glider;dA"
	# "ecoli;dG"
	# "ecoli;dA"
	# "ecoli;dL"
	# "lorenz;dx"
	# "lorenz;dy"
	# "lorenz;dz"
	# "shearflow;dA"
	# "shearflow;dB"
	# "vanderpol;dx"
	# "vanderpol;dy"
	# "lotkavolterra;dx"
	# "lotkavolterra;dy"
	# "predpreyfrac;dx"
	# "predpreyfrac;dy"

	# "simplependulum;dA"
	# "simplependulum;dV"
	# "chaoticpendulum;dA"
	# "chaoticpendulum;dV"
)

noise=(
	"clean"
	# "noisy"
)

func_levels=(
	"linear"
	# "nonlin"
)

init_levels=(
	"low"
	# "med"
	# "high"
)

grow_levels=(
	"low"
	# "med"
	# "high"
)

systype="explicit"
# systype="diffeq"

for probFields in ${probs[@]}; do
for amount in ${noise[@]}; do
for init in ${init_levels[@]}; do
for grow in ${grow_levels[@]}; do
for func in ${func_levels[@]}; do

	prob=${probFields}
	target="out"

	# fields=(${probFields//;/ })
	# prob=${fields[0]}
	# target=${fields[1]}

	echo "${prob} - ${target} - ${amount} -- f:${func} i:${init} g:${grow}"

	configfile="config.yml"
	inputfile="../data/benchmarks/${systype}/${prob}_${amount}.csv"
	outputdir="output/stage2b/${prob}/${target}/F_${func}__I_${init}__G_${grow}"

	mkdir -p ${outputdir}

	flags="--target ${target} --init_level ${init} --grow_level ${grow} --func_level ${func}"

	python main.py ${flags} ${configfile} ${inputfile} ${outputdir}
	# python main.py ${flags} ${configfile} ${inputfile} ${outputdir} > ${outputdir}/pge_output.log

done
done
done
done
done

