#!/bin/bash
source /opt/rh/rh-python36/enable
python -V 

source $PWD/setup_virtualenv.sh
pip install matplotlib
pip install cernrequests>=0.4.1
pip install --index-url https://test.pypi.org/simple runregistry==1.0.0


#pip install pyplot

