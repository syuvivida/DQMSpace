# json tool script (for the time being, it only works at lxplus7)
Folder that contains scripts to merge/compare/filter JSON files

0. These scripts are basically wrapper of a few python files provided here:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile#filterJSON_py

The definition or run ranges for each Run 3 era could be found here:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun3Analysis

1. Copy all necessary files from DQMSpace to your work directory. Here, /tmp/$USER/RR is just an example. 
```
workdir=/tmp/$USER/RR
mkdir -p $workdir
cd $workdir
git clone git@github.com:syuvivida/DQMSpace.git  
```

2. Go to the json tool directory
```
cd DQMSpace/json_tools
```

3. To compare JSON files
```
./myCompareJSON.sh json1 json2
```

4. To merge JSON files
```
./myMergeJSON.sh json1 json2 newjson
```

5. To produce JSON files for a certain run ranges out of an existing JSON file
```
./myPickJSON.sh oldjson run1 run2 newjson
```

