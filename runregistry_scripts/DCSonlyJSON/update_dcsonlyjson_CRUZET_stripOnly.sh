#!/bin/bash
scriptname=`basename $0`
EXPECTED_ARGS=4


## produce DCS-only JSON, requiring pixel/strip in DAQ and with HV on, 
# beam present and stable
class='Cosmics24'
minRun=376824
maxRun=999999
workdir=$PWD



if [ $# -eq 1 ]
then
    class=$1
elif [ $# -eq 2 ]
then
    class=$1
    minRun=$2
elif [ $# -eq 3 ]
then
    class=$1
    minRun=$2
    maxRun=$3
elif [ $# -eq $EXPECTED_ARGS ]
then
    class=$1
    minRun=$2
    maxRun=$3
    workdir=$4
else
    echo "Usage: $scriptname classname minRun maxRun workdir"
    echo "Example: ./$scriptname $class $minRun $maxRun $workdir"
    echo "Use the default values listed above" 
fi

# first check if there is any existing json files 
# the minimum run number will be over-written
outputdir=$workdir
fileprefix=${class}_CRUZET_stripOnly

# change to work directory
echo "Change directory to $workdir"
cd $workdir
## cleaning up
rm -rf out.txt out2.txt out3.txt



existOldJSONFile=false
minRunOld=$minRun

ls -lrt ${outputdir}/${fileprefix}*.json | tee out.txt 


## If no file exits, just use the default minimum
## run number
if [ ${PIPESTATUS[0]} -ne 0 ]; then
  echo "Use minimum run number $minRun"
else    
  existOldJSONFile=true
  lastjsonfilename=`tail -n 1 out.txt | awk '{print $9}'`	
  echo "The latest JSON file created is $lastjsonfilename"
  ./myPrintJSON.sh ${lastjsonfilename} | tee out2.txt; test ${PIPESTATUS[0]} -eq 0  || exit 2
  ## The minimum run number from the latest JSON file (produced previously)
  minRunOld=`tail -n 2 out2.txt | head -n 1`
  ## Use the maximum run number from the  latest JSON file
  ## as the minimum run number for our update of JSON file
  minRun=`tail -n 1 out2.txt` 
  echo "Use minimum run number $minRun instead"
fi


echo "Run range to process: $minRun -- $maxRun"
echo "Run class: $class"
echo "Will install runregistry via pip install"
source $workdir/setup_runregistry.sh
echo -e "\n"




########################################################################################
echo -e "\n"
echo "Now we are going to produce DCS only JSON files"

if [ -d "$outputdir" ]; then
    echo "The directory $outputdir exists."
else
    echo "The directory $outputdir does not exist."
    echo "Creating a new directory $outputdir"
    mkdir -p $outputdir
fi


python3 Run2024_dcsjson_githubRR.py -min $minRun -max $maxRun -g $class -o $outputdir -zb -so

postfix='DCSOnly_TkPx.json'     
tempJSONfile=${outputdir}/${fileprefix}_${minRun}_${maxRun}_${postfix}

#tempJSONfile=`ls -lrt ${outputdir}/${fileprefix} | tail -n 1 | awk '{print $9}'` 
# Now check the maximum and minimum run numbers in the JSON file produced in this job
./myPrintJSON.sh ${tempJSONfile} | tee out3.txt;  test ${PIPESTATUS[0]} -eq 0  || exit 3 
minRunNew=`tail -n 2 out3.txt | head -n 1`
maxRunNew=`tail -n 1 out3.txt`
echo "minRunNew = " $minRunNew
echo "maxRunNew = " $maxRunNew

echo "exist old JSONfile: $existOldJSONFile"
if [ "$existOldJSONFile" == "true" ]; then 
    finalJSONfile=${outputdir}/${fileprefix}_${minRunOld}_${maxRunNew}_${postfix}
    echo "merging $lastjsonfilename and $tempJSONfile to $finalJSONfile"
    ./myMergeJSON.sh $lastjsonfilename $tempJSONfile $finalJSONfile;  test ${PIPESTATUS[0]} -eq 0  || exit 4
    rm -rf $tempJSONfile
else
    # change the name of the new JSON file to show the min/max run numbers
    finalJSONfile=${outputdir}/${fileprefix}_${minRunNew}_${maxRunNew}_${postfix}
    echo "moving file $tempJSONfile to $finalJSONfile"
    mv $tempJSONfile $finalJSONfile
fi

# Going back to the original directory
cd -
