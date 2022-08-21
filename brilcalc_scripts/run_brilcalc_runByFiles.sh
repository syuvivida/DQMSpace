#!/bin/bash
#export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
#pip install --user brilws
#brilcalc --version
#brilcalc lumi  -c web -r $1 -u /pb | tail -2 | head -1 | awk '{print $12}'
awk '{print "./run_brilcalc_run.sh",$1}' $1 | bash > $2
~/scripts/colsum 1 $2
