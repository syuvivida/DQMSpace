#!/bin/bash
#Note, the end date needs to add 1 day
# 08/18/22 - 08/24/22
source ./install_brilcalc.sh

brilcalc lumi -c web -b "STABLE BEAMS" --byls --beamenergy 6800 \
	 --amodetag PROTPHYS\
	 --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json \
	 --begin $1' 00:00:00' --end $2' 00:00:00' -u /fb
