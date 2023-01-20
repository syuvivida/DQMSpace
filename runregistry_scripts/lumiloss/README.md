# Scripts to obtain luminosity loss figures
# Note this branch v1.0 contains the scripts for the new Golden and Muon JSON logic (used in Run 3 from call 20) 

The update is for Muon DPG/POG and ECAL. See https://github.com/syuvivida/DQMSpace/tree/v1.0/runregistry_scripts/lumiloss/goldenJSON.txt and https://github.com/syuvivida/DQMSpace/tree/v1.0/runregistry_scripts/lumiloss/muonJSON.txt 


0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually


1. Check out the DQMSpace package
```
git clone -b v1.0 git@github.com:syuvivida/DQMSpace.git
```

2. Go to the proper directory
```
bash
cd DQMSpace/runregistry_scripts/lumiloss
```

3. Prepare a text file that includes the list of runs for the period of data you want to produce luminosity loss figures and put it in your work directory. 
For example, Era/eraB_runs.txt


4. The main script is runAllSteps_lumiloss.sh. You can find out the usuage by running
```
./runAllSteps_lumiloss.sh
```

5. The script runAllSteps_lumiloss.sh can be run step by step or in one go. For longer run list, sometimes you can lose connection to the runregistry database and need to repeat certain steps. You can also use the default input parameters (the minimum number of input parameters is 1)
```
./runAllSteps_lumiloss.sh eraB
./runAllSteps_lumiloss.sh eraB inputcsv
```

6. If you run the full step (option: all), you will get the luminosity loss figures in the same directory and text file in textFiles
```
ls *png
ls textFiles/*
```


