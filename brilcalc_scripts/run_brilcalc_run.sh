#!/bin/bash
#export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
#pip install --user brilws
#brilcalc --version

brilcalc lumi -b "STABLE BEAMS" -c web --amodetag PROTPHYS --byls \
	 --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json \
	 -r $1 -u /pb | tail -2 | head -1 | awk '{print $12}'
                                 

