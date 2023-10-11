#!/bin/bash


runNumber=$1
eosDirectory=/eos/cms/store/group/comm_dqm/temp_DQMGUI_data_repository/Run2022
outputfilename=`ls $eosDirectory/*${runNumber}__EGamma*.root` 
echo $outputfilename



ReRecoNeve=`root -q -b countHisto2.C\(\"$outputfilename\",$runNumber\) | grep -a "number" | awk '{print $6}'`
echo $ReRecoNeve

eosDirectory=/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2022/EGamma
outputfilename=`ls -lrt ${eosDirectory}/*/*${runNumber}__EGamma__*PromptReco*.root | tail -n 1 | awk '{print $9}'`

echo $outputfilename


PromptRecoNeve=`root -q -b countHisto2.C\(\"$outputfilename\",$runNumber\) | grep -a "number" | awk '{print $6}'`
echo $PromptRecoNeve

outfile=$2
echo "$runNumber $PromptRecoNeve $ReRecoNeve" >> $outfile
