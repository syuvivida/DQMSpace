#!/bin/bash
rm -rf $HOME/.local/bin/
rm -rf $HOME/.local/lib
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
##python -m pip install --user 'brilws==3.6.6'
pip install --user --upgrade 'brilws==3.7.4'


brilcalc --version
