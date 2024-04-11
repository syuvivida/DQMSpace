#!/bin/bash
## produce output csv

source ./setup_runregistry.sh 
goldenJSONFile=$1
inputCSVFile=$2
outputCSVFile=$3
dataset=$4

if [ ! -f $inputCSVFile ]; then
    echo "The file $inputCSVFile does not exist!"
    exit 1
fi


if [ ! -f $goldenJSONFile ]; then
    echo "The file $goldenJSONFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce output csv file $outputCSVFile for making lumiloss plots"
echo "using the input from $goldenJSONFile and $inputCSVFile"
testFile=testoutput.csv


python get_plot_data.py -j $goldenJSONFile -i $inputCSVFile -o $testFile -d $dataset





if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "step outputcsv failed!"
    echo "Likely due to the broken connection with the run registry database"
    exit 1
fi


if [ ! -f $testFile ]; then
    echo "The file $testFile does not exist!"
    exit 1
fi


mv $testFile $outputCSVFile

if [ ! -f $outputCSVFile ]; then
    echo "The file $outputCSVFile does not exist!"
    exit 1
fi
