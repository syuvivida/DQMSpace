
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
parser.add_argument("-r", "--run",
                    dest="runnumber", type=int, default=359187, help="run number")
options = parser.parse_args()


oms_lumisections = runregistry.get_oms_lumisections(options.runnumber,"/PromptReco/Commissioning2022/DQM")
for lumi in range(0, len(oms_lumisections)):
  print(lumi,":",oms_lumisections[lumi]['fpix_ready'])

### GET ALL DATA WE NEED ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::














