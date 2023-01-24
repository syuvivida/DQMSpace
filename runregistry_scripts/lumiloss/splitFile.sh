#!/bin/bash

scriptname=`basename $0`
EXPECTED_ARGS=2
nlineperfile=20

if [ $# -eq 1 ]
then
    filename=$1
elif [ $# -eq $EXPECTED_ARGS ]
then
    filename=$1
    nlineperfile=$2
else
    echo "Usage: $scriptname inputFileName numberOfLinesPerFile"
    echo "Example: ./$scriptname runs.txt 20"
    exit 1
fi


iteration=0
linenumber=`wc -l $filename | awk '{print $1}'`
echo -e "\n"
echo "$filename has $linenumber lines"
echo "We will split $filename. Each subfile has $nlineperfile lines"

lastfile=$(( linenumber / nlineperfile ))
remainingLines=$(( linenumber % nlineperfile ))
echo $lastfile
echo $remainingLines

# Remove any postfix if the input file name has any, i.e. callRuns.txt --> callRuns 
temp=${filename%.*} 
# Remove the directory name if the input file name has any, i.e. /afs/cern.ch/s/syu/callRuns --> callRuns 
prefix=${temp##*/} 
echo $prefix 


while [ $iteration -lt $lastfile ]; 
do
  iteration=$(( iteration + 1 ))
  endline=$(( iteration*nlineperfile ))
  echo $endline
  head -n $endline $filename | tail -n $nlineperfile > ${prefix}_${iteration}.txt
done

# take care of the last file
if [ $remainingLines -ne 0 ]; then 
  iteration=$(( iteration + 1 ))
  tail -n $remainingLines $filename > ${prefix}_${iteration}.txt
fi


# a sanity check and make sure the split files could be combined and is equal to the original one
rm -rf tmp.txt
iteration=0
while [ $iteration -le $lastfile ]; 
do
  iteration=$(( iteration + 1 ))
  cat ${prefix}_${iteration}.txt >> tmp.txt
done


diff tmp.txt $filename
if [ $? -eq 0 ];  then
  echo "There is no difference between the produced and original files"
fi
