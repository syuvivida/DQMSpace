# scripts to check missing LSs in run registry
0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually

1. set up of run registry environment
```
bash
source setup_runregistry.sh
```

2. check the missing LS
```
./checkLS_inRROMS.sh 355100 355110
```

