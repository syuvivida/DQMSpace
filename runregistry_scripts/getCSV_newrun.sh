#!/bin/bash
# first get newRuns 
source setup_runregistry.sh
python get_newruns.py -min $1

# Then run brilcalc

source ./install_brilcalc.sh


timestamp=`date '+%Y%m%d%H%M%S'`
echo $timestamp
prefix=newRuns
echo $prefix
tempdir=$PWD/${timestamp}_${prefix}
echo "Creating CSV files in " $tempdir
mkdir -p $tempdir

echo "Getting information without restricting to stable beams"

awk -v myvar=$tempdir '{print "brilcalc lumi --byls -r",$1," -o "myvar"/"$1".csv"}' newRuns | bash

cd $tempdir

for file in *csv; do sed -i '/#/d' $file; done; 

cd -
