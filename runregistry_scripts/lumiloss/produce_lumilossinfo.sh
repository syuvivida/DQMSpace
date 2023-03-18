#!/bin/bash
## produce input.csv

source ./setup_runregistry.sh 
outputCSVFile=$1
period=$2
outputdir=textFiles_${period}

if [ ! -f "$outputCSVFile" ]; then
    echo "The file $outputCSVFile does not exist!"
    exit 1
fi


if [ -d "$outputdir" ];then
    echo "$outputdir directory exists."
    echo "moving the original $outputdir to tmp"
    mv $outputdir tmp
fi



echo "creating a new directory $outputdir"
mkdir -p $PWD/$outputdir


echo -e "\n"
echo "Now we are going to produce lumiloss text files in $period"
echo "using the input from $outputCSVFile"
#dump_lumiloss_info.py groups muon POG and muon DPG results, 
#dump_lumiloss_info.py groups Tracker DPG and Track POG results 
#python dump_lumiloss_info.py -c $outputCSVFile -p $period -d $outputdir

python dump_lumiloss_info_sub.py -c $outputCSVFile -p $period -d $outputdir

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "step dump failed!"
    exit 1
fi


echo -e "\n"
echo "The text files that include loss info are in the directory $PWD/$outputdir"
