#!/bin/bash

replacements=(
	01
	02
	03
	04
	06
	08
	12
	16
)


for rep in ${replacements[@]}; do

	sed -e "s/WORKERS/${!rep}/" config_sedlet.yml > config_explicit_${rep}.yml

done