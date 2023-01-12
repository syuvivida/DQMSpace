# scripts to check missing LSs in run registry
0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually

1. set up of run registry environment
```
bash
source setup_runregistry.sh
```

2. check the missing LS, you can find out the usuage by running
```
./checkLS_inRROMS.sh 355100 355110 runList.txt results.txt
```

3. You can also use the default input parameters (the minimum requirement is 1)
```
./checkLS_inRROMS.sh 355100 
```

