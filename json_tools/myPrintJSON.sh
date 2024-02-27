#!/bin/bash
## produce input.csv
## need to be in python 3 environment
JSON=$1

python3 checkJSON.py $JSON

if [ $? -ne 0 ]; then
    echo "Removing this empty JSON file $JSON"
    rm -rf $JSON
    exit 1
fi


if [ $# -eq 1 ] 
then 
    python3 printJSON.py $JSON 
elif [ $# -eq 2 ] 
then
    python3 printJSON.py $JSON --$2
else 
    echo -e "\n" 
    echo "=======================================================================" 
    echo "Usage: $scriptname jsonfile option" 
    echo "Example: ./$scriptname $JSON or ./$scriptname $JSON option" 
    echo "=======================================================================" 
    echo -e "\n"  
    ceho "options includes: range, min, max"
    exit 1 
fi 







