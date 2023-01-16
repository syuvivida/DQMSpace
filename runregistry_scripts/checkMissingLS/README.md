# scripts to check missing LSs in run registry
0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually

1. Check out the DQMSpace package
```
git clone git@github.com:syuvivida/DQMSpace.git 
```

2. set up of run registry environment
```
bash
cd DQMSpace/runregistry_scripts/checkMissingLS/
```

3. check the missing LS, you can find out the usuage by running
```
./checkLS_inRROMS.sh
```

4. You can also use the default input parameters (the minimum number of input parameters is 1)
```
./checkLS_inRROMS.sh 355100 
./checkLS_inRROMS.sh 355100 355110
```


5. If you want to know the number of LSs from brilcalc, you can run the following scripts
```
./checkLS_inBrilCalcRROMS.sh 355100 
./checkLS_inBrilCalcRROMS.sh 355100 355110
```

