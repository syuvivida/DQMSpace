#!/bin/bash
source ./install_brilcalc.sh


# default: normTag + no HLT
# hlt: normTag + HLT
# none: no normTag and no HLT

mode=$3

if [ "$mode" == "default" ]; then
    brilcalc lumi -b "STABLE BEAMS" -c web --byls --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -i $1 -o $2
else
    brilcalc lumi -b "STABLE BEAMS" -c web --byls -i $1 -o $2
fi

