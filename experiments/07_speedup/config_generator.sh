#!/bin/bash

evaluators=(
	1
	2
	3
	4
	6
	8
	12
	16
)

pythons=(
	1
	2
	3
	4
)


for evals in ${evaluators[@]}; do
for pyths in ${pythons[@]}; do

	if [ "$evals" -lt "$pyths" ]; then
		continue
	fi
	if [ "$evals" -ge "5" ] && [ "$pyths" -lt "3" ]; then
		continue
	fi

	cat config_sedlet.yml | sed -e "s/WORKERS/${pyths}/" | sed -e "s/REMOTE/${evals}/" \
		> config_explicit_p${pyths}_e${evals}.yml

	cat config_sedlet.yml | sed -e "s/WORKERS/${pyths}/" | sed -e "s/REMOTE/${evals}/" \
		> config_diffeq_p${pyths}_e${evals}.yml

done
done