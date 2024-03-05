#!/bin/bash
scriptname=`basename $0`
EXPECTED_ARGS=3

outputFile='diffRuns_brilcalcRR.txt'
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
    outputFile=$3
else
    echo "Usage: $scriptname minRun maxRun outputFile"
    echo "Example: ./$scriptname 355100 362760 $outputFile"
    exit 1
fi

echo "Run range to process: $minRun -- $maxRun"
echo "The output of run difference check is included in $outputFile"
echo -e "\n"

# first get the list of runs from the run registry, given a run range                                                                                                                   
                                                   
source setup_runregistry.sh
runListFile='runsInRR.txt'
echo "The list of runs in the run registry is included in $runListFile"
python get_newruns.py -min $minRun -max $maxRun -o $runListFile

sort -g $runListFile > temp.txt
mv temp.txt $runListFile

echo -e "\n"



# Then check the runs in brilcalc given the same run range

source ./install_brilcalc.sh


timestamp=`date '+%Y%m%d%H%M%S'`
echo $timestamp
# Remove any postfix if the input file name has any, i.e. callRuns.txt --> callRuns                                                                                                      
temp=${runListFile%.*}
# Remove the directory name if the input file name has any, i.e. /afs/cern.ch/s/syu/callRuns --> callRuns                                                                               
prefix=${temp##*/}
echo $prefix
csvFile=${timestamp}_${prefix}.csv

echo -e "\n"
echo "Getting information without restricting to stable beams and output it to $csvFile"

brilcalc lumi --begin $minRun --end $maxRun -o $csvFile

brilcalcRunFile='runsInBrilcalc.txt'
awk '! ($0 ~ "#")' $csvFile | awk -F ":" '{print $1}' | sort -g > $brilcalcRunFile


echo "The following runs appear in brilcalc but not in run registry"
grep -vf $runListFile $brilcalcRunFile | tee $outputFile

