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
import argparse
import sys
from operator import itemgetter


cscIncluded=False
dtIncluded=False
rpcIncluded=False

def runs_list(filter_in): 
  runs = runregistry.get_runs(filter = filter_in)
  return runs

## check if it is a Collision run 
def isCollisionRun( run_in ):

     print(run_in)

     oms_lumisections = runregistry.get_oms_lumisections(run_in)

     nLS=0
     
     for lumi in range(0, len(oms_lumisections)):
       
       if any(flag not in oms_lumisections[lumi] for flag in
              ['beam1_present','beam2_present',
               'beam1_stable','beam2_stable', 
               'cms_active']):
         continue
##      Run registry still checks the status when CMS is not taking data
#       if oms_lumisections[lumi]["cms_active"] != True:
#         continue
       beam1_present = oms_lumisections[lumi]["beam1_present"]
       beam2_present = oms_lumisections[lumi]["beam2_present"]
       beam1_stable = oms_lumisections[lumi]["beam1_stable"]
       beam2_stable = oms_lumisections[lumi]["beam2_stable"]

       # for runs > 355208, impose beam present requirement 
       # OMS beam present flags are not working for runs <= 355208
       # for all collision runs, impose beam stable requirements
       collisionRequirement = beam1_stable and beam2_stable \
                              and ( (run_in <= 355208) or 
                                    (run_in>355208 and beam1_present and beam2_present )) 
       if not collisionRequirement:
         continue


       nLS +=1   
       

     if nLS > 0:
       if options.verbose:
         print(oms_lumisections[lumi])
       return True  
     else:
       return False


def isCosmicsRun( run_in ):

     print(run_in)

     oms_lumisections = runregistry.get_oms_lumisections(run_in)

     nLS=0

     ## if we are checking cosmics class, need to make sure beam1 and beam2 
     ## are not present for the whole run
     for lumi in range(0, len(oms_lumisections)):
       if any(flag not in oms_lumisections[lumi] for flag in
              ['beam1_present','beam2_present',
               'tecm_ready','tecp_ready','tob_ready','tibtid_ready',
               'cms_active']):
         continue
##      Run registry still checks the status when CMS is not taking data
#       if oms_lumisections[lumi]["cms_active"] != True:
#         continue
       beam1_present = oms_lumisections[lumi]["beam1_present"]
       beam2_present = oms_lumisections[lumi]["beam2_present"]
       # check cosmics data, beam shall not be present for any LSs  
       cosmicsRequirement0 = (beam1_present == False) \
                             and (beam2_present == False)
       if not cosmicsRequirement0:
         return False
       # check strip DCS status   
       cosmicsRequirement1 = trackerIncluded  \
                             and (oms_lumisections[lumi]["tecm_ready"] 
                                  and oms_lumisections[lumi]["tecp_ready"] 
                                  and oms_lumisections[lumi]["tob_ready"]  
                                  and oms_lumisections[lumi]["tibtid_ready"])
   
       nMuon=0
       if cscIncluded and (oms_lumisections[lumi]["cscm_ready"] == True or
                           oms_lumisections[lumi]["cscp_ready"]  == True):
         nMuon +=1 
         
       if dtIncluded and (oms_lumisections[lumi]["dt0_ready"] == True or 
                           oms_lumisections[lumi]["dtm_ready"] == True or
                           oms_lumisections[lumi]["dtp_ready"] == True):
         nMuon +=1

       if rpcIncluded and oms_lumisections[lumi]["rpc_ready"] == True:
         nMuon +=1
       cosmicsRequirement2 = nMuon > 0       
         
       if not (cosmicsRequirement1 and cosmicsRequirement2): 
         continue

       nLS +=1   
       
     if nLS > 0:
       if options.verbose is True:
         print(oms_lumisections[lumi])
       return True
     else:
       return False


def isCommissioningRun( run_in ):

     print(run_in)

     oms_lumisections = runregistry.get_oms_lumisections(run_in)

     nLS=0

     
     for lumi in range(0, len(oms_lumisections)):

       
       if any(flag not in oms_lumisections[lumi] for flag in
              ['beam1_present','beam2_present',
               'beam1_stable','beam2_stable', 
               'cms_active']):
         continue

##      Run registry still checks the status when CMS is not taking data
#       if oms_lumisections[lumi]["cms_active"] != True:
#         continue
       beam1_present = oms_lumisections[lumi]["beam1_present"]
       beam2_present = oms_lumisections[lumi]["beam2_present"]
       beam1_stable = oms_lumisections[lumi]["beam1_stable"]
       beam2_stable = oms_lumisections[lumi]["beam2_stable"]


       commRequirement = ( (beam1_present == False) 
                           or (beam2_present == False)  
                           or (beam1_stable == False) 
                           or ( beam2_stable == False) )
       if not commRequirement:
         continue


       nLS +=1   
       

     if nLS > 0:
       if options.verbose is True:
         print(oms_lumisections[lumi])
       return True
     else:
       return False



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
            description='Give DCS-only JSONs for Online datasets')
    parser.add_argument("-min", "--min_run", dest="min_run", type=int, default=362167, help="minimum run for json")
    parser.add_argument("-max", "--max_run", dest="max_run",type=int, default=999999, help="maximum run for json")
    parser.add_argument("-v", "--verbose",
            dest="verbose", action="store_true", default=False, help="Display more info")
    parser.add_argument("-o", "--outpath",
        dest="outpath", type=str, default=os.getenv('PWD'), help="Output file path")


    options = parser.parse_args()
    print(sys.argv)      
      

    # generate filter 
    filter_arg = { 'run_number': { 'and':[ {'>=': options.min_run}, {'<=': options.max_run}] },
                   'hlt_physics_counter': { ">": 0 }
                  #include the runs that are not sign-off or not significant in case of problems
#                   'significant': { "=": True},
#                   'state': { "=": 'SIGNOFF'}
                 }

    out_runs = runs_list(filter_arg)
    if options.verbose is True:
      print(out_runs)

    anykey='/cdaq'  
    collisionhltkey='/cdaq/physics'  
    specialhltkey='/cdaq/special'
    cosmicshltkey='/cdaq/cosmic/commissioning2023/'

    filename = options.outpath + '/classoutput_' + str(options.min_run) + '_' + str(options.max_run) + '_runs.txt'
    print(filename)
    file = open(filename, "w")
    file.write("Run\t"+"RRClass\t"+"CorectClass\n")

    bugfilename = options.outpath + '/incorrect_' +  str(options.min_run) + '_' + str(options.max_run) + '_runs.txt'
    print(bugfilename)
    file2 = open(bugfilename, "w")
    file2.write("Run\t"+"RRClass\t"+"CorectClass\n")
 
    for run in out_runs:
      # first make hlt key requirement
      thisrun_hltkey = run["oms_attributes"]["hlt_key"]
      thisrun = run["run_number"]
      className = 'none'
      # priority 1: Collisions 
      if anykey not in thisrun_hltkey:
        continue

      if collisionhltkey in thisrun_hltkey:
        if isCollisionRun(thisrun):
          className = 'Collisions23'
        else:
          if isCommissioningRun(thisrun):
            className = "Commissioning23"
      # priority 2: CollisionsSpecial
      elif specialhltkey in thisrun_hltkey:
        if isCollisionRun(thisrun):
          className = 'Collisions23Special'
        else:
          if isCommissioningRun(thisrun):
            className = "Commissioning23"
      # priority 3: Cosmics
      elif cosmicshltkey in thisrun_hltkey:
          ## tracker must be included
          ## at least one muon system must be included
        trackerIncluded = False if 'tracker_included' not in run["oms_attributes"] else run["oms_attributes"]["tracker_included"]  
        cscIncluded = False if 'csc_included' not in run["oms_attributes"] else run["oms_attributes"]["csc_included"]  
        dtIncluded = False if 'dt_included' not in run["oms_attributes"] else run["oms_attributes"]["dt_included"]  
        rpcIncluded = False if 'rpc_included' not in run["oms_attributes"] else run["oms_attributes"]["rpc_included"]  

        if ( trackerIncluded  
             and (cscIncluded or dtIncluded or rpcIncluded )  
             and isCosmicsRun(thisrun)):
          className = 'Cosmics23'
        else:
          if isCommissioningRun(thisrun):
            className = "Commissioning23"
      else:
          if isCommissioningRun(thisrun):
            className = "Commissioning23"

      file.write(str(thisrun)+'\t'+run["class"]+"\t"+className+"\n")
      if className != run["class"]: 
        file2.write(str(thisrun)+'\t'+run["class"]+"\t"+className+"\n")
        
    file.close()
    file2.close()

    print("Job finished")
