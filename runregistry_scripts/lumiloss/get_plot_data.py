
from collections import defaultdict
import runregistry

### SET FOLLOWING :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# - path to grid certificate
certPath = "/afs/cern.ch/user/s/syu/.globus/usercert.pem"
keyPath = "/afs/cern.ch/user/s/syu/.globus/userkey.pem"
# - dataset
dataset = "/PromptReco/Collisions2022/DQM"
# - path to JSON
path_to_json = "Cert_Collisions2022_361105_361417_Golden.json"
# - path to brilcalc output
path_to_brilcal_results = "input.csv"
# - path to our results output
results_csv = "output.csv"
### :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

### GET ALL DATA WE NEED ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import csv
brilcalc_file = open(path_to_brilcal_results, newline='') 
brilcalc_reader = csv.reader(brilcalc_file, delimiter=',')
brilcalc_lumis = defaultdict( dict )

for row in brilcalc_reader:
  if "#" in row[0] : continue
  run  = int(row[0].split(":")[0])
  lumi = int(row[1].split(":")[0])
  lumi_ = int(row[1].split(":")[1])

  delivered = float(row[5])
  recorded  = float(row[6])
  
  #if lumi != lumi_ : 
  #  print("something unusual ...")
  # print( run, lumi, lumi_, delivered, recorded )

  brilcalc_lumis[run][lumi] = [ delivered, recorded ]

import json
json_file = open( path_to_json )
json_data = json.load( json_file )

brilcalc_file = open(results_csv, "w") 
out_file  = csv.writer(brilcalc_file, delimiter='$')

for run, lumis in brilcalc_lumis.items():
  print( "process run ", run )
#  if str(run) not in json_data:
#    continue

  rr_lumisections = runregistry.get_lumisections(run, dataset)
  oms_lumisections = runregistry.get_oms_lumisections(run, dataset)


  for lumi_number, lumi_data in lumis.items():
    if lumi_number > len(rr_lumisections):
      print( "run", run, "lumi", lumi_number, "not available in rr data, skip! with size = ", len(rr_lumisections) )
      continue

    loss = True

    if str(run) in json_data:
      json_lumis = json_data[ str(run) ]
      for lumi_start, lumi_end in json_lumis :
        if lumi_number < lumi_start : continue
        if lumi_number > lumi_end   : continue
        loss = False
        break

    if loss : 
      rr_lumi = rr_lumisections[ lumi_number-1 ]
      out = {}
      for subsystem, values in rr_lumi.items():
        out[subsystem] = values['status']
      
      oms_lumi = oms_lumisections[ lumi_number-1 ]  
      for subsystem, values in oms_lumi.items():
#        print("subsystem", subsystem, ":", oms_lumi[subsystem])
        out[subsystem] = oms_lumi[subsystem]
        
      lumi_data += [ out ]
    else :
      lumi_data += [ 0 ]

    out_file.writerow( [run, lumi_number] + lumi_data )

### :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
      
























