# Scripts to obtain luminosity loss figures
# Note this branch v0.0 contains the scripts for the old Golden and Muon JSON logic (used in Run 2 and Run 3 before call 20)

See https://github.com/syuvivida/DQMSpace/tree/v0.0/runregistry_scripts/lumiloss/goldenJSON.txt and https://github.com/syuvivida/DQMSpace/tree/v0.0/runregistry_scripts/lumiloss/muonJSON.txt

0. Setup grid certificate
https://github.com/cms-DQM/runregistry/tree/master/runregistry_api_client#provide-the-certificate-manually

1. Setup the runregistry and python environment (note setup_runregistry.sh calls setup_virtualenv.sh)
```
bash
source setup_runregistry.sh
```

2. Use the run registry JSON portal to create two JSON files. The first one is the JSON file that satifies the preselection of beam status (see JSON ID 825, note run range shall be varied). The second one is the Golden JSON file for your call. https://cmsrunregistry.web.cern.ch/json_portal

3. Produce an input csv file using the first JSON file (with only requirement of run range and beam status) 
```
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH 
pip install --user brilws 
brilcalc lumi -c web --byls -i call19_all.json -o input.csv
```

4. Prepare an output csv file that contains the DQM flags and DCS information. Note you need to modify the following lines in get_plot_data.py for your correspondin file names

```
certPath = "/afs/cern.ch/user/s/syu/.globus/usercert.pem" 
keyPath = "/afs/cern.ch/user/s/syu/.globus/userkey.pem" 
path_to_json = "Cert_Collisions2022_361105_361417_Golden.json" 
path_to_brilcal_results = "input.csv" 
results_csv = "output.csv" 
```

Then, run the python script
```
python get_plot_data.py
```

5. If you change the name of the output csv file from step4, please remember to change the file name in make_dc_plot.py as well. 

```
results_csv = "output.csv"
```

Then, run the python script

```
python make_dc_plot.py
```

6. See output figures for call 19 in the directory example_figures
