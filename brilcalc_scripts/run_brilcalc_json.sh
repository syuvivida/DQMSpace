#!/bin/bash
source ./install_brilcalc.sh

brilcalc lumi -b "STABLE BEAMS" -c web -i $1 -u /pb --amodetag PROTPHYS\
         --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json \
    | grep -A2 totrecorded | tail -1 | awk '{print $12}'
