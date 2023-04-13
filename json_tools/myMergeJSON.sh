#!/bin/bash
## produce input.csv
## need to be in python 2.7 environment
source ./setup_json.sh 
JSON1=$1
JSON2=$2
outputJSON=$3

python checkJSON.py $JSON1

if [ $? -ne 0 ]; then
    exit 1
fi

python checkJSON.py $JSON2

if [ $? -ne 0 ]; then
    exit 1
fi


##############################################################################
echo -e "\n"
echo "Now we are going to merge the JSON files $JSON1 and $JSON2 into $outputJSON"
python mergeJSON.py $JSON1 $JSON2 --output=$outputJSON

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "Failed to merge JSON files using mergeJSON.py"
    echo "Please check the JSON format or setup"
    exit 1
fi



