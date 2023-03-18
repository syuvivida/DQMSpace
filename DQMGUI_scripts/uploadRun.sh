#!/bin/bash

runNumber=$1
echo $runNumber
removeFile=removeFile.txt
filename=`ls -lrt /data/srv-prod/state/dqmgui/offline/uploads/*/*${runNumber}__StreamExpressCosmics__Commissioning2023-Express-v2__DQMIO.root | tail -n 1 | awk '{print $9}'`
version=`ls -lrt /data/srv-prod/state/dqmgui/offline/uploads/*/*${runNumber}__StreamExpressCosmics__Commissioning2023-Express-v2__DQMIO.root | wc -l\
`
#Writing out the name of files to be removed by cmsWeb
ls /data/srv-prod/state/dqmgui/offline/uploads/*/*${runNumber}__StreamExpressCosmics__Commissioning2023-Express-v2__DQMIO.root >> $removeFile
ls /data/srv-prod/state/dqmgui/offline/uploads/*/*${runNumber}__StreamExpressCosmics__Commissioning2023-Express-v2__DQMIO.root.origin.bad >> $removeFile
echo $version

versionNumber=`printf "%04d" $version` 
echo $versionNumber
echo $filename
export PATH=$PATH:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin
source /data/srv/current/apps/dqmgui/128/etc/profile.d/env.sh 
visDQMUpload http://vocms0738.cern.ch:8080/dqm/offline $filename
