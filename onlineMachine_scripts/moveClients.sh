#!/bin/bash

hostname=`hostname`

idledir=/etc/appliance/dqm_resources/idle/
echo "-----------------------------------------------------------"
echo "in $idledir"
ls -1 $idledir

qrdir=/etc/appliance/dqm_resources/quarantined/
echo "-----------------------------------------------------------"
echo "in $qrdir"
ls -1 $qrdir

onlinedir=/etc/appliance/dqm_resources/online/
cd $onlinedir

echo "-----------------------------------------------------------"
echo "in $onlinedir"
ls -1 

sudo rm -rf *py
machine=`grep -a type /etc/dqm_run_config | awk '{print $3}'`
echo "It is a $machine machine"
grep -a $hostname ~/clients_${machine} | awk '{print "sudo ln -s "$2" ."}' | bash

echo "-----------------------------------------------------------"
echo "after the move"
ls -1
cd -
