from collections import defaultdict
import runregistry
import argparse
import sys

### SET FOLLOWING :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# - path to grid certificate
# - dataset
dataset = "/PromptReco/Collisions2022/DQM"
### :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

parser = argparse.ArgumentParser(description='output file name that provides the check result')
parser.add_argument("-i", "--input",
                    dest="infile", type=str, default="runsToCheck.txt", help="Input file name")
parser.add_argument("-o", "--output",
                    dest="outfile", type=str, default="test.txt", help="Output file name")

options = parser.parse_args()


sys.stdout = open(options.outfile, "w")

print("Run number, OMS LS, online RR LS, offline RR LS")

inputrun_list= []
# Using readlines()                                                                                                  
file1 = open(options.infile, 'r')
Lines = file1.readlines()
# Strips the newline character                                                                                       
for line in Lines:
  thisrun = int(line.strip())
  rr_run = runregistry.get_run(thisrun)
  if type(rr_run) != type({}) : continue
  if "significant" not in rr_run : continue
  if not rr_run["significant"] : continue
   ## Need to have the dataset /PromptReco/Collisions2022/DQM
  if dataset not in runregistry.get_dataset_names_of_run(thisrun): continue
  
  ## Number of LS from OMS (Most of the time, it is the same as ls_onlineRR
  ls_oms = len(runregistry.get_oms_lumisections(thisrun))

  ## Number of LS from online RR (also LS Duration)
  ls_onlineRR = len(runregistry.get_lumisections(thisrun))

  ## Number of LS in offline RR (listed in DQM column)
  ls_offlineRR= len(runregistry.get_lumisections(thisrun, dataset))

  if ls_oms != ls_offlineRR: 
    print( thisrun, ls_oms, ls_onlineRR, ls_offlineRR, "! -->") 
  elif ls_oms != ls_onlineRR: 
    print( thisrun, ls_oms, ls_onlineRR, ls_offlineRR, "#") 
  else: 
    print( thisrun, ls_oms, ls_onlineRR, ls_offlineRR) 
    

sys.stdout.close()














