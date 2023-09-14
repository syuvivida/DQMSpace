#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

brilcalc lumi -c web -b "STABLE BEAMS" --byls --amodetag PROTPHYS -u /pb\
	 --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json \
	 -r $1 -o $2

awk -F "," '{print $7}' $2 > tmp.txt
~/scripts/colsum 1 tmp.txt
