#!/bin/bash -x
PWD=`pwd`
/usr/bin/virtualenv -p `which python3` venv
echo $PWD
activate () {
    . $PWD/venv/bin/activate
}

activate
