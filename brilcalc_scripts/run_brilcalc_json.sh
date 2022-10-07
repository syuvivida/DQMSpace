#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

brilcalc lumi -b "STABLE BEAMS" -c web -i $1 -u /pb | grep -A2 totrecorded | tail -1 | awk '{print $12}'
