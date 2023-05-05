
from collections import defaultdict
import runregistry
import argparse
import sys


### SET FOLLOWING :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# - path to grid certificate

parser = argparse.ArgumentParser(description='Give list of file names')
parser.add_argument("-j", "--json",
                    dest="jsonfile", type=str, default="Era/eraB_golden.json", help="Path to golden JSON file")
parser.add_argument("-i", "--inputcsv",
                    dest="inputcsvfile", type=str, default="Era/input_eraB.csv", help="Path to input csv file")
parser.add_argument("-o", "--outputcsv",
                    dest="outputcsvfile", type=str, default="Era/output_eraB.csv", help="Path to output csv file")
parser.add_argument("-d", "--dataset",
                    dest="dataset", type=str, default="/PromptReco/Collisions2022/DQM", help="run registry dataset name")
parser.add_argument("-t", "--hlt", 
            dest="requireHLTPath", action="store_true", default=False, help="Require a specific HLT path") 


options = parser.parse_args()
print(sys.argv)


# - path to JSON
path_to_json = options.jsonfile
# - path to input csv (produced by brilcalc)
path_to_inputcsv = options.inputcsvfile
# - path to our results output
results_csv = options.outputcsvfile
### :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

### GET ALL DATA WE NEED ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import csv
brilcalc_file = open(path_to_inputcsv, newline='') 
brilcalc_reader = csv.reader(brilcalc_file, delimiter=',')
brilcalc_lumis = defaultdict( dict )

for row in brilcalc_reader:
  if "#" in row[0] : continue
  run  = int(row[0].split(":")[0])
  lumi = int(row[1].split(":")[0])
  lumi_ = int(row[1].split(":")[1])

  if options.requireHLTPath is True:
    delivered = float(row[4])
    recorded  = float(row[5])
  else:
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

  rr_lumisections = runregistry.get_lumisections(run, options.dataset)
  oms_lumisections = runregistry.get_oms_lumisections(run, options.dataset)


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
      
























