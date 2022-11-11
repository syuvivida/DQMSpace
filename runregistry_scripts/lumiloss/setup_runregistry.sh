#!/bin/bash
#scl enable rh-python36 bash 
source /opt/rh/rh-python36/enable
python -V 

#virtualenv -p `which python3` venv  
#source venv/bin/activate
source $PWD/setup_virtualenv.sh
pip install runregistry 
pip install matplotlib
