#!/bin/bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
#brilcalc --version

awk '{print "./run_brilcalc_run.sh",$1}' $1 | bash > testlumi.txt
./colsum 1 testlumi.txt
