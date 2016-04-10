#!/bin/bash

echo "parsing 02_basic"

source ../scripts/extract_from_errs_log.sh

extract_last_lines_from_errs_log /dissertation_output/02_basic table.txt
python3 ../scripts/latex_table.py table.txt "problem"  "ave_size"  "ave_err"  "ave_r2"  "best_err"  "best_r2"

# strindex() { 
#   x="${1%%$2*}"
#   [[ $x = $1 ]] && echo -1 || echo ${#x}
# }

# declare -a files=`find /dissertation_output/02_basic -name pge_errs.log -exec ls -d {} \;`


# rm -f table.txt

# for file in ${files[@]}; do
# 	if [ ! -f "table.txt" ]; then
# 		cols=`head -n 1 $file`
# 		# echo "problem $cols" 
# 		echo "problem $cols" > table.txt
# 	fi

# 	idx1=`strindex $file "clean"`
# 	idx2=`strindex $file "pge_errs.log"`
# 	let idx1+=6
# 	let end=idx2-idx1-1
# 	short=${file:idx1:end}

# 	data=`tail -1 $file`

# 	echo "$short $data" >> table.txt

# 	# printf "\n\n"

# done

