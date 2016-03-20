#!/bin/bash

evaluators=(
	01
	02
	03
	04
	06
	08
	12
	16
)

pythons=(
	01
	02
	03
	04
	06
	08
)


for evals in ${evaluators[@]}; do
for pyths in ${pythons[@]}; do

	sed -e "s/WORKERS/${evals}/" config_sedlet.yml > config_explicit_p${pyths}_e${evals}.yml

done
done