#!/bin/bash

DATA_DIR="../data"
PROB_SET_DIR="prob_sets"

. scripts/helpers.sh

#Set Script Name variable
SCRIPT=`basename ${BASH_SOURCE[0]}`

#Initialize variables to default values.
DEFAULT_OPT_S="explicit"
DEFAULT_OPT_X="09_final"
DEFAULT_OPT_P="explicit_subset.sh"
DEFAULT_OPT_N="clean"

HELPMSG_OPT_S="System Tpye: Can be one of [explicit,diffeq]"
HELPMSG_OPT_X="Experiment:  Can be any directory in the experiments folder"
HELPMSG_OPT_P="Problem Set: Can be any file in the prob_sets directory"
HELPMSG_OPT_N="Noise Level: Can be one of [clean,noisy]"

OPT_S=$DEFAULT_OPT_S
OPT_X=$DEFAULT_OPT_X
OPT_P=$DEFAULT_OPT_P
OPT_N=$DEFAULT_OPT_N

#Set fonts for Help.
NORM=`tput sgr0`
BOLD=`tput bold`
REV=`tput smso`

#Help function
function HELP {
  echo -e \\n"Help documentation for ${BOLD}${SCRIPT}.${NORM}"\\n
  echo -e "${REV}Basic usage:${NORM} ${BOLD}$SCRIPT${NORM}"\\n
  echo "Command line switches are optional. The following switches are recognized."
  echo "${REV}-s${NORM}  --Sets the value for option ${BOLD}s${NORM}. Default is ${BOLD}${DEFAULT_OPT_S}${NORM}."
  echo "        $HELPMSG_OPT_S"
  echo "${REV}-x${NORM}  --Sets the value for option ${BOLD}x${NORM}. Default is ${BOLD}${DEFAULT_OPT_X}${NORM}."
  echo "        $HELPMSG_OPT_X"
  echo "${REV}-p${NORM}  --Sets the value for option ${BOLD}p${NORM}. Default is ${BOLD}${DEFAULT_OPT_P}${NORM}."
  echo "        $HELPMSG_OPT_P"
  echo "${REV}-n${NORM}  --Sets the value for option ${BOLD}n${NORM}. Default is ${BOLD}${DEFAULT_OPT_N}${NORM}."
  echo "        $HELPMSG_OPT_N"
  echo -e "${REV}-P${NORM}  --Doesn't run the experiments, just prints what they would be."\\n
  echo -e "${REV}-h${NORM}  --Displays this help message. No further functions are performed."\\n
  echo -e "Examples: "\\n
  echo -e "    ${BOLD}$SCRIPT -x 09_final -p explicit_all.sh -n clean ${NORM}"\\n
  echo -e "    ${BOLD}$SCRIPT -s diffeq -x 02_basic -p diffeq_all.sh  ${NORM}"\\n
  echo -e "    ${BOLD}$SCRIPT -s explicit -x 04_fitness_metrics -p explicit_subset.sh -n clean ${NORM}"\\n
  exit 1
}

### Start getopts code ###

#Parse command line flags
#If an option should be followed by an argument, it should be followed by a ":".
#Notice there is no ":" after "h". The leading ":" suppresses error messages from
#getopts. This is required to get my unrecognized option code to work.

PRINT_ONLY=0

while getopts :s:x:p:n:Ph FLAG; do
  case $FLAG in
    s)  #set experiment
      OPT_S=$OPTARG
      # echo "-x used: $OPTARG"
      # echo "OPT_S = $OPT_S"
      ;;
    x)  #set experiment
      OPT_X=$OPTARG
      # echo "-x used: $OPTARG"
      # echo "OPT_X = $OPT_X"
      ;;
    p)  #set problem
      OPT_P=$OPTARG
      # echo "-p used: $OPTARG"
      # echo "OPT_P = $OPT_P"
      ;;
    n)  #set noise
      OPT_N=$OPTARG
      # echo "-n used: $OPTARG"
      # echo "OPT_N = $OPT_N"
      ;;
    P)  #set debug (print only, no experiments)
      echo "Printing only, no experiments will be run"
      let PRINT_ONLY=1
      ;;
    h)  #show help
      HELP
      ;;
    \?) #unrecognized option - show help
      echo -e \\n"Option -${BOLD}$OPTARG${NORM} not allowed."
      HELP
      #If you just want to display a simple error message instead of the full
      #help, remove the 2 lines above and uncomment the 2 lines below.
      #echo -e "Use ${BOLD}$SCRIPT -h${NORM} to see the help documentation."\\n
      #exit 2
      ;;
  esac
done

shift $((OPTIND-1))  #This tells getopts to move on to the next argument.

### End getopts code ###


### Main loop to run experiment ###

#Check the number of arguments. If none are passed, print help and exit.
NUMARGS=$#
# echo -e \\n"Number of arguments: $NUMARGS"
if [ $NUMARGS -ne 0 ]; then
  HELP
fi

## Check the args values
if [ "$OPT_S" != "explicit" ] && [ "$OPT_S" != "diffeq" ] ; then
  echo "Unknown system type: $OPT_S."
  echo "  $HELPMSG_OPT_S"
  exit 1
fi

if [ ! -d "$OPT_X" ]; then
  echo "Experiment directory does not exist [./${OPT_X}]"
  echo "  $HELPMSG_OPT_X"
  exit 1
fi

PFILE="${PROB_SET_DIR}/${OPT_P}"
if [ ! -f "$PFILE" ]; then
  echo "Problem Set file does not exist [${PFILE}]"
  echo "  $HELPMSG_OPT_P"
  exit 1
fi

if [ "$OPT_N" != "clean" ] && [ "$OPT_N" != "noisy" ] ; then
  echo "Unknown noise level: $OPT_N."
  echo "  $HELPMSG_OPT_N"
  exit 1
fi

# source the problem file
. ${PFILE}

echo "Starting with options:"
echo "  systemtype:    $OPT_S"
echo "  experiment:    $OPT_X"
echo "  noiselevel:    $OPT_N"
echo "  problemset:    $OPT_P"
for p in ${problems[@]}; do
  echo "    - $p"
done

echo ""
echo ""



experiment_looper ${OPT_S} ${OPT_X} ${OPT_N} ${PRINT_ONLY} ${problems[@]}



exit 0







