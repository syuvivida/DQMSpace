#!/bin/bash
scriptname=`basename $0`
EXPECTED_ARGS=3

# check the classification of RR
minRun=367336
maxRun=999999
workdir=$PWD
#workdir=/afs/cern.ch/user/c/cmsdqm/cronjob_checkRRClass


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
    workdir=$3
else
    echo "Usage: $scriptname minRun maxRun workdir"
    echo "Example: ./$scriptname $minRun $maxRun $workdir"
    echo "Use the default values listed above" 
fi

# first check if there is any existing json files 
# the minimum run number will be over-written
#outputdir=/eos/user/c/cmsdqm/www/CAF/DQMTest
outputdir=$workdir

# change to work directory
echo "Change directory to $workdir"
cd $workdir
## cleaning up
rm -rf out*.txt


existOldJSONFile=false
minRunOld=$minRun

fileprefix=classoutput
fileprefix2=incorrect
ls -lrt ${outputdir}/${fileprefix}*.txt | tee out.txt 
ls -lrt ${outputdir}/${fileprefix2}*.txt | tee out2.txt 


## If no file exits, just use the default minimum
## run number
if [ ${PIPESTATUS[0]} -ne 0 ]; then
  echo "Use minimum run number $minRun"
else    
  existOldJSONFile=true
  lastfilename=`tail -n 1 out.txt | awk '{print $9}'`	
  echo "The latest classoutput file created is $lastfilename"
  lastfilename2=`tail -n 1 out2.txt | awk '{print $9}'`	
  echo "The latest incorrect file created is $lastfilename2"
  ## The minimum run number from the latest JSON file (produced previously)
  minRunOld=`tail -n +2 $lastfilename | awk '{print $1}' | sort -g | head -n 1`
  ## Use the maximum run number from the  latest JSON file
  ## as the minimum run number for our update of JSON file
  minRun=`tail -n +2 $lastfilename | awk '{print $1}' | sort -g | tail -n 1` 
  echo "Use minimum run number $minRun instead"
fi


echo "Run range to process: $minRun -- $maxRun"
source $workdir/setup_virtualenv_RR.sh
echo -e "\n"




########################################################################################
echo -e "\n"
echo "Now we are going to check the run class in online RR"

if [ -d "$outputdir" ]; then
    echo "The directory $outputdir exists."
else
    echo "The directory $outputdir does not exist."
    echo "Creating a new directory $outputdir"
    mkdir -p $outputdir
fi


python checkRRClassification.py -min $minRun -max $maxRun -o $outputdir

postfix='runs.txt'     
tempfile=${outputdir}/${fileprefix}_${minRun}_${maxRun}_${postfix}
tempfile2=${outputdir}/${fileprefix2}_${minRun}_${maxRun}_${postfix}
echo $tempfile
echo $tempfile2

# Now check the maximum and minimum run numbers in the JSON file produced in this job
minRunNew=`tail -n +2 $tempfile | awk '{print $1}' | sort -g | head -n 1`
maxRunNew=`tail -n +2 $tempfile | awk '{print $1}' | sort -g | tail -n 1` 

echo $minRunNew
echo $maxRunNew

echo "exist old JSONfile: $existOldJSONFile"
if [ "$existOldJSONFile" == "true" ]; then 
    finalJSONfile=${outputdir}/${fileprefix}_${minRunOld}_${maxRunNew}_${postfix}
    echo "merging $lastfilename and $tempfile to $finalJSONfile"
    head -n 1 $tempfile > out0.txt
    tail -n +2 $tempfile |sort -g > out3.txt
    tail -n +2 $lastfilename |sort -g > out4.txt
    rm -rf $tempfile
    rm -rf $lastfilename
    cat out0.txt out4.txt out3.txt > $finalJSONfile

    finalJSONfile2=${outputdir}/${fileprefix2}_${minRunOld}_${maxRunNew}_${postfix}
    echo "merging $lastfilename2 and $tempfile2 to $finalJSONfile2"
    head -n 1 $tempfile2 > out20.txt
    tail -n +2 $tempfile2 |sort -g > out23.txt
    tail -n +2 $lastfilename2 |sort -g > out24.txt
    rm -rf $tempfile2
    rm -rf $lastfilename2
    cat out20.txt out24.txt out23.txt > $finalJSONfile2
else
    # change the name of the new file to show the min/max run numbers
    finalJSONfile=${outputdir}/${fileprefix}_${minRunNew}_${maxRunNew}_${postfix}
    echo "moving file $tempfile to $finalJSONfile"
    head -n 1  $tempfile > out30.txt
    tail -n +2 $tempfile | sort -g > out33.txt
    rm -rf $tempfile
    cat out30.txt out33.txt > $finalJSONfile

    finalJSONfile2=${outputdir}/${fileprefix2}_${minRunNew}_${maxRunNew}_${postfix}
    echo "moving file $tempfile2 to $finalJSONfile2"
    head -n 1  $tempfile2 > out40.txt
    tail -n +2 $tempfile2 | sort -g > out43.txt
    rm -rf $tempfile2
    cat out40.txt out43.txt > $finalJSONfile2
fi

# Going back to the original directory
cd -
