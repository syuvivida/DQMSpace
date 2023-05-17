# scripts to compare the number of LSs in CMS-active (OMS) and DQMGUI root files
0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually

1. Check out the DQMSpace package
```
git clone git@github.com:syuvivida/DQMSpace.git 
```

2. Go to the proper directory
```
bash
cd DQMSpace/runregistry_scripts/checkDQMRootFile/
```

3. If you do not have an account of offline DQMGUI server (vocms0738), ask conveners to do the copy of DQM root files to eos. 
Before that, please pass the conveners a list of runs for the DC call: call1.txt
If you do have an account 
```
./copyAllRuns.sh call1.txt
```

4. Now you can compare the number of LSs and look for the runs that have big difference
```
./countAllRuns.sh call1.txt
```


5. The output is temp.txt

