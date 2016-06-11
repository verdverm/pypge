#!/bin/bash


#Initialize variables to default values.
DEFAULT_OPT_N="pypge"
DEFAULT_OPT_T="n1-standard-4"
DEFAULT_OPT_R="us-central1-c"

HELPMSG_OPT_N="GCE machine name"
HELPMSG_OPT_T="GCE machine type"
HELPMSG_OPT_R="GCE region"

OPT_N=$DEFAULT_OPT_N
OPT_T=$DEFAULT_OPT_T
OPT_R=$DEFAULT_OPT_R

#Set fonts for Help.
NORM=`tput sgr0`
BOLD=`tput bold`
REV=`tput smso`

#Help function
function HELP {
  echo -e \\n"Help documentation for ${BOLD}${SCRIPT}.${NORM}"\\n
  echo -e "${REV}Basic usage:${NORM} ${BOLD}$SCRIPT -- run.sh${NORM}"\\n
  echo "Command line switches are optional. The following switches are recognized."
  echo "${REV}-N${NORM}  --Sets the value for option ${BOLD}n${NORM}. Default is ${BOLD}${DEFAULT_OPT_N}${NORM}."
  echo "        $HELPMSG_OPT_N"
  echo "${REV}-T${NORM}  --Sets the value for option ${BOLD}s${NORM}. Default is ${BOLD}${DEFAULT_OPT_T}${NORM}."
  echo "        $HELPMSG_OPT_M"
  echo "${REV}-R${NORM}  --Sets the value for option ${BOLD}s${NORM}. Default is ${BOLD}${DEFAULT_OPT_R}${NORM}."
  echo "        $HELPMSG_OPT_M"
  echo -e "${REV}-h${NORM}  --Displays this help message. No further functions are performed."\\n
  echo -e "Examples: "\\n
  echo -e "    ${BOLD}$SCRIPT  -N pypge   -T n1-standard-4  --  run.sh ${NORM}"\\n
  echo -e "    ${BOLD}$SCRIPT  -N diffeq  -T n1-standard-4  --  run.sh -s diffeq -x 02_basic -p diffeq_all.sh  ${NORM}"\\n
  echo -e "    ${BOLD}$SCRIPT  -N speedup -T n1-highcpu-16  --  run.sh -x 08_speedup -p explicit_speedup.sh ${NORM}"\\n
  exit 1
}

### Start getopts code ###

#Parse command line flags
#If an option should be followed by an argument, it should be followed by a ":".
#Notice there is no ":" after "h". The leading ":" suppresses error messages from
#getopts. This is required to get my unrecognized option code to work.

PRINT_ONLY=0

while getopts :N:T:R:h FLAG; do
  case $FLAG in
    N)  #set problem
      OPT_N=$OPTARG
      ;;
    T)  #set noise
      OPT_T=$OPTARG
      ;;
    R)  #set noise
      OPT_R=$OPTARG
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
if [ $NUMARGS -eq 0 ]; then
  HELP
fi


echo "Starting:  $OPT_N"
gcloud compute instances create $OPT_N \
    --image container-vm \
    --zone $OPT_R \
    --machine-type $OPT_T

# gcloud compute instances create thegp \
#     --image container-vm \
#     --machine-type n1-standard-2


echo "waiting for vm"
sleep 23


echo "  starting evalr"
gcloud compute ssh --zone $OPT_R $OPT_N --command "sudo docker run -d -p 8080:8080 --name evalr verdverm/pypge-eval"


echo "  starting pypge"
gcmd='gcloud compute ssh --zone $OPT_R '${OPT_N}' --command "sudo docker run -d -v /home/tony:/pycode/experiments/output --name pypge verdverm/pypge-experiments '$@'"'
eval $gcmd


echo "done"
echo ""

exit 0

