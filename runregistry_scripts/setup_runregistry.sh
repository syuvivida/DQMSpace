#!/bin/bash
source /opt/rh/rh-python36/enable
python -V 

source $PWD/setup_virtualenv.sh
pip install runregistry 
pip install matplotlib
pip install cernrequests==0.3.3

#pip install pyplot

