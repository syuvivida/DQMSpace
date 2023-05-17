#!/bin/bash   

#input argument is a string with all run numbers
echo $1 > infile
awk -v OFS="\n" '$1=$1' infile | sort -g > outruns
