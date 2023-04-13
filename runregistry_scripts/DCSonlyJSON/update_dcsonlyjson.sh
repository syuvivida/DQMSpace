#!/bin/bash
scriptname=`basename $0`
EXPECTED_ARGS=5


## produce DCS-only JSON, requiring pixel/strip in DAQ and with HV on, 
# beam present and stable
class='Collisions23'
minRun=363380
maxRun=999999
#workdir=$PWD
workdir=/afs/cern.ch/user/s/syu/scripts/test_rr3
githubmode=1 ## by default, pick up RR from github


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
elif [ $# -eq 4 ]
then
    class=$1
    minRun=$2
    maxRun=$3
    workdir=$4
elif [ $# -eq $EXPECTED_ARGS ]
then
    class=$1
    minRun=$2
    maxRun=$3
    workdir=$4
    githubmode=$5
else
    echo "Usage: $scriptname classname minRun maxRun workdir githubmode"
    echo "Example: ./$scriptname $class $minRun $maxRun $workdir $githubmode"
    echo "Use the default values listed above" 
fi

# first check if there is any existing json files 
# the minimum run number will be over-written
outputdir=$workdir/test
fileprefix=Cert_${class}

# change to work directory
echo "Change directory to $workdir"
cd $workdir
## cleaning up
rm -rf out.txt out2.txt out3.txt out4.txt out5.txt



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
  ./myPrintJSON.sh ${lastjsonfilename} min | tee out2.txt; test ${PIPESTATUS[0]} -eq 0  || exit 1
  minRunOld=`tail -n 1 out2.txt`
  ./myPrintJSON.sh ${lastjsonfilename} max | tee out3.txt; test ${PIPESTATUS[0]} -eq 0  || exit 2
  minRun=`tail -n 1 out3.txt`
  echo "Use minimum run number $minRun instead"
fi


echo "Run range to process: $minRun -- $maxRun"
echo "Run class: $class"
if [ $githubmode -eq 0 ]
then
    echo "Will install runregistry via pip install"
    source $workdir/setup_runregistry.sh
else
    echo "Will install runregistry from github"
    source $workdir/setup_github_runregistry.sh default
fi
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


python collisions22_dcsjson_githubRR.py -min $minRun -max $maxRun -g $class -o $outputdir

postfix='DCSOnly_TkPx.json'     
tempJSONfile=${outputdir}/Cert_${class}_${minRun}_${maxRun}_${postfix}

#tempJSONfile=`ls -lrt ${outputdir}/${fileprefix} | tail -n 1 | awk '{print $9}'` 
./myPrintJSON.sh ${tempJSONfile} max | tee out4.txt;  test ${PIPESTATUS[0]} -eq 0  || exit 3 
maxRunNow=`tail -n 1 out4.txt`

echo "exist old JSONfile: $existOldJSONFile"
if [ "$existOldJSONFile" == "true" ]; then 
    finalJSONfile=${outputdir}/Cert_${class}_${minRunOld}_${maxRunNow}_${postfix}
    echo "merging $lastjsonfilename and $tempJSONfile to $finalJSONfile"
    ./myMergeJSON.sh $lastjsonfilename $tempJSONfile $finalJSONfile;  test ${PIPESTATUS[0]} -eq 0  || exit 4
    rm -rf $tempJSONfile
else
    ./myPrintJSON.sh ${tempJSONfile} min | tee out5.txt;  test ${PIPESTATUS[0]} -eq 0  || exit 5 
    minRunNow=`tail -n 1 out5.txt`
    finalJSONfile=${outputdir}/Cert_${class}_${minRunNow}_${maxRunNow}_${postfix}
    echo "moving file $tempJSONfile to $finalJSONfile"
    mv $tempJSONfile $finalJSONfile
fi

# Going back to the original directory
cd -
