#!/bin/bash
## produce input.csv

source ./setup_runregistry.sh 
inputRunFile=$1
inputJSONFile=$2
inputCSVFile=$3

if [ -f "$inputRunFile" ]; then
    echo "$inputRunFile exists."
else
    echo "The run list $inputRunFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce $inputJSONFile"
python create_preJSON.py -i $inputRunFile -o test.json
mv test.json $inputJSONFile


if [ -f "$inputJSONFile" ]; then
    echo "$inputJSONFile exists."
else
    echo "The file $inputJSONFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce $inputCSVFile"
./run_brilcalc_inputcsv.sh $inputJSONFile test.csv 
mv test.csv $inputCSVFile

