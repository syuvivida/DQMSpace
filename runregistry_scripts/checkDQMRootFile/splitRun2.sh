#!/bin/bash   

#input argument is a string with all run numbers
echo $1 > infile
awk -F, '{for(i=1;i<=NF;i++) print $i}' infile | sort -g > outruns 
