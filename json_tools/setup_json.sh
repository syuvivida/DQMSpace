#!/bin/bash
#scl enable python27 bash 
source /opt/rh/python27/enable
python -V 

#virtualenv -p `which python2` venv  
#source venv/bin/activate
source $PWD/setup_virtualenv_python27.sh
