from collections import defaultdict
import runregistry
import json
import argparse
import sys


parser = argparse.ArgumentParser(description='Give list of runs from csv')
parser.add_argument("-o", "--output",
                    dest="outfile", type=str, default="test.txt", help="Output file name")
parser.add_argument("-i", "--input",
                    dest="csvfile", type=str, default="call16.csv", help="Input CSV file name")
parser.add_argument("-v", "--verbose",
            dest="verbose", action="store_true", default=False, help="Print out info")

options = parser.parse_args()

# - path to brilcalc output
path_to_brilcal_results = options.csvfile


### GET ALL DATA WE NEED ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import csv
brilcalc_file = open(path_to_brilcal_results, newline='') 
brilcalc_reader = csv.reader(brilcalc_file, delimiter=',')
brilcalc_lumis = defaultdict( dict )


## first filling information from csv file of brilcalc
for row in brilcalc_reader:
  if "#" in row[0] : continue
  run  = row[0].split(":")[0]
  lumi = row[1].split(":")[0]
  lumi_ = row[1].split(":")[1]
  delivered = row[5]
  recorded  = row[6]
  if lumi_==lumi: cmsActive = True
  else: cmsActive = False

  if "STABLE" in row[3]: stableBeam = True
  else: stableBeam = False
  
  brilcalc_lumis[int(run)][int(lumi)-1] = [ cmsActive, stableBeam, float(delivered), float(recorded) ]

  
## Now compare brilcalc and OMS
sys.stdout = open(options.outfile, "w")
print("Run number, OMS LS (delivered lumi: ub), brilcalc LS (recoreded lumi: ub)")  
for run, lumis in brilcalc_lumis.items():
  rr_run = runregistry.get_run(run)
  if type(rr_run) != type({}) : continue
  if "significant" not in rr_run : continue
  if not rr_run["significant"] : continue


  ## Number of LS from brilcalc
  ls_brilcalc = len(lumis)
  oms_lumisections = runregistry.get_oms_lumisections(run)
  ls_oms = len(oms_lumisections)
  nls_cmsActive = rr_run['oms_attributes']['last_lumisection_number']

  if ls_oms < ls_brilcalc:
    print(run, ls_oms, ls_brilcalc, "Warning: OMS API has fewer LSs than brilcalc")
  elif options.verbose:
    print(run, ls_oms, ls_brilcalc)
    
  # now loop over lumisections in brilcalc 
  Nbril_stableActive = 0
  Nbril_active = 0  
  for lumiNumber, lumiData in lumis.items():
    # Do not access OMS information that is not available
    if lumiNumber > ls_oms:
      continue    
    oms_cms_active  = oms_lumisections[lumiNumber]["cms_active"]
    oms_beam_stable = oms_lumisections[lumiNumber]["beam1_stable"] or oms_lumisections[lumiNumber]["beam2_stable"]
    bril_cms_active = lumiData[0]
    bril_beam_stable = lumiData[1]
    delivered_lumi  = lumiData[2]
    recorded_lumi   = lumiData[3]
    humanLumiIndex  = lumiNumber + 1
    if oms_beam_stable != bril_beam_stable:
      print( run, ":", humanLumiIndex, delivered_lumi, recorded_lumi, ", OMS stableFlag:", oms_beam_stable, ", brilcalc stableFlag:", bril_beam_stable)
    # Only alert if brilcalc has stable beam but cmsActive flag is not consistent  
    if bril_beam_stable == True and oms_cms_active != bril_cms_active:
      print( run, ":", humanLumiIndex, delivered_lumi, recorded_lumi, ", OMS cmsActive:", oms_cms_active, ", brilcalc cmsActive:", bril_cms_active)
    if bril_cms_active and bril_beam_stable: Nbril_stableActive += 1  

    if bril_cms_active: Nbril_active += 1 
    if options.verbose:
      print(run, humanLumiIndex, ", brilcalc: ", bril_cms_active, bril_beam_stable, ", OMS: ", oms_cms_active, oms_beam_stable)

  NOMS_stableActive = 0
  NOMS_active = nls_cmsActive
  # now loop over lumisections in OMS    
  for lumiNumber in range(0,nls_cmsActive):
    oms_beam_stable = oms_lumisections[lumiNumber]["beam1_stable"] or oms_lumisections[lumiNumber]["beam2_stable"]
    oms_cms_active  = oms_lumisections[lumiNumber]["cms_active"]
    if oms_beam_stable and oms_cms_active: NOMS_stableActive += 1  
    humanLumiIndex  = lumiNumber + 1
    if options.verbose:
      print("OMS", run, humanLumiIndex, oms_cms_active, oms_beam_stable)

  if NOMS_active != Nbril_active:
    print( run, NOMS_active, Nbril_active, "Alert!! OMS and brilcalc have different number of cms_active LSs (no requirement on beam)")

  if NOMS_stableActive != Nbril_stableActive:
    print( run, NOMS_stableActive, Nbril_stableActive, "Alert!! OMS and brilcalc have different number of stable+cms_active LSs")

  if options.verbose:
    print( run, "NActive LSs:", NOMS_active, Nbril_active)
    print( run, "NStableActive LSs", NOMS_stableActive, Nbril_stableActive)  
    
sys.stdout.close()














