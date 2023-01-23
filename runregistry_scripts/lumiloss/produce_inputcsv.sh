#!/bin/bash
## produce input.csv

source ./setup_runregistry.sh 
inputRunFile=$1
inputJSONFile=$2
inputCSVFile=$3

if [ ! -f $inputRunFile ]; then
    echo "The run list $inputRunFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce $inputJSONFile"
testFile=test.json
python create_preJSON.py -i $inputRunFile -o $testFile
if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi
mv $testFile $inputJSONFile


if [ ! -f $inputJSONFile ]; then
    echo "The file $inputJSONFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce $inputCSVFile"
testFile=test.csv
./run_brilcalc_inputcsv.sh $inputJSONFile $testFile
if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi
mv $testFile $inputCSVFile
if [ ! -f $inputCSVFile ]; then
    echo "The file $inputCSVFile does not exist!"
    exit 1
fi

