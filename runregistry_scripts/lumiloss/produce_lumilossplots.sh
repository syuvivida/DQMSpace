#!/bin/bash
## produce input.csv

source ./setup_runregistry.sh 
outputCSVFile=$1
period=$2
outputdir=figures_${period}

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
echo "Now we are going to produce lumiloss plots in $period"
echo "using the input from $outputCSVFile"
python make_dc_plot.py -c $outputCSVFile -p $period -d $outputdir
echo "The png files are in the directory $PWD/$outputdir"
