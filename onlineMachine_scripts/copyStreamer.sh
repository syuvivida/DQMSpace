#!/bin/bash     

run=$1
LS1=$2
LS2=$3
hostname=bu-c2f11-09-01
echo "beginning LS=${LS1}"
echo "ending LS=${LS2}"
dir=/fff/output/playback_files/run${run}_test
sudo mkdir -p $dir
cd $dir

for i in $(seq $LS1 $LS2); do LS=`printf "%04d" $i`; echo $LS; sudo scp -p $USER"@"$hostname":/fff/ramdisk/run"${run}"/*${LS}*" .; done
