#!/bin/bash

scriptname=`basename $0`
EXPECTED_ARGS=6

runListFile='runsToCheck_bril.txt'
outputFile='checkResults_bril.txt'
maxRun=999999
class='Collisions23'
dataset='/PromptReco/Collisions2023/DQM'
    
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
    runListFile=$3
elif [ $# -eq 4 ]
then
    minRun=$1
    maxRun=$2
    runListFile=$3
    outputFile=$4
elif [ $# -eq $EXPECTED_ARGS ]
then
    minRun=$1
    maxRun=$2
    runListFile=$3
    outputFile=$4
    class=$5
    dataset=$6
else
    echo "Usage: $scriptname minRun maxRun runListFile outputFile runClass dataset"
    echo "Example: ./$scriptname 355100 362760 $runListFile $outputFile $class $dataset"           
    exit 1
fi

echo "Run range to process: $minRun -- $maxRun" 
echo "The list of runs is included in $runListFile"
echo "The output of LS check is included in $outputFile"
echo "The run class is $class and the dataset is $dataset"

echo -e "\n"

# first get newRuns 
source setup_runregistry.sh
python get_newruns.py -min $minRun -max $maxRun -o $runListFile -c $class

echo -e "\n"

sort -g $runListFile > temp.txt
mv temp.txt $runListFile


## Now produce the by LS csv files using brilcalc
#setup brilcalc
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

timestamp=`date '+%Y%m%d%H%M%S'`
echo $timestamp
# Remove any postfix if the input file name has any, i.e. callRuns.txt --> callRuns
temp=${runListFile%.*}
# Remove the directory name if the input file name has any, i.e. /afs/cern.ch/s/syu/callRuns --> callRuns
prefix=${temp##*/}
echo $prefix
tempdir=$PWD/${timestamp}_${prefix}
echo "Creating CSV files in " $tempdir
mkdir -p $tempdir

echo "Getting information without restricting to stable beams"

awk -v myvar=$tempdir '{print "brilcalc lumi -c web --byls -r",$1," -o "myvar"/"$1".csv"}' $runListFile | bash

csvFile=${timestamp}_${prefix}.csv
cat $tempdir/*.csv > $csvFile

echo "The csv file produced by brilcalc is $csvFile" 
echo -e "\n"


## Compare the LS in OMS, RR, and Brilcalc
source setup_runregistry.sh 
python compare_brilcalc_oms_rr_ls.py  -i $csvFile -o $outputFile -d $dataset


echo -e "\n"

grep -q '!' $outputFile
if [ $? -eq 0 ] 
then 
  echo "The follow runs have different number of LSs in OMS cmsActive and in offline RR!"
  grep -a '!' $outputFile
fi

grep -q '#' $outputFile
if [ $? -eq 0 ] 
then 
  echo "The follow runs have different number of LSs in OMS and in online RR!"
  grep -a '#' $outputFile
fi

grep -q '%' $outputFile
if [ $? -eq 0 ] 
then 
  echo "The follow runs have different number of LSs in OMS and in brilcalc!"
  grep -a '%' $outputFile
fi

grep -q -E '#|!|%' $outputFile 
if [ $? -ne 0 ] 
then 
  echo "The numbers of LSs match in OMS/onlineRR/offlineRR"
fi

