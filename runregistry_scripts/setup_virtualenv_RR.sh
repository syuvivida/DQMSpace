#!/bin/bash
source /opt/rh/rh-python36/enable
python -V 

PWD=`pwd`
/usr/bin/virtualenv -p `which python3` venv
echo $PWD
activate () {
    . $PWD/venv/bin/activate
}

activate

pip install runregistry 
