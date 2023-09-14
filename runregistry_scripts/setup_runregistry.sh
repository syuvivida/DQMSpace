#!/bin/bash
/usr/bin/virtualenv -p `which python3` venv
source venv/bin/activate

pip install --upgrade pip
pip install matplotlib
pip install cernrequests
pip install runregistry



