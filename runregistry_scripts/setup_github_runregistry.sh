#!/bin/bash

WORKDIR=$PWD
rm -rf $WORKDIR/venv
virtualenv -p `which python3` venv
source venv/bin/activate
pip install --upgrade pip
pip install matplotlib
pip install cernrequests


## By default there is no need for argument
## checkout run registry from master or pip
mode="default"
if [ $# -eq 1 ]
then
    mode=$1
fi


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
    if [ "$mode" == "default" ]; then
	git clone git@github.com:cms-DQM/runregistry.git
    else
	git clone -b $mode git@github.com:cms-DQM/runregistry.git
    fi
    export GITHUB_PATH=$RRDIR/runregistry_api_client/runregistry
fi

