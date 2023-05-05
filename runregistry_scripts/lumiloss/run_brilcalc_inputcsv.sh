#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

mode=$3

if [ "$mode" == "hlt" ]; then
    brilcalc lumi -c web -b "STABLE BEAMS" --byls --amodetag PROTPHYS --hltpath="HLT_PFJet500_*" -i $1 -o $2
else
    brilcalc lumi -c web -b "STABLE BEAMS" --byls --amodetag PROTPHYS -i $1 -o $2
fi

