#!/bin/bash

ls /data/srv/state/dqmgui/offline/uploads/0001/*root | awk '{print $1}' > outFile
removeFile=removeFile2.txt

while read -r line; do 
outputfilename=${line##*/};
echo $outputfilename
finalfilepath=`ls -lrt /data/srv-prod/state/dqmgui/offline/uploads/*/${outputfilename} | tail -n 1 | awk '{print $9}'`
echo $finalfilepath
version=`ls -lrt /data/srv-prod/state/dqmgui/offline/uploads/*/${outputfilename} | wc -l\
`
versionNumber=`printf "%04d" $version` 
echo $versionNumber

#Writing out the name of files to be removed by cmsWeb
ls /data/srv-prod/state/dqmgui/offline/uploads/*/${outputfilename} >> $removeFile
ls /data/srv-prod/state/dqmgui/offline/uploads/*/${outputfilename}.origin.bad >> $removeFile
export PATH=$PATH:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin
source /data/srv/current/apps/dqmgui/128/etc/profile.d/env.sh 
visDQMUpload http://vocms0738.cern.ch:8080/dqm/offline $finalfilepath

done < outFile

