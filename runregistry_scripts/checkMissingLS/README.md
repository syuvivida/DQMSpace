# scripts to check missing LSs in run registry
0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually

1. Check out the DQMSpace package
```
git clone -b v1.0 git@github.com:syuvivida/DQMSpace.git 
```

2. set up of run registry environment
```
cd DQMSpace/runregistry_scripts/checkMissingLS
bash
source setup_runregistry.sh
```

3. check the missing LS
```
./checkLS_inRROMS.sh 355100 355110
```

