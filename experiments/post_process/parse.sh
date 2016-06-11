#!/bin/bash 

baseline=0
basic=0
fitness_metrics=0
enhanced_expansion=0
progressive_expansion=0
progressive_evaluation=0
speedup=0
final=0

# baseline=1
basic=1
# fitness_metrics=1
# enhanced_expansion=1
# progressive_expansion=1
# progressive_evaluation=1
# speedup=1
final=1

set -e

source scripts/extraction_helpers.sh


if [ "$baseline" -eq "1" ]; then
	cd 01_baseline && python3 parse.py  && cd ..
fi

### 02_basic ###
if [ "$basic" -eq "1" ]; then
	extract_last_lines_from_errs_log /dissertation_output/02_basic table.txt
	python3 scripts/latex_table.py table.txt "problem"  "best_r2" "evald_models"
fi


### 04_fitness_metrics ###
if [ "$fitness_metrics" -eq "1" ]; then
	# extract_last_lines_from_errs_log /dissertation_output/04_fitness_metrics table.txt true
	# python3 scripts/latex_table.py table.txt "problem"  "group"  "ave_size"  "ave_r2"  "best_r2"
	# python3 scripts/timing_stats_04.py table.txt  "elapsed_seconds" "problem"  "group" "elapsed_seconds"  "evald_models"  "best_r2"
	# python3 scripts/timing_stats_04.py table.txt  "evald_models" "problem"  "group" "elapsed_seconds"  "evald_models"  "best_r2"
	# python3 scripts/timing_stats_04.py table.txt  "best_r2" "problem"  "group" "elapsed_seconds"  "evald_models"  "best_r2"
	python3 scripts/timing_stats_04.py table.txt  "ave_size" "problem"  "group" "ave_size"  
fi


### 05_enhanced_expansion ###
if [ "$enhanced_expansion" -eq "1" ]; then
	extract_last_lines_from_errs_log /dissertation_output/05_enhanced_expansion table.txt true
	# python3 scripts/group_table.py table.txt "problem"  "group" "elapsed_seconds" "evald_models" "best_r2"
	python3 scripts/timing_stats_05.py table.txt "problem"  "group" "elapsed_seconds"  "evald_models"  "best_r2" "ave_size"
fi


### 06_progressive_expansion ###
if [ "$progressive_expansion" -eq "1" ]; then
	extract_last_lines_from_errs_log /dissertation_output/06_progressive_expansion table.txt true
	python3 scripts/group_table.py table.txt "problem"  "group" "elapsed_seconds" "evald_models" "best_r2"
	cat table.txt | sed -e "s/low/L/g" -e "s/med/M/g" -e "s/high/H/g" -e "s/false/F/g" -e "s/true/T/g" -e "s/diffeq_//g" -e "s/_L4_T1//g" > clean.txt
	python3 scripts/graph_06.py clean.txt
	# python3 scripts/timing_stats_06.py table.txt "elapsed_seconds" "problem"  "group" "elapsed_seconds" 
	# python3 scripts/timing_stats_06.py table.txt "evald_models" "problem"  "group" "evald_models" 
	# python3 scripts/timing_stats_06.py table.txt "best_r2" "problem"  "group" "best_r2" 
fi


### 07_progressive_evaluation ###
if [ "$progressive_evaluation" -eq "1" ]; then
	extract_last_lines_from_errs_log /dissertation_output/07_progressive_evaluation table.txt true
	python3 scripts/latex_table.py table.txt "problem"  "group"  "best_r2"  "elapsed_seconds"  "peekd_models"  "evald_models" "total_point_evals"
fi


### 08_speedup ###
if [ "$speedup" -eq "1" ]; then
	extract_last_lines_from_errs_log /dissertation_output/08_speedup table.txt true
	python3 scripts/group_table.py table.txt "problem" "group" "elapsed_seconds" "best_r2"
	extract_loop_timing_data_from_main_log /dissertation_output/08_speedup speedup.txt true
	clean_loop_timing_data speedup.txt > clean_speedup.txt
	python3 scripts/gather_speedup.py clean_speedup.txt calcd_speedup.txt
	python3 scripts/graph_speedup.py calcd_speedup.txt
	python3 scripts/boxplot_speedup.py clean_speedup.txt boxp_speedup.txt
fi


### 09_final ###
if [ "$final" -eq "1" ]; then
	extract_last_lines_from_errs_log /dissertation_output/09_final table.txt
	python3 scripts/latex_table.py table.txt "problem"  "best_r2"  "evald_models"
fi


