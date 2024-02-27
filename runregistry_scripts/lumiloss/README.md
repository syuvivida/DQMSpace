# Scripts to obtain luminosity loss figures

Example JSON logic can be found here: https://github.com/syuvivida/DQMSpace/tree/v2.0/runregistry_scripts/lumiloss/goldenJSON.txt and https://github.com/syuvivida/DQMSpace/tree/v2.0/runregistry_scripts/lumiloss/muonJSON.txt 


Note, if you need to update lumiloss figures because of an update of certain 
runs, please see point 8.

If you need to create lumiloss figure for ReReco dataset, see point 10.

## Normal running 
0. Setup SSO: register your application to obtain your SSO client ID and 
secret and prepare a .env file in your work directory
https://github.com/CMSTrackerDPG/cernrequests#for-cern-apis-using-the-new-sso

To check if your setup for the new CERN SSO is ready, please read steps 1-4 
of https://github.com/syuvivida/DQMSpace/tree/main/runregistry_scripts#readme 

Note, setup_runregistry.sh is sourced in the major script runAllSteps_lumiloss.sh mentioned below.


1. Check out the DQMSpace package
```
git clone -b pp2023 git@github.com:syuvivida/DQMSpace.git
```

2. Go to the proper directory
```
cd DQMSpace/runregistry_scripts/lumiloss
```

3. Prepare a text file that includes the list of runs for the period of data 
you want to produce luminosity loss figures and put it in your output 
directory. For example, Era/eraB_runs.txt. Note, if your input run list text 
file is not located in the output directory, you need to specify it explicitly
 (see blow).


4. The main script is runAllSteps_lumiloss.sh. You can find out the usuage by 
running
```
./runAllSteps_lumiloss.sh

=======================================================================
Usage: runAllSteps_lumiloss.sh period step outputDirName inputRunFile dataset run_class
Example: ./runAllSteps_lumiloss.sh eraB all testoutput testoutput/eraB_runs.txt /PromptReco/Collisions2023/DQM Collisions23
=======================================================================


The name of the period will be used as prefix/postfix of the output files
The inputRunFile must exist but the file path can be anywhere!
The dataset name is the name in run registry and must have corresponding run class


Steps include: all        --> running all steps (inputcsv, json, outputcsv, plot, dump)
The following options are only one step per job
               inputcsv   --> producing csv files for the input runs using brilcalc
               json       --> producing muon and golden JSON files
                              Note, only golden JSON files are required for the next step
                              If you lose connection to the DB after producing golden JSON file, you can move on to the next step
               outputcsv  --> producing run registry info for the input runs
               plot       --> make luminosity loss plots
               dump       --> dump the major lumi loss into text files


The following options run the job from step xx to the last step
               json_all       --> running json, outputcsv, plot, dump
               outputcsv_all  --> running outputcsv, plot, dump
               plot_all       --> running plot, dump

```

5. The script runAllSteps_lumiloss.sh can be run step by step, or from one 
certain step until the end, or in one go. 
For longer run list, sometimes you can lose connection to the runregistry 
database and need to repeat certain steps. 
You can also use the default input parameters (the minimum number of input 
parameters is 1). The options of steps include all, inputcsv, json, outputcsv, 
plot, dump, json_all, outputcsv_all, plot_all. 
Note, if you run the script step by step, the output directory name must be 
the same in all steps.
```
./runAllSteps_lumiloss.sh eraB
./runAllSteps_lumiloss.sh eraB inputcsv
```

6. if your input run list text file is not located in the output directory, 
you need to specify it explicitly (the last input argument).
```
./runAllSteps_lumiloss.sh eraB inputcsv outputtest Era/eraB_runs.txt
```


7. If you run the full step (option: all), you will get the luminosity loss figures in the same directory and text file in textFiles
```
ls outputtest/figures_eraB/_*png
ls outputtest/textFiles_eraB/*
```

## When you need to update luminosity loss after re-certification 
8. Note, if you need to update lumiloss figures because some subsystems 
recertify a number of runs, you can prepare an input file containing these 
runs only, say L1TRecover_runs.txt. Copy all the scripts from the 
DQMSpace/json_tools directory to your work directory and run the following 
script to get updated JSON files and output csv file. Then, run the plotting 
command. 
```
cp -p ../../json_tools/* .
./replace_outputloss.sh L1TRecover_runs.txt Era
./produce_lumilossplots.sh output_Era/output_final_eraC.csv eraC 
./produce_lumilossplots.sh <locationofbigcsv> calls7to23 output_Era
./produce_lumilossinfo.sh <locationofbigcsv> calls7to23 output_Era
```

Note, produce_lumilossplots.sh is the plotting script called by runAllSteps_lumiloss.sh. The output csv file after combining all the calls could be big so we 
suggest you to put this big CSV file in the afs work area. 


9. In some cases, you may have too many runs to process (say 100 runs), the 
chance of having broken connection with the run registry is high. 
You can use the following script to split the run list. In general, 20 runs 
per file is reasonable and the full job could finish without problems. 
```
./splitFile.sh
./splitFile.sh Era/eraC_runs.txt 20
```

## Produce luminosity loss for ReReco dataset
10. Follow the steps 0-3

11. You can modify the dataset name directly in the script runAllSteps_lumiloss.sh or add the dataset name in the input argument. 
For example
```
./runAllSteps_lumiloss.sh eraB inputcsv outputtest Era/eraB_runs.txt /ReReco/Run2022B_10Dec2022/DQM Collisions22
```


