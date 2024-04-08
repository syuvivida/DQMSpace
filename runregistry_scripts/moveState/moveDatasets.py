#!/usr/bin/env python

import os
import json
import argparse
import sys
from operator import itemgetter


githubstring='GITHUB_PATH'
github_path = os.getenv(githubstring)
if githubstring in os.environ:
  print("Setting up the path of runregistry")
  sys.path.append(os.path.dirname(os.path.realpath(github_path)))


import runregistry
## Note by default it is set to production
#runregistry.setup( "development" ) 
#runregistry.setup( "production" ) 

def runs_list(filter_in): 
  runs = runregistry.get_runs(filter = filter_in)
  return runs


    
parser = argparse.ArgumentParser(description='Give list of Collisions runs for Online datasets')
parser.add_argument("-m", "--mode",
                    dest="mode", type=int, default= 1, help="Mode 0: use run range, Mode 1: use run list")
parser.add_argument("-i", "--infile",
                    dest="infile", type=str, default="eraB_runs.txt", help="Input file that contains the run numbers")
# a run range is use if mode is set to 0
parser.add_argument("-min", "--min_run", dest="min_run", type=int, default=355100, help="minimum run for json")
parser.add_argument("-max", "--max_run", dest="max_run",type=int, default=999999, help="maximum run for json")
parser.add_argument("-f", "--from", dest="fromstate", type=str, default="OPEN", help="from the state")
parser.add_argument("-t", "--to", dest="tostate",type=str, default="SIGNOFF", help="to the state")
## to avoid doing changes for collision runs, by default set Commissioning runs
# this is only imposed when specifying a run ranges
parser.add_argument("-g", "--group",
                    dest="dataset_class", type=str, default="Cosmics18", help="Run class type") 
parser.add_argument("-n", "--name",
                    dest="dataset_name", type=str, default="/Calibration/HICosmics18A/DQM", help="Dataset name") 
parser.add_argument("-w", "--workspace",
                    dest="workspace", type=str, default="global", help="workspace")
parser.add_argument("-v", "--verbose",
                    dest="verbose", action="store_true", default=False, help="Display more info")

options = parser.parse_args()
print(sys.argv)
# use run range if using default mode
if options.mode==0: 
  # generate filter 
  print("Using mode 0 and the runs from ", options.min_run, " to ", options.max_run)
  filter_arg = { 'run_number': { 'and':[ {'>=': options.min_run}, {'<=': options.max_run}] }, 
                 'class': { '=': options.dataset_class}
  }


  # first read input files to get the list of run numbers for a certain period or a certain call
elif options.mode==1:
  inputrun_list= [] 
  # Using readlines()
  file1 = open(options.infile, 'r')
  Lines = file1.readlines()
  # Strips the newline character
  for line in Lines:
    thisrun = int(line.strip())
    thisdict = {'=':thisrun}
    dict_copy = thisdict.copy()
    inputrun_list.append(dict_copy)

    print("Using mode 1 and the runs in the following list")
    print(inputrun_list)
  # generate filter 
  filter_arg = { 'run_number': {'or': inputrun_list}
  }




out_runs = runs_list(filter_arg)
print("There are ",len(out_runs), " runs")
if options.verbose is True:
  print(out_runs)

for run in out_runs:
  answer = runregistry.move_datasets( options.fromstate, options.tostate, options.dataset_name, run=run["run_number"], workspace=options.workspace )
#  answer = runregistry.move_datasets( 'waiting dqm gui', 'OPEN', options.dataset_name, run=run["run_number"], options.workspace )
#  print( answer, answer.text )
  print(run["run_number"])
                               

## now setting up
