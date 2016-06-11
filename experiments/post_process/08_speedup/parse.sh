#!/bin/bash


echo "parsing 08_speedup"


strindex() { 
  x="${1%%$2*}"
  [[ $x = $1 ]] && echo -1 || echo ${#x}
}

declare -a files=`find /dissertation_output/08_speedup -name pge_errs.log -exec ls -d {} \;`


rm -f table.txt
rm -f headers2.txt

printf "problem " > table2.txt


for file in ${files[@]}; do
	if [ ! -f "table.txt" ]; then
		cols=`head -n 1 $file`
		# echo "problem $cols" 
		echo "group problem $cols" > table.txt
	fi

	idx1=`strindex $file "config"`
	idx2=`strindex $file "clean"`
	let idx1+=7
	let end=idx2-idx1-1
	group=${file:idx1:end}

	group="$(echo -e "${group}" | tr -d '[[:space:]]')"

	idx1=`strindex $file "clean"`
	idx2=`strindex $file "pge_errs.log"`
	let idx1+=6
	let end=idx2-idx1-1
	short=${file:idx1:end}

	echo "$group $short"

	echo "$group" >> headers2.txt
	# contents=`tail -n +2 $file`
	
	while read -r line
	do
		echo "$group $short $line" >> table.txt
	done < <(tail -n +2 $file)

done

# headers
while read -r line
do
	echo -e "$line " | tr -d '[[:space:]]' >> table2.txt
	printf "  " >> table2.txt
done < <(cat headers2.txt | awk '!x[$0]++')

echo "" >> table2.txt

cp table2.txt table_tmp.txt
cat table_tmp.txt | sed -e "s/000//g" | sed -e "s/.yml//g" | sed -e "s/explicit_//g" > table2.txt

# exit 1

python3 parse.py >> table2.txt

python3 graph.py
