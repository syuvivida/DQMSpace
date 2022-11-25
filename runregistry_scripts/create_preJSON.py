#!/usr/bin/env python

import runregistry
import json
import argparse
import sys
from operator import itemgetter

dataset = "/PromptReco/Collisions2022/DQM"

def runs_list(filter_in): 
  runs = runregistry.get_runs(filter = filter_in)
  return runs

#print(type(runs))

def get_run_ls( run_in ):

     oms_lumisections = runregistry.get_oms_lumisections(run_in,dataset)
     lumi_store = []
     flags_list = ['beam1_present','beam2_present','beam1_stable','beam2_stable']
     if run_in not in main_obj:
          main_obj[run_in] = []
     
     print(run_in)
     #print(oms_lumisections[lumi])
     check_lumi_range = False
     for lumi in range(0, len(oms_lumisections)):

       if any(flag not in oms_lumisections[lumi] for flag in flags_list):
         continue;
       quality = True

       # for call 7, OMS beam1_present and beam2_present flags are not correct
       if (run_in >= 355100 and run_in <= 355208) and (oms_lumisections[lumi][flags_list[2]] == False or oms_lumisections[lumi][flags_list[3]] == False):
         quality = False
       # for other calls, beam1_present and beam2_present are required  
       elif run_in > 355208:
         for flag in flags_list:
           if oms_lumisections[lumi][flag] == False:
             quality = False
             break
       if quality is False:
         check_lumi_range=False           
         continue
             
       if check_lumi_range:
         start_of_current_range = main_obj[run_in][-1][0] 
         main_obj[run_in][-1] = [start_of_current_range,lumi+1]   

       if check_lumi_range is False:
         main_obj[run_in].append([lumi+1,lumi+1]) 
         check_lumi_range=True


#     for el in main_obj:                                                                                        
#       main_obj[el] = sorted(main_obj[el], key=itemgetter(0))

     return main_obj[run_in]


def write_json(main_obj_read, out):
    main_temp = {}
    for i in main_obj_read:
        if len(main_obj_read[i])>0:
            main_temp[i] = main_obj_read[i]
    with open(out, "w") as f:
          f.write(json.dumps(main_temp, indent=1, sort_keys=True))



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
            description='Give list of Collisions runs for Online datasets')
    parser.add_argument("-m", "--mode",
        dest="mode", type=int, default= 1, help="Mode 0: use run range, Mode 1: use run list")
    parser.add_argument("-i", "--infile",
        dest="infile", type=str, default="eraB_runs.txt", help="Input file that contains the run numbers")
    # a run range is use if mode is set to 0
    parser.add_argument("-min", "--min_run", dest="min_run", type=int, default=355100, help="minimum run for json")
    parser.add_argument("-max", "--max_run", dest="max_run",type=int, default=999999, help="maximum run for json")
    parser.add_argument("-o", "--outfile",
        dest="outfile", type=str, default="eraB_allLS.json", help="Output file name")
    parser.add_argument("-v", "--verbose",
            dest="verbose", action="store_true", default=False, help="Display more info")

    options = parser.parse_args()

    # use run range if using default mode
    if options.mode==0: 
    # generate filter 
      print("Using mode 0 and the runs from ", options.min_run, " to ", options.max_run)
      filter_arg = { 'run_number': { 'and':[ {'>=': options.min_run}, {'<=': options.max_run}] }, 
                     'class': { '=': 'Collisions22'},
                   'oms_attributes.b_field': {">=": 3.7}
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
      filter_arg = { 'run_number': {'or': inputrun_list},
                     'class': { '=': 'Collisions22'},
                     'oms_attributes.b_field': {">=": 3.7}
                   }




    out_runs = runs_list(filter_arg)
    print("There are ",len(out_runs), " runs")
#    print(out_runs)

    main_obj = {}                                                                                                                                            
    for run in out_runs:
         main_obj[run["run_number"]]= get_run_ls(run["run_number"])

    for el in main_obj:
         main_obj[el] = sorted(main_obj[el], key=itemgetter(0))


    write_json(main_obj,options.outfile)

