#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

brilcalc lumi -b "STABLE BEAMS" -c web --begin $1 --end $2 -u /fb \
	--amodetag PROTPHYS\
	--normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json \
    | tail -2 | head -1 | awk '{print $12}'

