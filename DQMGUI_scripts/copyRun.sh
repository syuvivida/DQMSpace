#!/bin/bash

runNumber=$1
eosDirectory=/eos/cms/store/group/comm_dqm/Commissioning2023/
echo $runNumber
filename=`ls -lrt /data/srv-prod/state/dqmgui/offline/uploads/*/*${runNumber}__StreamExpressCosmics__Commissioning2023-Express-v2__DQMIO.root | tail -n 1 | awk '{print $9}'`
version=`ls -lrt /data/srv-prod/state/dqmgui/offline/uploads/*/*${runNumber}__StreamExpressCosmics__Commissioning2023-Express-v2__DQMIO.root | wc -l`

versionNumber=`printf "%04d" $version` 
echo $versionNumber
echo $filename
outputfilename=${filename##*/} 
#newfilename=`echo "${outputfilename/V0001/V$versionNumber}"`
echo $newfilename
#cp -p $filename $eosDirectory/$newfilename
echo $filename
cp -p $filename $eosDirectory/.
