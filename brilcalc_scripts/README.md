# brilcalc_scripts
Folder that contains scripts to compute luminosity loss for a certain subsystem

# How to compute the loss of luminosity using brilcalc?

0. Install brilcalc using the commands in install_brilcalc.sh (bash commands)

1. Go to the run registry web site

https://cmsrunregistry.web.cern.ch/offline/datasets/global

2. Find out the run lists that are bad for a certain subsystem

Click on "+Rule" and choose a proper run range for a certain cycle by using "run_number" ">=" and "run_number" "<=" and require a subsystem status to be bad.

3. From the information of run registry, find out the runs that are totally bad (all lumi sections are bad) or the ones that are partially bad. Produce a text file that includes the runs that are totally bad and type the following command to get the total recorded luminosity in /pb for these totally bad runs

```
./run_brilcalc_runByFiles.sh inputRun
```

4. For the partially bad runs, produce a json file by running the following macro and enter the corrsponding run numbers and bad lumi sections. Note, if you do not want to enter any more lumi sections any more, type "-1 -1". If you do not want to enter any new run numbers any more, type "-1" to stop the macro.


```
root -q -b produceFakeJson.C\(\"fake.json\"\)
```

5. Run brilcalc for these partially bad runs using the fake.json.

```
./run_brilcalc_json.sh fake.json
```
