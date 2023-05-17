#!/bin/bash

workdir=$PWD
while read -r line; do 
    $workdir/copyRun.sh $line
done < $1

