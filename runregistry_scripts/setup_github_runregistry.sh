#!/bin/bash

WORKDIR=$PWD
source /opt/rh/rh-python36/enable
python -V 

source $WORKDIR/setup_virtualenv.sh
pip install requests
pip install cernrequests
pip install matplotlib

## the following command needs to be run once before sourcing this setup
# so check first if the repository exists
RRDIR=$WORKDIR/runregistry
if [ -d "$RRDIR" ]; then
  # Take action if $DIR exists. #
    cd $RRDIR
    git rev-parse --is-inside-work-tree
    if [ $? -ne 0 ]; then 
	echo "Although this directory exists, it's not a runregistry github directory!" 
	cd $WORKDIR
	exit 1
    else
	cd $WORKDIR
	export GITHUB_PATH=$RRDIR/runregistry_api_client/runregistry
	echo "The $RRDIR github exists. No need to check out from github again"
    fi
else
  # Take action if $DIR does not exist 
    #git clone -b dev git@github.com:cms-DQM/runregistry.git              
    git clone git@github.com:cms-DQM/runregistry.git
    export GITHUB_PATH=$RRDIR/runregistry_api_client/runregistry
fi

