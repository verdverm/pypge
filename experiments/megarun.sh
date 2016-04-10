#!/bin/bash

# echo ""
# echo "THIS IS GOING TO TAKE A WHILE !!!"
# echo "THIS IS GOING TO TAKE A WHILE !!!"
# echo "THIS IS GOING TO TAKE A WHILE !!!"
# echo ""
# echo ""
# echo ""

# P="-P"

# ./run.sh   -x   00_dev                         $P  -s "explicit"   -p "dev.sh"

# ./run.sh   -x   02_basic                     $P  -s "explicit"   -p "explicit_low.sh"
# ./run.sh   -x   02_basic                     $P  -s "explicit"   -p "explicit_high.sh"
# ./run.sh   -x   02_basic                     $P  -s "diffeq"     -p "diffeq_all.sh"

# ./run.sh   -x   03_fitness_metrics           $P  -s "explicit"   -p "explicit_subset.sh"
# ./run.sh   -x   03_fitness_metrics           $P  -s "diffeq"     -p "diffeq_subset.sh"

# ./run.sh   -x   04_enhance_expansion         $P  -s "explicit"   -p "explicit_subset.sh"
# ./run.sh   -x   04_enhance_expansion         $P  -s "diffeq"     -p "diffeq_subset.sh"

# ./run.sh   -x   05_progressive_expansion     $P  -s "explicit"   -p "explicit_subset.sh"
# ./run.sh   -x   05_progressive_expansion     $P  -s "diffeq"     -p "diffeq_subset.sh"

# ./run.sh   -x   06_progressive_evaluation    $P  -s "explicit"   -p "explicit_subset.sh"
# ./run.sh   -x   06_progressive_evaluation    $P  -s "diffeq"     -p "diffeq_subset.sh"

# ./run.sh   -x   07_speedup                   $P  -s "explicit"   -p "explicit_speedup.sh"
# ./run.sh   -x   07_speedup                   $P  -s "diffeq"     -p "diffeq_speedup.sh"

./run.sh   -x   08_yeast                     $P  -s "diffeq"     -p "diffeq_yeast.sh"

# ./run.sh   -x   09_final                     $P  -s "explicit"   -p "explicit_low.sh"
# ./run.sh   -x   09_final                     $P  -s "explicit"   -p "explicit_high.sh"
# ./run.sh   -x   09_final                     $P  -s "diffeq"     -p "diffeq_all.sh"

