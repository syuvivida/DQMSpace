#!/bin/bash     

run=$1
LS1=$2
LS2=$3
hostname=bu-c2f11-09-01

echo "beginning LS=${LS1}"
echo "ending LS=${LS2}"
dir=/tmp/run${run}_test 
mkdir -p $dir
cd $dir

for i in $(seq $LS1 $LS2); do LS=`printf "%04d" $i`; echo $LS; scp -p $USER"@"$hostname":/fff/ramdisk/run"${run}"/*${LS}*" .; done
