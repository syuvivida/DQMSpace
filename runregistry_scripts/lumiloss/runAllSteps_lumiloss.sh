#!/bin/bash
scriptname=`basename $0`
EXPECTED_ARGS=3

step='all'
dir="Era"

if [ $# -eq 1 ]
then
    period=$1
elif [ $# -eq 2 ]
then
    period=$1
    step=$2
elif [ $# -eq $EXPECTED_ARGS ]
then
    period=$1
    step=$2
    dir=$3
else
    echo "Usage: $scriptname period step dirName"
    echo "Example: ./$scriptname eraB $step $dir"
    echo "The name of the period will be used as prefix of the csv and JSON files"
    echo "The run list $dir/period_runs.txt must exist"
    echo "Steps include: all inputcsv json outputcsv plot dump" 
    exit 1
fi

echo -e "\n"
echo "The period to process lumiloss plots is $period"
echo "We will run step $step"
echo "The input run list and output csv/JSON files are in the directory $dir"
echo -e "\n"

# first get the list of runs from the run registry, given a run range                                                                                                                   

inputRunFile=${dir}/${period}_runs.txt


## produce input.csv

inputJSONFile=${dir}/${period}.json
inputCSVFile=${dir}/input_${period}.csv
scriptCSV=produce_inputcsv.sh
if [[ "$step" == "inputcsv" || "$step" == "all" ]]; then
    ./$scriptCSV $inputRunFile $inputJSONFile $inputCSVFile
fi

if [ "$step" == "inputcsv" ]; then
    echo "The script $scriptCSV has produced the input csv file and will stop now"
    exit 0
fi

## continue to produce muon and golden JSON files
muonJSONFile=${dir}/${period}_muon.json
goldenJSONFile=${dir}/${period}_golden.json
scriptJSON=produce_json.sh

if [[ "$step" == "json" || "$step" == "all" ]]; then
    ./$scriptJSON $inputRunFile $muonJSONFile $goldenJSONFile
fi

if [ "$step" == "json" ]; then
    echo "The script $scriptJSON has produced input the muon and golden JSON files and will stop now"
    exit 0
fi

# Now we will produce output csv file
outputCSVFile=${dir}/output_${period}.csv
scriptCSVOutput=produce_outputcsv.sh

if [[ "$step" == "outputcsv" || "$step" == "all" ]]; then
    ./$scriptCSVOutput $goldenJSONFile $inputCSVFile $outputCSVFile
fi

if [ "$step" == "outputcsv" ]; then
    echo "The script $scriptCSVOutput has produced output csv files and will stop now"
    exit 0
fi


# Now we will produce lumiloss plots using the files from previous steps
scriptPlot=produce_lumilossplots.sh
if [[ "$step" == "plot" || "$step" == "all" ]]; then
    ./$scriptPlot $outputCSVFile $period
fi

if [ "$step" == "plot" ]; then
    echo "The script $scriptPlot has produced luminosity loss plots and will stop now"
    exit 0
fi


# Now we will dump lumiloss information into text files using the files from previous steps
scriptDump=produce_lumilossinfo.sh
if [[ "$step" == "dump" || "$step" == "all" ]]; then
    ./$scriptDump $outputCSVFile $period
fi

if [ "$step" == "dump" ]; then
    echo "The script $scriptDump has produced luminosity loss text files and will stop now"
    exit 0
fi


