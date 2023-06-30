# brilcalc_scripts
Folder that contains scripts to compute luminosity with brilcalc

# How to compute the loss of luminosity using brilcalc?

1. Download scripts from DQMSpace
```
git clone git@github.com:syuvivida/DQMSpace.git
cd DQMSpace/brilcalc_scripts
```

2. Provide a list of runs for computation

```
./run_brilcalc_runByFiles.sh inputRun
```

3. If you want to compute lumi loss, you could use the following way:
For the partially bad runs, produce a json file by running the following macro and enter the corrsponding run numbers and bad lumi sections. Note, if you do not want to enter any more lumi sections any more, type "-1 -1". If you do not want to enter any new run numbers any more, type "-1" to stop the macro.


```
root -q -b produceFakeJson.C\(\"fake.json\"\)
```

Run brilcalc for these partially bad runs using the fake.json.

```
./run_brilcalc_json.sh fake.json
```
