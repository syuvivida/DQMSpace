#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

brilcalc lumi -b "STABLE BEAMS" -i $1 -u /pb --amodetag PROTPHYS\
         --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json \
    | grep -A2 totrecorded | tail -1 | awk '{print $12}'
