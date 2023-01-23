#!/bin/bash
## produce input.csv

source ./setup_runregistry.sh 
inputRunFile=$1
muonJSONFile=$2
goldenJSONFile=$3

if [ ! -f $inputRunFile ]; then
    echo "The run list $inputRunFile does not exist!"
    exit 1
fi



echo -e "\n"
echo "Now we are going to produce $goldenJSONFile"
testFile=test.json
python create_goldenJSON.py -i $inputRunFile -o $testFile
if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi
mv $testFile $goldenJSONFile
if [ ! -f $goldenJSONFile ]; then
    echo "The file $goldenJSONFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce $muonJSONFile"
python create_muonJSON.py -i $inputRunFile -o $testFile
if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi
mv $testFile $muonJSONFile
if [ ! -f $muonJSONFile ]; then
    echo "The file $muonJSONFile does not exist!"
    exit 1
fi

