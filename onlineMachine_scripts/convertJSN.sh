#!/bin/bash     

LS=`printf "%04d" $1`
echo "LS=${LS}"
template=/eos/cms/store/group/comm_dqm/HI_testStreamers/TEST.jsn

## first do for *.dat

for file in *ls$LS*streamDQM*sm-c2a11-43-01.dat  
do 
    a=${file%%.dat*}.jsn
    echo $a	
    cp -p $template $a
    sed -i 's/FILE/'$file'/g' $a	
done

## then do for *.pb

for file in *ls$LS*streamDQM*sm-c2a11-43-01.pb  
do 
    a=${file%%.pb*}.jsn
    echo $a	
    cp -p $template $a
    sed -i 's/FILE/'$file'/g' $a	
done

