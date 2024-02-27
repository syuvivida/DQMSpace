# runregistry_scripts
Folder that contains scripts to retrieve information from run registry

Full instruction of getting information from run registry with the new SSO: https://github.com/cms-DQM/runregistry_api_client/wiki/20230712_SSO_Migration 

0. Register your application to obtain your SSO client ID and secret and prepare a .env file
https://github.com/CMSTrackerDPG/cernrequests#for-cern-apis-using-the-new-sso

1. Copy all necessary files from DQMSpace to your work directory. Here, /tmp/$USER/RR is just an example. 
```
workdir=/tmp/$USER/RR
mkdir -p $workdir
cd $workdir
git clone -b pp2023 git@github.com:syuvivida/DQMSpace.git  
cp -p DQMSpace/runregistry_scripts/setup_runregistry.sh .
```

2. Put your .env file in the work directory /tmp/$USER/RR 

3. Set up the required packages for run registry
```
bash
source setup_runregistry.sh
```

4. Do a test to see if the setup is done correctly
```
python
import runregistry
run = runregistry.get_run(run_number=328762)
print(run)
```

