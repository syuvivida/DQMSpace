#!/bin/bash
## produce final plots

source ./setup_runregistry.sh 
outputCSVFile=$1
period=$2
topdir=$3
outputdir=${topdir}/figures_${period}

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
#make_dc_plot.py groups muon POG and muon DPG results, 
#make_dc_plot.py groups Tracker DPG and Track POG results 
#python make_dc_plot.py -c $outputCSVFile -p $period -d $outputdir

python make_dc_plot_sub.py -c $outputCSVFile -p $period -d $outputdir

if [ $? -ne 0 ]; then
    echo -e "\n"
    echo "step plot failed!"
    exit 1
fi


echo "The png files are in the directory $PWD/$outputdir"
