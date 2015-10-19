#!/bin/bash

probs=(
	# koza_01_clean
	# koza_02_clean
	# koza_03_clean
	# lipson_01_clean
	# lipson_02_clean
	# lipson_03_clean

	# nguyen_01_clean
	# nguyen_02_clean
	# nguyen_03_clean
	# nguyen_04_clean
	# nguyen_05_clean
	# nguyen_06_clean
	# nguyen_07_clean
	nguyen_08_clean
	# nguyen_09_clean
	nguyen_10_clean
	# nguyen_11_clean
	# nguyen_12_clean
)

for prob in ${probs[@]}; do
	echo ${prob}
	mkdir -p temp/${prob}
	python main.py config.yml data/benchmarks/explicit/${prob}.csv temp/${prob} > temp/${prob}/pge_output.log
done
