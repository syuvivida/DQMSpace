# dqmsquare_mirror_scripts
Folder that contains scripts for setting up dqm^2 mirror

Github Instruction: https://github.com/cms-DQM/dqmsquare_mirror

# How I tried to set it up (but failed)

1. Log on to lxplus8 and go to my afs work area
```
ssh lxplus8.cern.ch
```

2. clone the package first
```
git clone git@github.com:cms-DQM/dqmsquare_mirror.git
cd dqmsquare_mirror
```

3. copy the setup scripts
```
wget https://raw.githubusercontent.com/syuvivida/DQMSpace/main/dqmsquare_mirror_scripts/setup_virtualenv.sh
wget https://raw.githubusercontent.com/syuvivida/DQMSpace/main/dqmsquare_mirror_scripts/setup_dqmsquare.sh
```

4. Setup a virtual environment and install all required packages
```
source setup_dqmsquare.sh
```

5. Setup DQM_PASSWORD as instructed

6. Run the python script
```
python dqmsquare_server_flask.py
```