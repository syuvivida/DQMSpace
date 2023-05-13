# Scripts to cross-check RR class

## Normal running 
0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually

To make sure the grid certificate is set up properly, please follow the instruction here to do a simple test via python interface directly. See https://github.com/syuvivida/DQMSpace/tree/v2.0/runregistry_scripts/README.md

1. Check out the DQMSpace package
```
git clone git@github.com:syuvivida/DQMSpace.git
```

2. Go to the proper directory
```
cd DQMSpace/runregistry_scripts/crossCheckRRClass
```

3. We setup a cronjob using the account cmsdqm and the script is launched every day at 7:59, 15:59, and 23:59. 
You could also run it locally, suggest to run for 20 runs maximum to avoid broken connection to run registry
```
./update_checkRRClass.sh 366000 366020
```


