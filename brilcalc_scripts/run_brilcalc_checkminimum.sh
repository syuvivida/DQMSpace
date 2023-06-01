#!/bin/bash

# This is a script to check if the runs contain in a DC call has integrated 
# luminosity less than 80/nb
#
# There is only one input argument, the name of a text file that contains 
# the list of runs. 
# Inside the text file, run numbers are written in separate lines, i.e.
# 355100
# 355101
# 355102 

export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version
inputRunList=$1
miniLumi=80 #/nb
lumiUnit=nb

while read -r line; do
    lumi=`brilcalc lumi -b "STABLE BEAMS" --amodetag PROTPHYS --byls -c web -r $line -u /$lumiUnit | tail -2 | head -1 | awk '{print $12}'`  
    if (( $(echo "$lumi < $miniLumi" |bc -l) )); then
      echo "run "$line" has integrated luminosity "$lumi" /"$lumiUnit", shall be removed from the DC call"
    else   
      echo "run "$line" has integrated luminosity "$lumi" /"$lumiUnit", ok"
    fi
  done < $inputRunList

