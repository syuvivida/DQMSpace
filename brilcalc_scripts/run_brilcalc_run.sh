#!/bin/bash
#export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
#pip install --user brilws
#brilcalc --version
brilcalc lumi -b "STABLE BEAMS" --byls -c web -r $1 -u /pb | tail -2 | head -1 | awk '{print $12}'
#brilcalc lumi -b "STABLE BEAMS" -c web -r $1 -u /pb | tail -2 | head -1 | awk '{print $10}'                                      
                                 
#brilcalc lumi -b "STABLE BEAMS" -c web -r $1 -u /pb 

