#!/bin/bash
scriptname=`basename $0`
EXPECTED_ARGS=5

print_steps(){
    echo -e "\n"
    echo "Steps include: all        --> running all steps (inputcsv, json, outputcsv, plot, dump)" 
    echo "The following options are only one step per job" 
    echo "               inputcsv   --> producing csv files for the input runs using brilcalc"
    echo "               json       --> producing muon and golden JSON files" 
    echo "                              Note, only golden JSON files are required for the next step"
    echo "                              If you lose connection to the DB after producing golden JSON file, you can move on to the next step"
    echo "               outputcsv  --> producing run registry info for the input runs" 
    echo "               plot       --> make luminosity loss plots"
    echo "               dump       --> dump the major lumi loss into text files"
    echo -e "\n"
    echo "The following options run the job from step xx to the last step" 
    echo "               json_all       --> running json, outputcsv, plot, dump"
    echo "               outputcsv_all  --> running outputcsv, plot, dump" 
    echo "               plot_all       --> running plot, dump"
    echo -e "\n"
}

step='all'
dir='Era'
dataset="/PromptReco/Collisions2022/DQM"
#dataset="/ReReco/Run2022B_10Dec2022/DQM"

if [ $# -eq 1 ]
then
    period=$1
    inputRunFile=${dir}/${period}_runs.txt
elif [ $# -eq 2 ]
then
    period=$1
    step=$2
    inputRunFile=${dir}/${period}_runs.txt
elif [ $# -eq 3 ]
then
    period=$1
    step=$2
    dir=$3
    inputRunFile=${dir}/${period}_runs.txt
elif [ $# -eq 4 ]
then
    period=$1
    step=$2
    dir=$3
    inputRunFile=$4
elif [ $# -eq $EXPECTED_ARGS ]
then
    period=$1
    step=$2
    dir=$3
    inputRunFile=$4
    dataset=$5
else
    echo -e "\n"
    echo "======================================================================="
    echo "Usage: $scriptname period step outputDirName inputRunFile dataset"
    echo "Example: ./$scriptname eraB $step $dir $dir/eraB_runs.txt $dataset"
    echo "======================================================================="
    echo -e "\n"
    echo "The name of the period will be used as prefix/postfix of the output files"
    echo "The inputRunFile must exist!"
    echo "The dataset name is the name in run registry"
    print_steps
    exit 1
fi

echo -e "\n"
echo "The period to process lumiloss plots is $period"
echo "We will run step $step"
echo "The output csv/JSON files are in the directory $dir"
echo "The input run file is $inputRunFile"
echo "The dataset in offline RR is $dataset"
echo -e "\n"
print_steps
# first get the list of runs from the run registry, given a run range                                                                                



if [ -d "$dir" ]; then
    echo "The directory $PWD/$dir exists."
else
    echo "The directory $PWD/$dir does not exist."
    echo "Creating a new directory $PWD/$dir"
    mkdir -p $PWD/$dir
fi

                                   

if [ ! -f $inputRunFile ]; then
    echo "The run list $inputRunFile does not exist!"
    exit 1
else 
    echo "The run list is $inputRunFile"
fi
## produce input.csv

inputJSONFile=${dir}/${period}.json
inputCSVFile=${dir}/input_${period}.csv
scriptCSV=produce_inputcsv.sh
if [[ "$step" == "inputcsv" || "$step" == "all" ]]; then
    ./$scriptCSV $inputRunFile $inputJSONFile $inputCSVFile $dataset
    if [ $? -ne 0 ]; then
	echo "step inputcsv failed!"
	exit 1
    fi
fi

if [ "$step" == "inputcsv" ]; then
    echo "The script $scriptCSV has produced the input csv file and will stop now"
    exit 0
fi

## continue to produce muon and golden JSON files
muonJSONFile=${dir}/${period}_muon.json
goldenJSONFile=${dir}/${period}_golden.json
scriptJSON=produce_json.sh

if [[ "$step" == "json" || "$step" == "all" || "$step" == "json_all" ]]; then
    ./$scriptJSON $inputRunFile $muonJSONFile $goldenJSONFile $dataset
    if [ $? -ne 0 ]; then
	echo "step json failed!"
	exit 1
    fi
fi

if [ "$step" == "json" ]; then
    echo "The script $scriptJSON has produced input the muon and golden JSON files and will stop now"
    exit 0
fi

# Now we will produce output csv file
outputCSVFile=${dir}/output_${period}.csv
scriptCSVOutput=produce_outputcsv.sh

if [[ "$step" == "outputcsv" || "$step" == "all" 
      || "$step" == "outputcsv_all" || "$step" == "json_all" ]]; then
    ./$scriptCSVOutput $goldenJSONFile $inputCSVFile $outputCSVFile $dataset
    if [ $? -ne 0 ]; then
	echo "step outputcsv failed!"
	exit 1
    fi
fi

if [ "$step" == "outputcsv" ]; then
    echo "The script $scriptCSVOutput has produced output csv files and will stop now"
    exit 0
fi


# Now we will produce lumiloss plots using the files from previous steps
scriptPlot=produce_lumilossplots.sh
if [[ "$step" == "plot" || "$step" == "all" 
	    || "$step" == "plot_all" || "$step" == "json_all" 
	    || "$step" == "outputcsv_all" ]]; then
    ./$scriptPlot $outputCSVFile $period
    if [ $? -ne 0 ]; then
	echo "step plot failed!"
	exit 1
    fi
fi

if [ "$step" == "plot" ]; then
    echo "The script $scriptPlot has produced luminosity loss plots and will stop now"
    exit 0
fi


# Now we will dump lumiloss information into text files using the files from previous steps
scriptDump=produce_lumilossinfo.sh
if [[ "$step" == "dump" || "$step" == "all" 
	    || "$step" == "plot_all" || "$step" == "json_all" 
	    || "$step" == "outputcsv_all" ]]; then
    ./$scriptDump $outputCSVFile $period
    if [ $? -ne 0 ]; then
	echo "step dump failed!"
	exit 1
    fi
fi

if [ "$step" == "dump" ]; then
    echo "The script $scriptDump has produced luminosity loss text files and will stop now"
    exit 0
fi


