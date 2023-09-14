#!/bin/bash
 
scriptname=`basename $0`
EXPECTED_ARGS=4


## produce DCS-only JSON, requiring pixel/strip in DAQ and with HV on, 
# beam present and stable
workdir=$PWD
githubmode=1 ## by default, pick up RR from github
maxRun=999999
class='Collisions22'

if [ $# -eq 1 ]
then
    minRun=$1
elif [ $# -eq 2 ]
then
    minRun=$1
    maxRun=$2
elif [ $# -eq 3 ]
then
    minRun=$1
    maxRun=$2
    class=$3
elif [ $# -eq $EXPECTED_ARGS ]
then
    minRun=$1
    maxRun=$2
    class=$3
    githubmode=$4
else
    echo "Usage: $scriptname minRun maxRun classname githubmode"
    echo "Example: ./$scriptname 355100 $maxRun $class 1"
    exit 1
fi

echo "Run range to process: $minRun -- $maxRun"
echo "Run class: $class"
if [ $githubmode -eq 0 ]
then
    echo "Will install runregistry via pip install"
    source $workdir/setup_runregistry.sh
else
    echo "Will install runregistry from github"
    source $workdir/setup_github_runregistry.sh default
fi
echo -e "\n"




########################################################################################
echo -e "\n"
echo "Now we are going to produce DCS only JSON files"
outputdir=$PWD/test

if [ -d "$outputdir" ]; then
    echo "The directory $outputdir exists."
else
    echo "The directory $outputdir does not exist."
    echo "Creating a new directory $outputdir"
    mkdir -p $outputdir
fi


python collisions22_dcsjson_githubRR.py -min $minRun -max $maxRun -g $class -o $outputdir
