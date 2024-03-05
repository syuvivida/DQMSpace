#!/bin/bash
source ./install_brilcalc.sh

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

awk -v myvar=$tempdir '{print "brilcalc lumi -c web --byls --amodetag PROTPHYS --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -r",$1," -o "myvar"/"$1".csv"}' $1 | bash

output=${timestamp}_${prefix}.csv
cat $tempdir/*.csv > $output
