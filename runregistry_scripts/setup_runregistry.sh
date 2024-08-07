#!/bin/bash
/usr/bin/virtualenv -p `which python3` venv
source venv/bin/activate

pip install --upgrade pip
pip install --upgrade matplotlib
pip install --upgrade cernrequests
pip install --upgrade runregistry



