# scripts to produce DCS-only JSON files
0. Setup SSO: register your application to obtain your SSO client ID and  
secret and prepare a .env file in your work directory 
https://github.com/CMSTrackerDPG/cernrequests#for-cern-apis-using-the-new-sso 
 
To check if your setup for the new CERN SSO is ready, please read steps 1-4  
of https://github.com/syuvivida/DQMSpace/tree/main/runregistry_scripts#readme  
 


1. Check out the DQMSpace package
```
git clone git@github.com:syuvivida/DQMSpace.git 
```

2. Go to the proper directory
```
bash
cd DQMSpace/runregistry_scripts/DCSonlyJSON/
```

3. If you want to produce DCS-only JSON files for Collision runs. You could add more input parameters depending on the situation. See the script or type ./update_dcsonlyjson_Collisions.sh to get an idea.
```
./update_dcsonlyjson_Collisions.sh Collisions23 366000 

```

4. If you want to produce DCS-only JSON files for Cosmics runs with 3.8 Tesla. You could add more input parameters depending on the situation. See the script or type ./update_dcsonlyjson_CRAFT.sh to get an idea.
```
./update_dcsonlyjson_CRAFT.sh Cosmics23 363000 

```



