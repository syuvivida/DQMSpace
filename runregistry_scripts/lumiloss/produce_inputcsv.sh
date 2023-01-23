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

##############################################################################
echo -e "\n"
echo "Now we are going to produce $inputJSONFile"
testFile=test.json
python create_preJSON.py -i $inputRunFile -o $testFile

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "step inputcsv: production of input JSON file failed!"
    echo "Likely due to the broken connection with the run registry database"
    exit 1
fi


if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi
mv $testFile $inputJSONFile


if [ ! -f $inputJSONFile ]; then
    echo "The file $inputJSONFile does not exist!"
    exit 1
fi


##############################################################################
echo -e "\n"
echo "Now we are going to produce $inputCSVFile"
testFile=test.csv
./run_brilcalc_inputcsv.sh $inputJSONFile $testFile

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "step inputcsv: production of input csv file failed!"
    echo "Likely due to the broken connection with brilcalc"
    exit 1
fi


if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi
mv $testFile $inputCSVFile
if [ ! -f $inputCSVFile ]; then
    echo "The file $inputCSVFile does not exist!"
    exit 1
fi

