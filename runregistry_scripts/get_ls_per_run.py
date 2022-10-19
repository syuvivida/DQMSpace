from collections import defaultdict
import runregistry
import json
import argparse
import sys

### SET FOLLOWING :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# - path to grid certificate
# - dataset
dataset = "/PromptReco/Collisions2022/DQM"
### :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

parser = argparse.ArgumentParser(description='Give list of runs from csv')
parser.add_argument("-o", "--output",
                    dest="outfile", type=str, default="test.txt", help="Output file name")
parser.add_argument("-i", "--input",
                    dest="csvfile", type=str, default="call16.csv", help="Input CSV file name")

options = parser.parse_args()

# - path to brilcalc output
path_to_brilcal_results = options.csvfile


### GET ALL DATA WE NEED ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import csv
brilcalc_file = open(path_to_brilcal_results, newline='') 
brilcalc_reader = csv.reader(brilcalc_file, delimiter=',')
brilcalc_lumis = defaultdict( dict )


sys.stdout = open(options.outfile, "w")

print("Run number, Offline RR LS, LS Duration (Online RR), OMS LS, brilcalc LS")

for row in brilcalc_reader:
  if "#" in row[0] : continue
  run  = row[0].split(":")[0]
  lumi = row[1].split(":")[0]
  lumi_ = row[1].split(":")[1]

  delivered = row[5]
  recorded  = row[6]

  brilcalc_lumis[int(run)][int(lumi)] = [ float(delivered), float(recorded) ]


for run, lumis in brilcalc_lumis.items():
  rr_run = runregistry.get_run(run)
  if type(rr_run) != type({}) : continue
  if "significant" not in rr_run : continue
  if not rr_run["significant"] : continue
   ## Need to have the dataset /PromptReco/Collisions2022/DQM
  if dataset not in runregistry.get_dataset_names_of_run(run): continue

  ## Number of LS in DCS bits (offline RR)
  rr_lumisections = len(runregistry.get_lumisections(run, dataset))
  ## Number of LS from online RR (also LS Duration in offline RR)
  rr_ls_duration = len(runregistry.get_lumisections(run))

  ## Number of LS from brilcalc
  ls_brilcalc = len(lumis)

  ls_oms = len(runregistry.get_oms_lumisections(run))
#  ls_oms = len(runregistry.get_oms_lumisections(run,dataset))
#  print(run, ls_oms) 

  if rr_lumisections != rr_ls_duration: 
    print( run, rr_lumisections, rr_ls_duration, ls_oms, ls_brilcalc, "! -->") 
  elif rr_ls_duration < ls_brilcalc or ls_oms < ls_brilcalc:
    print( run, rr_lumisections, rr_ls_duration, ls_oms, ls_brilcalc, "#") 
  else: 
    print( run, rr_lumisections, rr_ls_duration, ls_oms, ls_brilcalc) 
    

sys.stdout.close()














