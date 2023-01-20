#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

brilcalc lumi -c web -b "STABLE BEAMS" --byls --amodetag PROTPHYS -i $1 -o $2
