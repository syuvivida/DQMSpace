#!/bin/bash
## produce input.csv
## need to be in python 2.7 environment
JSON=$1

if [[ ! -f $JSON ]]; then
    echo "file $JSON does not exist!"
    exit 1
fi

if [ $# -eq 1 ] 
then 
    source ./setup_json.sh 
    python printJSON.py $JSON 
elif [ $# -eq 2 ] 
then
    source ./setup_json.sh  
    python printJSON.py $JSON --$2
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







