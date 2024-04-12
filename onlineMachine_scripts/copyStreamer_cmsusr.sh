#!/bin/bash     

run=$1
LS1=$2
LS2=$3
hostname=dqmrubu-c2a06-01-01

echo "beginning LS=${LS1}"
echo "ending LS=${LS2}"
dir=/globalscratch/run${run}_test 
mkdir -p $dir
cd $dir

for i in $(seq $LS1 $LS2); do LS=`printf "%04d" $i`; echo $LS; scp -p $USER"@"$hostname":/fff/ramdisk/run"${run}"/*${LS}*" .; done
