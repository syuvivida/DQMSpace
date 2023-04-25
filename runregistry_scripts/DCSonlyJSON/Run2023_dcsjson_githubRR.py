#!/usr/bin/env python
import sys, os
#sys.path.append(os.path.dirname(os.path.realpath("../runregistry")))          
# "./runregistry/runregistry_api_client/runregistry" 
githubstring='GITHUB_PATH'
github_path = os.getenv(githubstring)
if githubstring in os.environ: 
  print("Setting up the path of runregistry")
  sys.path.append(os.path.dirname(os.path.realpath(github_path)))

import runregistry
import json
import argparse
import sys
from operator import itemgetter

isCollisionClass=False

def runs_list(filter_in): 
  runs = runregistry.get_runs(filter = filter_in)
  return runs


def get_run_ls( run_in ):

     oms_lumisections = runregistry.get_oms_lumisections(run_in)
     lumi_store = []
     if run_in not in main_obj:
          main_obj[run_in] = []
     
     check_lumi_range = False
     print(run_in)

     for lumi in range(0, len(oms_lumisections)):

       if options.verbose is True:
         print(oms_lumisections[lumi])

       # first check if flags exist in OMS
       if any(flag not in oms_lumisections[lumi] for flag in 
              ['fpix_ready','bpix_ready','tecm_ready','tecp_ready','tob_ready','tibtid_ready','cms_active']):
         check_lumi_range=False
         continue

       # check if CMS is taking data  
       if oms_lumisections[lumi]["cms_active"] != True:
         check_lumi_range=False
         continue

       # check if forward pixel DCS status is good
       if oms_lumisections[lumi]['fpix_ready'] != True: 
         check_lumi_range=False
         continue 

       # check if barrel pixel DCS status is good
       if oms_lumisections[lumi]["bpix_ready"] != True:
         check_lumi_range=False
         continue

       # check if strip outer endcaps minus side  DCS status is good
       if oms_lumisections[lumi]["tecm_ready"] != True:
         check_lumi_range=False
         continue

       # check if strip outer endcaps plus side  DCS status is good
       if oms_lumisections[lumi]["tecp_ready"] != True:
         check_lumi_range=False
         continue

       # check if strip outer barrel side  DCS status is good
       if oms_lumisections[lumi]["tob_ready"] != True:
         check_lumi_range=False
         continue

       # check if strip inner barrel and inner disk  DCS status is good
       if oms_lumisections[lumi]["tibtid_ready"] != True:
         check_lumi_range=False
         continue

       # for runs > 355208, impose beam present requirement 
       # OMS beam present flags are not working for runs <= 355208
       if isCollisionClass and not ( (run_in <= 355208) or 
                                     (run_in>355208 
                                      and oms_lumisections[lumi]["beam1_present"] == True 
                                      and oms_lumisections[lumi]["beam2_present"] == True)):
         check_lumi_range=False
         continue

       # for all collision runs, impose beam stable requirements
       if isCollisionClass and not (oms_lumisections[lumi]["beam1_stable"] == True and oms_lumisections[lumi]["beam2_stable"] == True):
         check_lumi_range=False
         continue

       if check_lumi_range:
         start_of_current_range = main_obj[run_in][-1][0] 
         main_obj[run_in][-1] = [start_of_current_range,lumi+1]   

       if check_lumi_range is False:
         main_obj[run_in].append([lumi+1,lumi+1]) 
         check_lumi_range=True

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
            description='Give DCS-only JSONs for Online datasets')
    parser.add_argument("-min", "--min_run", dest="min_run", type=int, default=362167, help="minimum run for json")
    parser.add_argument("-max", "--max_run", dest="max_run",type=int, default=999999, help="maximum run for json")
    parser.add_argument("-minE", "--min_energy", dest="minEnergy", type=int, default=6500, help="minimum beam energy")
    parser.add_argument("-maxE", "--max_energy", dest="maxEnergy", type=int, default=7000, help="maximum beam energy")
    parser.add_argument("-zb", "--zerobfield",
            dest="zeroBField", action="store_true", default=False, help="Zero B field (CRUZET)")
    parser.add_argument("-g", "--group",
        dest="dataset_group", type=str, default="Collisions22", help="Run class type")
    parser.add_argument("-v", "--verbose",
            dest="verbose", action="store_true", default=False, help="Display more info")

    parser.add_argument("-o", "--outpath",
        dest="outpath", type=str, default=os.getenv('PWD'), help="Output file path")

    options = parser.parse_args()
    print(sys.argv)

    # Check if the class is a Collision class
    if 'Collisions' in options.dataset_group:
      isCollisionClass=True
      print("this is a Collision class and beam requirements will be imposed\n")
      

    # generate filter 
    filter_arg = { 'run_number': { 'and':[ {'>=': options.min_run}, {'<=': options.max_run}] }, 
                   'class': { 'like': options.dataset_group},
                   'significant': { "=": True},
                   'state': { "=": 'SIGNOFF'},
                   'oms_attributes.tracker_included': {"=": True},
                   'oms_attributes.pixel_included': {"=": True}
                   }

    out_runs = runs_list(filter_arg)

    if options.verbose is True:
      print(out_runs)

    main_obj = {}                                                                                                                                            
    for run in out_runs:
         # make beam energy requirement if this is a collision class
         # somehow the filter doesn't work, and one needs to apply requirements here
         if isCollisionClass and run["oms_attributes"]["energy"] < options.minEnergy:
           continue
         if isCollisionClass and run["oms_attributes"]["energy"] > options.maxEnergy:
           continue
         if options.zeroBField is False and run["oms_attributes"]["b_field"] < 3.7:
           continue
         elif options.zeroBField is True and run["oms_attributes"]["b_field"] > 1.0:
           continue
  
         main_obj[run["run_number"]]= get_run_ls(run["run_number"])

    for el in main_obj:
         main_obj[el] = sorted(main_obj[el], key=itemgetter(0))

    postfix='_DCSOnly_TkPx.json'     

    infotag='_'
    if 'Cosmics' in options.dataset_group: 
      if options.zeroBField is False:
        infotag='_CRAFT_'
      else:  
        infotag='_CRUZET_'

    if isCollisionClass and options.minEnergy >= 6500 and options.maxEnergy <= 7000:
      infotag='_13p6TeV_'
    elif isCollisionClass and options.minEnergy >= 400 and options.maxEnergy <= 500:
      infotag='_900GeV_'

    output_file = options.outpath+ '/'+options.dataset_group+ infotag +str(options.min_run)+'_'+str(options.max_run)+ postfix
    write_json(main_obj,output_file)

