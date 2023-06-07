#!/bin/bash
## produce muon and golden json

source ./setup_runregistry.sh 
inputRunFile=$1
muonJSONFile=$2
goldenJSONFile=$3
dataset=$4
class=$5

if [ ! -f $inputRunFile ]; then
    echo "The run list $inputRunFile does not exist!"
    exit 1
fi


########################################################################################
echo -e "\n"
echo "Now we are going to produce $goldenJSONFile"
testFile=test.json
python create_goldenJSON.py -i $inputRunFile -o $testFile -d $dataset -c $class

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "step json: production of golden JSON file failed!"
    echo "Likely due to the broken connection with the run registry database"
    exit 1
fi

if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi
mv $testFile $goldenJSONFile
if [ ! -f $goldenJSONFile ]; then
    echo "The file $goldenJSONFile does not exist!"
    exit 1
fi


########################################################################################
echo -e "\n"
echo "Now we are going to produce $muonJSONFile"
python create_muonJSON.py -i $inputRunFile -o $testFile -d $dataset -c $class

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "step json: production of muon JSON file failed!"
    echo "Likely due to the broken connection with the run registry database"
    echo "muon JSON file is not required for the lumiloss plots. You can proceed to the next step"
    exit 1
fi


if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi


mv $testFile $muonJSONFile
if [ ! -f $muonJSONFile ]; then
    echo "The file $muonJSONFile does not exist!"
    exit 1
fi


