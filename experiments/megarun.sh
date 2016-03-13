#!/bin/bash

explicit_probs=(
	"koza_01;out"
	"koza_02;out"
	"koza_03;out"
	# # "lipson_01;out"
	# # "lipson_02;out"
	# # "lipson_03;out"

	# # "nguyen_01;out"
	# "nguyen_02;out"
	# "nguyen_03;out"
	# "nguyen_04;out"
	# "nguyen_05;out"
	# "nguyen_06;out"
	# # "nguyen_07;out"
	# # "nguyen_08;out"
	# "nguyen_09;out"
	# # "nguyen_10;out"
	# # "nguyen_11;out"
	# "nguyen_12;out"

	# "korns_01;out"
	# "korns_02;out"
	# "korns_03;out"
	# "korns_04;out"
	# # "korns_05;out"
	# # "korns_06;out"
	# # "korns_07;out"
	# # "korns_08;out"
	# # "korns_09;out"
	# "korns_10;out"
	# "korns_11;out"
	# "korns_12;out"
	# # "korns_13;out"
	# # "korns_14;out"
	# # "korns_15;out"
)

diffeq_probs=(
	# "bacresp;D_x"
	# "bacresp;D_y"
	# # "barmags;D_X"
	# # "barmags;D_Y"
	# "glider;D_v"
	# "glider;D_A"
	# "ecoli;D_G"
	# "ecoli;D_A"
	# "ecoli;D_L"
	# # "lorenz;D_x"
	# # "lorenz;D_y"
	# # "lorenz;D_z"
	# # "shearflow;D_A"
	# # "shearflow;D_B"
	# # "vanderpol;D_x"
	# # "vanderpol;D_y"
	# # "lotkavolterra;D_x"
	# # "lotkavolterra;D_y"
	# "predpreyfrac;D_x"
	# "predpreyfrac;D_y"
	# "simplependulum;D_A"
	# "simplependulum;D_V"
	# "chaoticpendulum;D_A"
	# "chaoticpendulum;D_V"
)


# ----------------

experiments=(
	# dev
	basic

	# eval_speedup

	# fitness
	# expand_levels
	# expand_ops

	# lotsa_vars
)

noise=(
	"clean"
	# "noisy"
)

datadir="../data/"


run_experiment() {

	local systype=$1
	local experiment=$2
	local cfg=$3
	local noise=$4
	local probFields=$5


	fields=(${probFields//;/ })
	prob=${fields[0]}
	target=${fields[1]}

	echo "  ${experiment} -- ${cfg} :: ${noise} - ${prob} - ${target}"

	cfgfile="${experiment}/${cfg}"
	inputfile="${datadir}/benchmarks/${systype}/${prob}_${noise}.csv"
	outputdir="output/${experiment}/${cfg}/${noise}/${prob}/${target}"

	mkdir -p ${outputdir}

	flags="--target ${target}"

	python3 main.py ${flags} ${cfgfile} ${inputfile} ${outputdir}
	# python main.py ${flags} ${cfgfile} ${inputfile} ${outputdir} > ${outputdir}/pge_output.log


}

experiment_looper () {

	systype=$1
	experiment=$2
	declare -a problems=("${!3}")

	configs=`ls ${experiment} | grep "${systype}" | grep yml`
	for config in ${configs[@]}; do
		echo "--------------------------------"
		echo "    $experiment -- $config"
		echo "--------------------------------"
		for amount in ${noise[@]}; do
		for probFields in ${problems[@]}; do

			# echo "run_experiment ${experiment} ${config} ${amount} ${probFields}"
			run_experiment ${systype} ${experiment} ${config} ${amount} ${probFields}

		done
		done
		echo "================================"
	done
}



echo ""


for experiment in ${experiments[@]}; do
	echo "================================"
	echo "||          Explicit          ||"
	echo "================================"

	experiment_looper "explicit" ${experiment} explicit_probs[@]
done

echo ""
echo ""
echo ""

# echo "DEV ROADBLOCK"
# exit


for experiment in ${experiments[@]}; do
	echo "================================"
	echo "||           Diffeq           ||"
	echo "================================"

	experiment_looper "diffeq" ${experiment} diffeq_probs[@]

done
echo ""
echo ""
echo ""

