# Scripts to compare regularly the difference between brilcalc and OMS

0. Setup SSO: register your application to obtain your SSO client ID and 
secret and prepare a .env file in your work directory
https://github.com/CMSTrackerDPG/cernrequests#for-cern-apis-using-the-new-sso

To check if your setup for the new CERN SSO is ready, please read steps 1-4 
of https://github.com/syuvivida/DQMSpace/tree/main/runregistry_scripts#readme 

Note, setup_runregistry.sh is sourced in the major script runCompareBrilCalcOMS.sh mentioned below.


1. Check out the DQMSpace package
```
workdir=/tmp/$USER/RR
mkdir -p $workdir
cd $workdir
git clone git@github.com:syuvivida/DQMSpace.git
```

2. Go to the proper directory
```
cd DQMSpace/runregistry_scripts/compareBrilOMS
```

3. Find out from runregistry the first run number or a run range you would like to compare. By default, runs with class Collisions24 are compared. If you want to change the run class, you need to modify compare_brilcalc_oms.py

4. The main script is runCompareBrilCalcOMS.sh. You can find out the usuage by 
running
```
./runCompareBrilCalcOMS.sh
Usage: runCompareBrilCalcOMS.sh minRun maxRun runListFile outputFile
Example: ./runCompareBrilCalcOMS.sh 355100 362760 runsToCheck_bril.txt checkResults_bril.txt
```

5. An example to check the runs starting from 378238
```
./runCompareBrilCalcOMS.sh 378238
```

6. From the screen printout of the job output, you could see the difference between brilcalc and OMS. The scripts compare the total number of LSs in which cms DAQ is active and also with stable beam. The scripts also compare lumisection by lumisection the beam_stable status and cmsActive status when the data are available in brilcalc.