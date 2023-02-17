#!/bin/bash
 
scriptname=`basename $0`
EXPECTED_ARGS=3


## produce DCS-only JSON, requiring pixel/strip in DAQ and with HV on, 
# beam present and stable
workdir=$PWD
githubmode=1 ## by default, pick up RR from github
maxRun=999999

if [ $# -eq 1 ]
then
    minRun=$1
elif [ $# -eq 2 ]
then
    minRun=$1
    maxRun=$2
elif [ $# -eq $EXPECTED_ARGS ]
then
    minRun=$1
    maxRun=$2
    githubmode=$3
else
    echo "Usage: $scriptname minRun maxRun githubmode"
    echo "Example: ./$scriptname 355100 $maxRun 1"
    exit 1
fi

echo "Run range to process: $minRun -- $maxRun"
if [ $githubmode -eq 0 ]
then
    echo "Will install runregistry via pip install"
    source $workdir/setup_runregistry.sh
else
    echo "Will install runregistry from github"
    source $workdir/setup_github_runregistry.sh
fi
echo -e "\n"




########################################################################################
echo -e "\n"
echo "Now we are going to produce DCS only JSON files"
python collisions22_dcsjson_githubRR.py -min $minRun -max $maxRun
