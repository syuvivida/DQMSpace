#!/bin/bash
## produce input.csv

source ./setup_runregistry.sh 
inputRunFile=$1
muonJSONFile=$2
goldenJSONFile=$3

if [ -f "$inputRunFile" ]; then
    echo "$inputRunFile exists."
else
    echo "The run list $inputRunFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce $muonJSONFile"
python create_muonJSON.py -i $inputRunFile -o test.json
mv test.json $muonJSONFile


echo -e "\n"
echo "Now we are going to produce $goldeJSONFile"
python create_goldenJSON.py -i $inputRunFile -o test.json
mv test.json $goldenJSONFile
