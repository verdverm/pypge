#!/bin/bash 


DIRS=(
	01_baseline
	02_basic
	03_fitness_normalizing
	04_fitness_metrics
	05_enhanced_expansion
	06_progressive_expansion
	07_progressive_evaluation
	08_speedup
	09_final
)

a="graphing"
f="graph.sh"

for d in ${DIRS[@]}; do
	echo "#!/bin/bash" > $d/$f
	echo "" >> $d/$f
	echo "" >> $d/$f
	echo "echo \"$a $d\"" >> $d/$f
	echo "" >> $d/$f
	echo "" >> $d/$f
	$d/$f
done
