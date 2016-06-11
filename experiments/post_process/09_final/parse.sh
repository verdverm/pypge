#!/bin/bash

echo "parsing 09_final"

strindex() { 
  x="${1%%$2*}"
  [[ $x = $1 ]] && echo -1 || echo ${#x}
}

declare -a files=`find /dissertation_output/09_final -name pge_errs.log -exec ls -d {} \;`


rm -f table.txt

for file in ${files[@]}; do
	if [ ! -f "table.txt" ]; then
		cols=`head -n 1 $file`
		# echo "problem $cols" 
		echo "problem $cols" > table.txt
	fi

	idx1=`strindex $file "clean"`
	idx2=`strindex $file "pge_errs.log"`
	let idx1+=6
	let end=idx2-idx1-1
	short=${file:idx1:end}

	data=`tail -1 $file`

	echo "$short $data" >> table.txt

	# printf "\n\n"

done

python3 parse.py
