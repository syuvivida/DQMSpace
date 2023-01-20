#!/bin/bash
## produce input.csv

source ./setup_runregistry.sh 
goldenJSONFile=$1
inputCSVFile=$2
outputCSVFile=$3


if [ -f "$inputCSVFile" ]; then
    echo "$inputCSVFile exists."
else
    echo "The file $inputCSVFile does not exist!"
    exit 1
fi


if [ -f "$goldenJSONFile" ]; then
    echo "$goldenJSONFile exists."
else
    echo "The file $goldenJSONFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce output csv file $outputCSVFile for making lumiloss plots"
echo "using the input from $goldenJSONFile and $inputCSVFile"
python get_plot_data.py -j $goldenJSONFile -i $inputCSVFile -o $outputCSVFile

