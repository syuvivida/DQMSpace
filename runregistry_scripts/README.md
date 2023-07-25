# runregistry_scripts
Folder that contains scripts to retrieve information from run registry

Full instruction of getting information from run registry with the new SSO: https://github.com/cms-DQM/runregistry_api_client/wiki/20230712_SSO_Migration 

0. Register your application to obtain your SSO client ID and secret and prepare a .env file
https://github.com/CMSTrackerDPG/cernrequests#for-cern-apis-using-the-new-sso


1. python setup
https://cern.service-now.com/service-portal?id=kb_article&sys_id=3554cdc50a0a8c0800e89d3ccb5ed4a7

```
scl enable rh-python36 bash
python -V
```

2. Setup a virtual environment
```
virtualenv -p `which python3` venv
source venv/bin/activate
```

3. Install runregistry 
```
pip install --index-url https://test.pypi.org/simple runregistry==1.0.0
```

4. Prepare a .env file following the instruction here and put in your work directory 
https://github.com/cms-DQM/runregistry_api_client/wiki/20230712_SSO_Migration#step-33-set-your-environment-variables

5. You could run all commands in one shot by sourcing the setup script
```
bash
source setup_runregistry.sh
```

6. Do a test to see if the setup is done correctly
```
python
import runregistry
run = runregistry.get_run(run_number=328762)
print(run)
```

