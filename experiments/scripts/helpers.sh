#!/bin/bash

run_experiment() {

  local systype=$1
  local experiment=$2
  local cfg=$3
  local noise=$4
  local probFields=$5


  fields=(${probFields//;/ })
  prob=${fields[0]}
  target=${fields[1]}

  # echo "  ${experiment} -- ${cfg} :: ${noise} - ${prob} - ${target}"

  cfgfile="${experiment}/${cfg}"
  inputfile="${DATA_DIR}/benchmarks/${systype}/${prob}_${noise}.csv"
  outputdir="output/${experiment}/${cfg}/${noise}/${prob}/${target}"

  mkdir -p ${outputdir}

  flags="--target ${target}"

  python3 main.py ${flags} ${cfgfile} ${inputfile} ${outputdir} > ${outputdir}/stdout.log 2> ${outputdir}/stderr.log

}

experiment_looper () {

  local systemtype=$1
  local experiment=$2
  local noiselevel=$3
  local printonly=$4
  shift 4

  declare -a problems=("${@}")
  configs=`ls ${experiment} | grep "${systemtype}" | grep yml | grep nsga2`

  PLEN=0
  for config in ${problems[@]}; do
    let PLEN+=1
  done
  CLEN=0
  for config in ${configs[@]}; do
    let CLEN+=1
  done

  echo "================================================================"
  CCNT=1
  for config in ${configs[@]}; do
    echo "----------------------------------------------------------------"
    printf "  [%2d/%d]:  %s -- %s -- %s\n" ${CCNT} ${CLEN} ${experiment} ${config} ${noiselevel}
    echo "----------------------------------------------------------------"
    
    PCNT=1

    for probFields in ${problems[@]}; do

      printf "  running [%2d/%d]:    %s\n" ${PCNT} ${PLEN} ${probFields}
      if [ "${printonly}" -eq "0" ]; then
        run_experiment ${systemtype} ${experiment} ${config} ${noiselevel} ${probFields}
      fi
      let PCNT+=1
    done
    let CCNT+=1
    echo "================================================================"
  done
}
