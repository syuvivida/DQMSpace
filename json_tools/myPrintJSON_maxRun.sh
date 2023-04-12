#!/bin/bash
## produce input.csv
## need to be in python 2.7 environment
source ./setup_json.sh 
JSON1=$1

if [[ ! -f $JSON1 ]]; then
    echo "file $JSON1 does not exist!"
    exit 1
fi

##############################################################################
#echo -e "\n"
#echo "Now we are going to print the maximum of the old JSON file"
python printJSON.py $JSON1 --max




