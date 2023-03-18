#!/bin/bash -x
PWD=`pwd`
/usr/bin/virtualenv -p `which python` venv
echo $PWD
activate () {
    . $PWD/venv/bin/activate
}

activate
