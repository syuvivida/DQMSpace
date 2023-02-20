#!/bin/bash
 
scriptname=`basename $0`
EXPECTED_ARGS=4


## produce DCS-only JSON, requiring pixel/strip in DAQ and with HV on, 
# beam present and stable
workdir=$PWD
inputFile=$workdir/testruns.txt
fromstate="OPEN"
tostate="SIGNOFF"
class="Commissioning22"

if [ $# -eq 1 ]
then
    inputFile=$1
elif [ $# -eq 3 ]
then
    inputFile=$1
    fromstate=$2
    tostate=$3
elif [ $# -eq $EXPECTED_ARGS ]
then
    inputFile=$1
    fromstate=$2
    tostate=$3
    class=$4
else
    echo "Usage: $scriptname inputFile from_state_RR to_state_RR class_name "
    echo "Example: ./$scriptname $inputFile $fromstate $tostate $class"
    echo "Available states are SIGNOFF OPEN COMPLETED"
    exit 1
fi

echo "Will install runregistry from github"
source $workdir/setup_github_runregistry.sh dev

echo -e "\n"




########################################################################################
echo -e "\n"
echo "Now we are going to change the status of runs in online run registry"

python moveRuns.py -i $inputFile -m 1 -f $fromstate -t $tostate -g $class
