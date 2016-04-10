#!/bin/bash


WOUT_FUNCS='    usable_funcs: []'

WITH_FUNCS='    usable_funcs: \
     - "sin" \
     - "cos"'

LINEAR_FUNCS='      func_level: "linear"'
NONLIN_FUNCS='      func_level: "nonlin"'

USABLE_FUNCS_1=(
	WOUT_FUNCS
	# WITH_FUNCS
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
	# 'high'
)
XTOP_LEVELS_1=(
	# 'true'
	'false'
)
LIMITING_DEPTHS_1=(
	# 3
	4
	# 5
)

USABLE_FUNCS_2=(
	# WOUT_FUNCS
	WITH_FUNCS
)
FUNC_LINEARITY_2=(
	LINEAR_FUNCS
	# NONLIN_FUNCS
)
INIT_LEVELS_2=(
	'med'
	# 'high'
)
GROW_LEVELS_2=(
	# 'low'
	'med'
	'high'
)
SUBS_LEVELS_2=(
	# 'med'
	'high'
)
XTOP_LEVELS_2=(
	'true'
	# 'false'
)
LIMITING_DEPTHS_2=(
	# 3
	4
	# 5
)

L2=(
	'# '
	''
)

ITERATIONS=(
	20
)


for iter in ${ITERATIONS[@]}; do

for func in ${USABLE_FUNCS_1[@]}; do
for liny in ${FUNC_LINEARITY_1[@]}; do
for init in ${INIT_LEVELS_1[@]}; do

for grow in ${GROW_LEVELS_1[@]}; do
for subs in ${SUBS_LEVELS_1[@]}; do
for xtop in ${XTOP_LEVELS_1[@]}; do
for limd in ${LIMITING_DEPTHS_1[@]}; do



for func2 in ${USABLE_FUNCS_2[@]}; do
for liny2 in ${FUNC_LINEARITY_2[@]}; do
for init2 in ${INIT_LEVELS_2[@]}; do

for grow2 in ${GROW_LEVELS_2[@]}; do
for subs2 in ${SUBS_LEVELS_2[@]}; do
for xtop2 in ${XTOP_LEVELS_2[@]}; do
for limd2 in ${LIMITING_DEPTHS_2[@]}; do


	cat config_sedlet.yml > tmp1.yml

	sed -e "s/ITERATIONS/${iter}/"        tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	   
	sed -e "s/USABLE_FUNCS_1/${!func}/"   tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/FUNC_LINEARITY_1/${!liny}/" tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/INIT_LEVEL_1/${init}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
       
	sed -e "s/GROW_LEVEL_1/${grow}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/SUBS_LEVEL_1/${subs}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/USE_XTOP_1/${xtop}/"        tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/LIM_DEPTH_1/${limd}/"       tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	

	TIERS="2"
	L2=""
	sed -e "s/L2/${L2}/" tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml


	sed -e "s/USABLE_FUNCS_2/${!func2}/"   tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/FUNC_LINEARITY_2/${!liny2}/" tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/INIT_LEVEL_2/${init2}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
       
	sed -e "s/GROW_LEVEL_2/${grow2}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/SUBS_LEVEL_2/${subs2}/"      tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/USE_XTOP_2/${xtop2}/"        tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml
	sed -e "s/LIM_DEPTH_2/${limd2}/"       tmp1.yml > tmp2.yml && mv tmp2.yml tmp1.yml



	fn="config_explicit_Fwout_G${grow}_S${subs}_X${xtop}_L${limd}_G${grow2}_S${subs2}_X${xtop2}_L${limd2}_T${TIERS}"
	sed -e "s/NAME/${fn}/" tmp1.yml > tmp2.yml
	mv tmp2.yml ${fn}.yml

	fn="config_diffeq_Fwout_G${grow}_S${subs}_X${xtop}_L${limd}_G${grow2}_S${subs2}_X${xtop2}_L${limd2}_T${TIERS}"
	sed -e "s/NAME/${fn}/" tmp1.yml > tmp2.yml
	mv tmp2.yml ${fn}.yml

	rm tmp1.yml

done
done
done
done

done
done
done


done
done
done
done

done
done
done


done





