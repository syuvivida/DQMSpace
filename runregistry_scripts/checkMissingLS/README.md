# scripts to check 
Folder that contains scripts to retrieve information from run registry

Github Instruction of getting information from run registry: https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client 

0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually

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
pip install runregistry
```

4. You could run all commands in one shot by sourcing the setup script
```
bash
source setup_runregistry.sh
```

5. Do a test to see if the setup is done correctly
```
python
import runregistry
run = runregistry.get_run(run_number=328762)
print(run)
```

