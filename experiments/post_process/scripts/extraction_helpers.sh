#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. $DIR/utils.sh

extract_last_lines_from_errs_log () {

	inputdir=$1
	outfile=$2
	dogroup=$3

	# if [ "$dogroup" == "true" ]; then
	# 	echo "group: $dogroup"
	# fi

	declare -a files=`find $inputdir -name pge_errs.log -exec ls -d {} \;`

	rm -f $outfile
	for file in ${files[@]}; do
		if [ ! -f "$outfile" ]; then
			cols=`head -n 1 $file`
			if [ "$dogroup" == "true" ]; then
				echo "group problem $cols" > $outfile
			else
				echo "problem $cols" > $outfile			
			fi
		fi

		idx1=`strindex $file "clean"`
		idx2=`strindex $file "pge_errs.log"`
		let idx1+=6
		let end=idx2-idx1-1
		short=${file:idx1:end}

		if [ "$dogroup" == "true" ]; then
			idx1=`strindex $file "config"`
			idx2=`strindex $file "clean"`
			let idx1+=7
			let end=idx2-idx1-1
			group=${file:idx1:end}
		fi

		# echo "$group $short"

		data=`tail -1 $file`

		if [ "$dogroup" == "true" ]; then
			echo "$group $short $data" | sed -e "s/explicit_//g" -e "s/.yml//g" -e "s|/out||g" -e "s|/D|_D|g" >> $outfile
		else
			echo "$short $data" | sed -e "s/explicit_//g" -e "s/.yml//g" -e "s|/out||g" -e "s|/D|_D|g" >> $outfile
		fi

	done

}


extract_all_lines_from_errs_log () {

	inputdir=$1
	outfile=$2
	dogroup=$3

	# if [ "$group" == "true" ]; then
	# 	echo "dogroup: $dogroup"
	# fi

	declare -a files=`find $inputdir -name pge_errs.log -exec ls -d {} \;`

	rm -f $outfile

	for file in ${files[@]}; do
		if [ ! -f "$outfile" ]; then
			cols=`head -n 1 $file`
			if [ "$dogroup" == "true" ]; then
				echo "group problem $cols" > $outfile
			else
				echo "problem $cols" > $outfile			
			fi
		fi


		idx1=`strindex $file "clean"`
		idx2=`strindex $file "pge_errs.log"`
		let idx1+=6
		let end=idx2-idx1-1
		short=${file:idx1:end}

		if [ "$dogroup" == "true" ]; then
			idx1=`strindex $file "config"`
			idx2=`strindex $file "clean"`
			let idx1+=7
			let end=idx2-idx1-1
			group=${file:idx1:end}
		fi

		# echo "$group $short"

		while read -r line
		do
			if [ "$dogroup" == "true" ]; then
				echo "$group $short $line" | sed -e "s/explicit_//g" -e "s/.yml//g" -e "s|/out||g" -e "s|/D|_D|g" >> $outfile
			else
				echo "$short $line" | sed -e "s/explicit_//g" -e "s/.yml//g" -e "s|/out||g" -e "s|/D|_D|g" >> $outfile
			fi
		done < <(tail -n +2 $file)


		# data=`tail -1 $file`

		# echo "$group $short $data" >> $outfile

	done

}

extract_loop_timing_data_from_main_log () {

	inputdir=$1
	outfile=$2
	dogroup=$3

	# if [ "$group" == "true" ]; then
	# 	echo "dogroup: $dogroup"
	# fi

	declare -a files=`find $inputdir -name pge_main.log -exec ls -d {} \;`

	rm -f $outfile

	for file in ${files[@]}; do

		idx1=`strindex $file "clean"`
		idx2=`strindex $file "pge_main.log"`
		let idx1+=6
		let end=idx2-idx1-1
		short=${file:idx1:end}

		if [ "$dogroup" == "true" ]; then
			idx1=`strindex $file "config"`
			idx2=`strindex $file "clean"`
			let idx1+=7
			let end=idx2-idx1-1
			group=${file:idx1:end}
		fi

		# echo "$group $short"

		grep_str='create\|evaling\|popped\|runtime'

		while read -r line
		do
			if [ "$dogroup" == "true" ]; then
				echo "$group $short $line" | sed -e "s/explicit_//g" -e "s/.yml//g" -e "s|/out||g" -e "s|/D|_D|g" >> $outfile
			else
				echo "$short $line" | sed -e "s/explicit_//g" -e "s/.yml//g" -e "s|/out||g" -e "s|/D|_D|g" >> $outfile
			fi
		done < <(grep $grep_str $file)


		# data=`tail -1 $file`

		# echo "$group $short $data" >> $outfile

	done

}

clean_loop_timing_data () {

	infile=$1

	echo "group  problem  iteration  expand  evaluate  loop_total  running_total"

	while read -r line
	do

		declare -a tokens=${line}
		tidx=0
		last_token=""
		for token in ${tokens[@]}; do
			if [ "$tidx" -lt "3" ]; then
				if [[ $line == *"create"* ]] || [[ $line == *"popped"* ]]; then
					printf "%s  " $token
				fi
			fi

			if [ "$token" == "seconds" ]; then
				# if [[ $line != *"runtime"* ]]; then
					printf "%s  " $last_token
				# fi
			fi

			if [ "$token" == "total" ] && [ "$tidx" -gt "7" ]; then
				printf "%s  " $last_token
				echo ""
			fi



			last_token=$token
			let tidx+=1
		done

	done < <(cat $infile | sed -e "s/explicit_//g" -e "s/.yml//g" -e "s|/out||g" -e "s/e1 /e01 /g"  -e "s/e2 /e02 /g"  -e "s/e3 /e03 /g"  -e "s/e4 /e04 /g"  -e "s/e6 /e06 /g"  -e "s/e8 /e08 /g" )

}


