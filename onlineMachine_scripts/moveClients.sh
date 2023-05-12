#!/bin/bash

hostname=`hostname`

idledir=/etc/appliance/dqm_resources/idle/
qrdir=/etc/appliance/dqm_resources/quarantined/
onlinedir=/etc/appliance/dqm_resources/online/

echo "-----------------------------------------------------------"
echo "in $idledir"
ls -1 $idledir
cd $idledir
sudo rm -rf *py

echo "-----------------------------------------------------------"
echo "in $qrdir"
ls -1 $qrdir
cd $qrdir
sudo rm -rf *py

echo "-----------------------------------------------------------"
echo "in $onlinedir"
ls -1 $onlinedir
cd $onlinedir
sudo rm -rf *py

echo "-----------------------------------------------------------"
echo "in $idledir"
cd $idledir


machine=`grep -a type /etc/dqm_run_config | awk '{print $3}'`
echo "It is a $machine machine"
grep -a $hostname ~/clients_${machine} | awk '{print "sudo ln -s "$2" ."}' | bash

echo "-----------------------------------------------------------"
echo "after the move"
ls -1
cd -
