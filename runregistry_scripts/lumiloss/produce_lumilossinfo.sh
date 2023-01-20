#!/bin/bash
## produce input.csv

source ./setup_runregistry.sh 
outputCSVFile=$1
period=$2

if [ -f "$outputCSVFile" ]; then
    echo "$outputCSVFile exists."
else
    echo "The file $outputCSVFile does not exist!"
    exit 1
fi


echo -e "\n"
echo "Now we are going to produce lumiloss text files in $period"
echo "using the input from $outputCSVFile"
python dump_lumiloss_info.py -c $outputCSVFile -p $period

