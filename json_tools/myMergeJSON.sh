#!/bin/bash
## produce input.csv
## need to be in python 3 environment
#source ./setup_json.sh 
JSON1=$1
JSON2=$2
outputJSON=$3

python3 checkJSON.py $JSON1

if [ $? -ne 0 ]; then
    echo "Removing this empty JSON file $JSON1"
    rm -rf $JSON1
    exit 1
fi

python3 checkJSON.py $JSON2

if [ $? -ne 0 ]; then
    echo "Removing this empty JSON file $JSON2"
    rm -rf $JSON2
    exit 1
fi


##############################################################################
echo -e "\n"
echo "Now we are going to merge the JSON files $JSON1 and $JSON2 into $outputJSON"
python3 mergeJSON.py $JSON1 $JSON2 --output=$outputJSON

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "Failed to merge JSON files using mergeJSON.py"
    echo "Please check the JSON format or setup"
    exit 1
fi



