#!/bin/bash
 
scriptname=`basename $0`
EXPECTED_ARGS=6


## produce DCS-only JSON, requiring pixel/strip in DAQ and with HV on, 
# beam present and stable
workdir=$PWD
inputFile=$workdir/testruns.txt
fromstate="OPEN"
tostate="SIGNOFF"
class="Collisions24"
dataset="/Express/Collisions2024/DQM"
ws='tracker'

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
    dataset=$5
    ws=$6
else
    echo "Usage: $scriptname inputFile from_state_RR to_state_RR class_RR datasetname_RR workspace"
    echo "Example: ./$scriptname $inputFile $fromstate $tostate $class $dataset $ws"
    echo "Available states are SIGNOFF OPEN COMPLETED 'waiting dqm gui'"
    exit 1
fi

echo "Will install runregistry from github" 
echo "Moving from $fromstate to $tostate"
source $workdir/setup_runregistry.sh

echo -e "\n"




########################################################################################
echo -e "\n"
echo "Now we are going to change the status of runs in online run registry"

python moveDatasets.py -i $inputFile -m 1 -f "$fromstate" -t "$tostate" -g $class -n $dataset --workspace $ws
