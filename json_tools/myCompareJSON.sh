#!/bin/bash
## produce input.csv
## need to be in python 2.7 environment
source ./setup_json.sh 
JSON1=$1
JSON2=$2

if [[ ! -f $JSON1 || ! -f $JSON2 ]]; then
    echo "Either file $JSON1 or file $JSON2 does not exist!"
    exit 1
fi

##############################################################################
echo -e "\n"
echo "Now we are going to compare the original JSON $JSON1 and the modified JSON $JSON2"
python compareJSON.py --diff $JSON1 $JSON2 




