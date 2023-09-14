#!/bin/bash

workdir=$PWD
source $workdir/setup_runregistry.sh

infile=$1

outfile='temp.txt'
rm -rf $outfile
echo "Run File OMSLS DQMROOT" >> outfile


while read -r line; do 
 $workdir/countRun.sh $line $outfile
done < $infile

