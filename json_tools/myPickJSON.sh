#!/bin/bash
## produce input.csv
## need to be in python 2.7 environment
source ./setup_json.sh 
oldJSON=$1
minRun=$2
maxRun=$3
outputJSON=$4

if [ ! -f $oldJSON ]; then
    echo "file $oldJSON does not exist!"
    exit 1
fi

##############################################################################
echo -e "\n"
echo "Now we are going to include only run ranges $minRun -- $maxRun from the JSON file $oldJSON and produce $outputJSON"
python filterJSON.py --min $minRun --max $maxRun  $oldJSON --output $outputJSON 

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "Failed to filter JSON files using filterJSON.py"
    echo "Please check the JSON format or setup"
    exit 1
fi



