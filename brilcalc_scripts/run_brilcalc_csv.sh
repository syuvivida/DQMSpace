#!/bin/bash
#export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
#pip install --user brilws
#brilcalc --version
#brilcalc lumi  -c web -r $1 -u /pb | tail -2 | head -1 | awk '{print $12}'
brilcalc lumi -b "STABLE BEAMS" --byls --amodetag PROTPHYS -r $1 -o $2
awk -F "," '{print $7}' $2 > tmp.txt
~/scripts/colsum 1 tmp.txt
