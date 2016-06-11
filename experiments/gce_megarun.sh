#!/bin/bash

# echo ""
# echo "THIS IS GOING TO TAKE A WHILE !!!"
# echo "THIS IS GOING TO TAKE A WHILE !!!"
# echo "THIS IS GOING TO TAKE A WHILE !!!"
# echo ""
# echo ""
# echo ""

# P="-P"

# XXX ./gce_run.sh  -N  pypge-02-basic-explicit-low                           --    ./run.sh   -x   02_basic                     -P  -s "explicit"   -p "explicit_low.sh"
# ./gce_run.sh  -N  pypge-02-basic-explicit-high                          --    ./run.sh   -x   02_basic                     $P  -s "explicit"   -p "explicit_high.sh"
./gce_run.sh  -N  pypge-02-basic-diffeq-all                             --    ./run.sh   -x   02_basic                     $P  -s "diffeq"     -p "diffeq_all.sh"

# ./gce_run.sh  -N  pypge-03-fitness-normalizing-explicit-subset          --    ./run.sh   -x   03_fitness_normalizing       $P  -s "explicit"   -p "explicit_subset.sh"
# ./gce_run.sh  -N  pypge-03-fitness-normalizing-diffeq-subset            --    ./run.sh   -x   03_fitness_normalizing       $P  -s "diffeq"     -p "diffeq_subset.sh"

# ./gce_run.sh  -N  pypge-04-fitness-metrics-explicit-subset              --    ./run.sh   -x   04_fitness_metrics           $P  -s "explicit"   -p "explicit_subset.sh"
# ./gce_run.sh  -N  pypge-04-fitness-metrics-diffeq-subset                --    ./run.sh   -x   04_fitness_metrics           $P  -s "diffeq"     -p "diffeq_subset.sh"

# XXX ./gce_run.sh  -N  pypge-05-enhance-expansion-explicit-subset            --    ./run.sh   -x   05_enhance_expansion         $P  -s "explicit"   -p "explicit_subset.sh"
# XXX ./gce_run.sh  -N  pypge-05-enhance-expansion-diffeq-subset              --    ./run.sh   -x   05_enhance_expansion         $P  -s "diffeq"     -p "diffeq_subset.sh"

# ./gce_run.sh  -N  pypge-06-progressive-expansion-explicit-subset  -T n1-highmem-4      --    ./run.sh   -x   06_progressive_expansion     $P  -s "explicit"   -p "explicit_subset.sh"
# ./gce_run.sh  -N  pypge-06-progressive-expansion-diffeq-subset    -T n1-highmem-4      --    ./run.sh   -x   06_progressive_expansion     $P  -s "diffeq"     -p "diffeq_subset.sh"

# ./gce_run.sh  -N  pypge-07-progressive-evaluation-explicit-subset       --    ./run.sh   -x   07_progressive_evaluation    $P  -s "explicit"   -p "explicit_subset.sh"
# ./gce_run.sh  -N  pypge-07-progressive-evaluation-diffeq-subset         --    ./run.sh   -x   07_progressive_evaluation    $P  -s "diffeq"     -p "diffeq_subset.sh"

# ./gce_run.sh  -N  pypge-08-speedup-explicit-speedup  -T n1-standard-16  --    ./run.sh   -x   08_speedup                   $P  -s "explicit"   -p "explicit_speedup.sh"
# ./gce_run.sh  -N  pypge-08-speedup-diffeq-speedup    -T n1-standard-16  -R us-east1-d  --    ./run.sh   -x   08_speedup                   $P  -s "diffeq"     -p "diffeq_speedup.sh"

# XXX ./gce_run.sh  -N  pypge-09-final-explicit-low                           --    ./run.sh   -x   09_final                     $P  -s "explicit"   -p "explicit_low.sh"
# XXX ./gce_run.sh  -N  pypge-09-final-explicit-high                          --    ./run.sh   -x   09_final                     $P  -s "explicit"   -p "explicit_high.sh"
# XXX ./gce_run.sh  -N  pypge-09-final-diffeq-all                             --    ./run.sh   -x   09_final                     $P  -s  diffeq     -p  diffeq_all.sh

