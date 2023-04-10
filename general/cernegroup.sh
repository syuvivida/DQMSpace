#!/bin/bash   

#input argument is a string with all run numbers
echo $1 > infile
awk -v RS='[,\n]' -v OFS="\n" '{$1=$1; print "E,,"$1}' infile > input.csv
