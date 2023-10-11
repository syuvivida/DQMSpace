#!/bin/bash

workdir=$PWD

infile=$1

outfile='temp.txt'
rm -rf $outfile
echo "Run NPrompt NReReco" >> $outfile


while read -r line; do 
 $workdir/countRun2.sh $line $outfile
done < $infile

