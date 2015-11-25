#!/bin/bash


WOUT_FUNCS='    usable_funcs: []'

WITH_FUNCS='    usable_funcs: \
     - "sin" \
     - "cos"'

LINEAR_FUNCS='      func_level: "linear"'
NONLIN_FUNCS='      func_level: "nonlin"'

USABLE_FUNCS_1=(
	# WOUT_FUNCS
	WITH_FUNCS
)
FUNC_LINEARITY_1=(
	LINEAR_FUNCS
	# NONLIN_FUNCS
)
INIT_LEVELS_1=(
	'med'
	# 'high'
)
GROW_LEVELS_1=(
	'low'
	'med'
	# 'high'
)
SUBS_LEVELS_1=(
	'med'
	'high'
)
XTOP_LEVELS_1=(
	'true'
	'false'
)
LIMITING_DEPTHS_1=(
	# 3
	4
	# 5
)

USABLE_L2_PARAMS=()

L2=(
	'# '
	''
)

ITERATIONS=(
	20
)


echo "GOT HERE"

for iter in ${ITERATIONS[@]}; do
echo "GOT HERE ${iter}"


for func in ${USABLE_FUNCS_1[@]}; do
for liny in ${FUNC_LINEARITY_1[@]}; do
for init in ${INIT_LEVELS_1[@]}; do

for grow in ${GROW_LEVELS_1[@]}; do
for subs in ${SUBS_LEVELS_1[@]}; do
for xtop in ${XTOP_LEVELS_1[@]}; do
for limd in ${LIMITING_DEPTHS_1[@]}; do

	# if [ grow -eq subs ]; then continue fi

	cat config_sedlet.yml > tmp1.yml

	sed -e "s/ITERATIONS/${iter}/"        tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	   
	sed -e "s/USABLE_FUNCS_1/${!func}/"   tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/FUNC_LINEARITY_1/${!liny}/" tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/INIT_LEVEL_1/${init}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
       
	sed -e "s/GROW_LEVEL_1/${grow}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/SUBS_LEVEL_1/${subs}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/USE_XTOP_1/${xtop}/"        tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/LIM_DEPTH_1/${limd}/"       tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	

	TIERS="1"
	L2="# "
	sed -e "s/L2/${L2}/" tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml

	fn="config_explicit_G${grow}_S${subs}_X${xtop}_L${limd}_T${TIERS}"
	sed -e "s/NAME/${fn}/" tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml


	mv tmp1.yml ${fn}.yml

	echo "$fn"


	# if [ L2 -eq true ]; do
	# for __ in ${USABLE_FUNCS_1[@]}; do
	# for __ in ${FUNC_LINEARITY_1[@]}; do
	# for __ in ${INIT_LEVELS_1[@]}; do
	# for __ in ${GROW_LEVELS_1[@]}; do
	# for __ in ${SUBS_LEVELS_1[@]}; do
	# for __ in ${XTOP_LEVELS_1[@]}; do
	# for __ in ${LIMITING_DEPTHS_1[@]}; do

done
done
done
done

done
done
done

done





