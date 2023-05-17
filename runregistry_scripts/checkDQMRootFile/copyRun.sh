#!/bin/bash


workdir=$PWD

runNumber=$1
eosDirectory=/eos/cms/store/group/comm_dqm/temp_DQMGUI_data_repository/Run2023
filename=`ls -lrt /data/srv-prod/state/dqmgui/offline/data/OfflineData/Run2023/JetMET0/*/*${runNumber}__JetMET0*.root | tail -n 1 | awk '{print $9}'`

outputfilename=$eosDirectory/${filename##*/} 


## this part could only be done at vocms0738 for people
## who have an account at offline DQM
cp -p $filename $eosDirectory/.
