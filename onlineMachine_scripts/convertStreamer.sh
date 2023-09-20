#!/bin/bash     

LS=`printf "%04d" $1`
echo "LS=${LS}"

## first do for *.dat

for file in *ls$LS*streamDQM*dat  
do 
    a=${file%%pid*}
    finalname=${a}sm-c2a11-43-01.dat
#    echo $finalname 
    ls -lrt $file
    b=${file/${LS}/"0000"}
    b2=${b%%.dat}.ini
#    echo $b2
    ls -lrt $b2
    cat $b2 $file > $finalname
done


## then do for *.pb

for file in *ls$LS*streamDQM*pb
do 
    a=${file%%pid*}
    finalname=${a}sm-c2a11-43-01.pb
#    echo $finalname 
    ls -lrt $file
    b=${file/${LS}/"0000"}
    b2=${b%%.pb}.ini
#    echo $b2
    ls -lrt $b2
    cat $b2 $file > $finalname
done
