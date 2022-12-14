#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

timestamp=`date '+%Y%m%d%H%M%S'`
echo $timestamp
# Remove any postfix if the input file name has any, i.e. callRuns.txt --> callRuns
temp=${1%.*}
# Remove the directory name if the input file name has any, i.e. /afs/cern.ch/s/syu/callRuns --> callRuns
prefix=${temp##*/}
echo $prefix
tempdir=$PWD/${timestamp}_${prefix}
echo "Creating CSV files in " $tempdir
mkdir -p $tempdir

echo "Getting information without restricting to stable beams"

awk -v myvar=$tempdir '{print "brilcalc lumi --byls -r",$1," -o "myvar"/"$1".csv"}' $1 | bash

output=${timestamp}_${prefix}.csv
cat $tempdir/*.csv > $output
