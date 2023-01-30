#!/bin/bash

scriptname=`basename $0`
EXPECTED_ARGS=4

dir="Era"
allcallsName="call7to23"
allcallsCSV="/afs/cern.ch/work/s/syu/DQM_lumiloss_csvFiles/output_call7to23.csv"

if [ $# -eq 1 ]
then
    inputfile=$1
elif [ $# -eq 2 ]
then
    inputfile=$1
    dir=$2
elif [ $# -eq $EXPECTED_ARGS ]
then
    inputfile=$1
    dir=$2
    allcallsName=$3
    allcallsCSV=$4
else
    echo -e "\n"
    echo "===================================================================="
    echo "Usage: $scriptname inputfile directoryOfEraRuns nameofAllCalls pathofAllCSV"
    echo "Example: ./$scriptname L1T_runs.txt $dir $allcallsName $allcallsCSV"
    echo -e "\n"
    echo "directorOfEraRuns is the directory where the input run lists per Era are stored. The files are used to check the era of the updated runs."
    echo "nameofAllCalls is the name you give to the full collision period." 
    echo "pathOfAllCSV is the path of the big output csv file of all calls combined." 
    echo "===================================================================="
    echo -e "\n"
    exit 1
fi

echo -e "\n"
echo "The original run input files per Era is at $PWD/$dir"
echo -e "\n"


file=$(cat $inputfile)

outputdir=output_${dir}
rm -rf $outputdir
mkdir -p $outputdir

for line in $file
do
#    echo -e "$line\n"
    for iteration in {B,C,D,E,F,G}
    do
	#  echo $iteration
	grep -aq $line $dir/era${iteration}_runs.txt
	if [ $? -eq 0 ]; then 
	    echo -e "\n"
	    echo "$line is in Era $iteration"
	    echo -e "\n"
	    # Add new element at the end of the array
	    echo $line  >> $outputdir/era${iteration}_$inputfile
	fi
    done
done


## apart from the files per Era, we also need to update the overallJSON
allcalls_muonjson=$dir/${allcallsName}_muon.json
allcalls_muonjson_copy=$outputdir/${allcallsName}_muon.json
allcalls_muonjson_final=$outputdir/final_${allcallsName}_muon.json
cp -p $allcalls_muonjson $allcalls_muonjson_copy

allcalls_goldenjson=$dir/${allcallsName}_golden.json
allcalls_goldenjson_copy=$outputdir/${allcallsName}_golden.json
allcalls_goldenjson_final=$outputdir/final_${allcallsName}_golden.json
cp -p $allcalls_goldenjson $allcalls_goldenjson_copy


# Remove the directory name if the input file name has any, i.e. /afs/cern.ch/s/syu/callRu 
csvDir=${allcallsCSV%/*}
allcallsCSV_final=${csvDir}$/output_final_${allcallsName}.csv
cp -p $allcallsCSV $allcallsCSV_final

for iteration in {B,C,D,E,F,G}
do
    runfile=$outputdir/era${iteration}_$inputfile
    if [ -f "$runfile" ]; then
	echo "$runfile exists."
	era=era$iteration
	./runAllSteps_lumiloss.sh $era inputcsv $outputdir $runfile
	./runAllSteps_lumiloss.sh $era json $outputdir $runfile
	./runAllSteps_lumiloss.sh $era outputcsv $outputdir $runfile
	muonjson=$outputdir/original_${era}_muon.json
	muonjson_copy=$outputdir/copy_${era}_muon.json
	muonjson_final=$outputdir/final_${era}_muon.json
	cp -p $dir/${era}_muon.json $muonjson
	cp -p $dir/${era}_muon.json $muonjson_copy

	goldenjson=$outputdir/original_${era}_golden.json
	goldenjson_copy=$outputdir/copy_${era}_golden.json
	goldenjson_final=$outputdir/final_${era}_golden.json
	cp -p $dir/${era}_golden.json $goldenjson
	cp -p $dir/${era}_golden.json $goldenjson_copy

	testfile=$outputdir/output_final_${era}.csv
	cp -p $dir/output_${era}.csv $testfile
	while read -r runnumber
	do
	    echo "$runnumber"
	    #check if there is a need to replace JSON files
	    ## output the new files
	    echo -e "\n"
	    echo "Checking moun JSON files" 
	    # first delete the original lines 
	    sed -i '/"'$runnumber'"/,/^ ]/d' $muonjson_copy 
	    sed -i '/"'$runnumber'"/,/^ ]/d' $allcalls_muonjson_copy
      
	    echo -e "\n"
	    echo "Checking golden JSON files"
#	    awk '/^ "'$runnumber'"/{flag=1; next} /^ ]/{flag=0} flag' $outputdir/${era}_golden.json > $newfile
#	    sed '/"'$runnumber'"/,/^ ]/!b;//!d;/^ ]/e cat '$newfile $goldenjson > $goldenjson2
	    # first delete the original lines 
	    sed -i '/"'$runnumber'"/,/^ ]/d' $goldenjson_copy
	    sed -i '/"'$runnumber'"/,/^ ]/d' $allcalls_goldenjson_copy

	    echo -e "\n"
	    echo "replacing output csv"
	    appendfile=tmp2.txt
	    grep -e '^'$runumber'\$' output_Era/output_${era}.csv > $appendfile
	    #now loop over runs to replace outputcsv
	    sed -i -e '/^'$runnumber'/{R '$appendfile -e 'd}' $testfile
	    sed -i -e '/^'$runnumber'/{R '$appendfile -e 'd}' $allcallsCSV_final

	done < "$runfile"

	# now use mergeJSON.py, need to unsetup python2.7
	append_muonjson=$outputdir/${era}_muon.json
	./myReplaceJSON.sh $muonjson_copy $append_muonjson $muonjson_final
	./myReplaceJSON.sh $allcalls_muonjson_copy $append_muonjson $allcalls_muonjson_final
	cp -p $allcalls_muonjson_final $allcalls_muonjson_copy

	append_goldenjson=$outputdir/${era}_golden.json
	./myReplaceJSON.sh $goldenjson_copy $append_goldenjson $goldenjson_final
	./myReplaceJSON.sh $allcalls_goldenjson_copy $append_goldenjson $allcalls_goldenjson_final
	cp -p $allcalls_goldenjson_final $allcalls_goldenjson_copy

	# now compare the original JSON and the new one
	./myCompareJSON.sh $muonjson $muonjson_final
	./myCompareJSON.sh $goldenjson $goldenjson_final
    fi

done

./myCompareJSON.sh $allcalls_muonjson $allcalls_muonjson_final
./myCompareJSON.sh $allcalls_goldenjson $allcalls_goldenjson_final


