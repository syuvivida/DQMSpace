#!/bin/bash


runNumber=$1
eosDirectory=/eos/cms/store/group/comm_dqm/temp_DQMGUI_data_repository/Run2023
outputfilename=`ls $eosDirectory/*${runNumber}__JetMET0*.root` 
echo $outputfilename


OMSLS=`python get_cmsActiveLS.py -r $runNumber`
echo $OMSLS

#root -q -b countHisto.C\(\"$outputfilename\",$OMSLS\)

ROOTLS=`root -q -b countHisto.C\(\"$outputfilename\",$OMSLS\) | grep -a "no-zero" | awk '{print $8}'`

outfile=$2
echo "$runNumber $outputfilename $OMSLS $ROOTLS" >> $outfile
