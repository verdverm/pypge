#!/bin/bash

#Baseline 2 component

A_1_1=' \
err_method: "mae" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
'

A_1_2=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
'

# Multiple equal-weight accuracy components

A_2_2a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
 - "+r2" \
'

A_2_2b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
 - "-bic" \
'

A_2_3a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
 - "+r2" \
 - "-bic" \
'

A_2_3b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
 - "+r2" \
 - "+evar" \
'

A_2_4a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
 - "+r2" \
 - "-bic" \
 - "+improve_bic" \
'

A_2_4b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
 - "-redchi" \
 - "-bic" \
 - "+improve_bic" \
'

A_2_5=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-sz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'


# Multiple balanced-weight accuracy components

A_3_2a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "+(2)sz" \
 - "-score" \
 - "+r2" \
'

A_3_2b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(2)sz" \
 - "-score" \
 - "-bic" \
'

A_3_3a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(3)sz" \
 - "-score" \
 - "+r2" \
 - "-bic" \
'

A_3_3b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(3)sz" \
 - "-score" \
 - "+r2" \
 - "+evar" \
'

A_3_4a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(4)sz" \
 - "-score" \
 - "+r2" \
 - "-bic" \
 - "+improve_bic" \
'

A_3_4b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(4)sz" \
 - "-score" \
 - "-redchi" \
 - "-bic" \
 - "+improve_bic" \
'

A_3_5=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(5)sz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'



# Parsimony 2 Component

P_1_1=' \
err_method: "mae" \
fitness_func_params: \
 - "normalize" \
 - "-psz" \
 - "-score" \
'

P_1_2=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-psz" \
 - "-score" \
'

P_1_3=' \
err_method: "mae" \
fitness_func_params: \
 - "normalize" \
 - "-jpsz" \
 - "-score" \
'

P_1_4=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-jpsz" \
 - "-score" \
'


# Parsimony Multi-accuracy Component equal-weighted

P_2_5a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-psz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'
P_2_5b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-jpsz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'
 

# Parsimony Multi-accuracy Component balance-weighted

P_3_5a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(5)psz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'

P_3_5b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(5)jpsz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'


# Parsimony Multi-all Component balance-weighted

P_4_5a=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(4)psz" \
 - "-(1)jpsz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'

P_4_5b=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(3)psz" \
 - "-(2)jpsz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'

P_4_5c=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(2.5)psz" \
 - "-(2.5)jpsz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'

P_4_5d=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(2.5)jpsz" \
 - "-(2.5)psz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'

P_4_5e=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(3)jpsz" \
 - "-(2)psz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'

P_4_5f=' \
err_method: "rmse" \
fitness_func_params: \
 - "normalize" \
 - "-(4)jpsz" \
 - "-(1)psz" \
 - "-score" \
 - "-redchi" \
 - "+evar" \
 - "-bic" \
 - "+improve_bic" \
'


# 16 A's
# 14 P's 


replacements=(
	A_1_1
	A_1_2
	A_2_2a
	A_2_2b
	A_2_3a
	A_2_3b
	A_2_4a
	A_2_4b
	
	A_2_5
	A_3_2a
	A_3_2b
	A_3_3a
	A_3_3b
	A_3_4a
	A_3_4b
	A_3_5

	P_1_1
	P_1_2
	P_1_3
	P_1_4
	P_2_5a
	P_2_5b
	P_3_5a
	P_3_5b

	P_4_5a
	P_4_5b
	P_4_5c
	P_4_5d
	P_4_5e
	P_4_5f
)




for rep in ${replacements[@]}; do

	sed -e "s/FITNESS_PARAMS/${!rep}/" config_sedlet.yml > config_explicit_${rep}.yml

done