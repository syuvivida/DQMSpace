#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

# default: normTag + no HLT
# hlt: normTag + HLT
# none: no normTag and no HLT

mode=$3

if [ "$mode" == "default" ]; then
    brilcalc lumi -b "STABLE BEAMS" -c web --byls --amodetag PROTPHYS --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -i $1 -o $2
elif [ "$mode" == "hlt" ]; then
    brilcalc lumi -b "STABLE BEAMS" -c web --byls --amodetag PROTPHYS --hltpath="HLT_PFJet500_*" --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -i $1 -o $2
else
    brilcalc lumi -b "STABLE BEAMS" -c web --byls --amodetag PROTPHYS -i $1 -o $2
fi

