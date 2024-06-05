from contextlib import redirect_stdout
from collections import defaultdict
import runregistry
import matplotlib
import os
import argparse
import sys


class MyPlot:
  def __init__(self, title, xtitle, ytitle, labelsize, inputdict):
    self.title  = title
    self.xtitle = xtitle
    self.ytitle = ytitle
    self.labelsize = labelsize
    self.inputdict = inputdict


def sort_dict(inputdict, mode=0):
  if mode==1: # for pie chart, ignore the contribution less than 1%
    for iele in list(inputdict.keys()):
      if(inputdict[iele]<1e-2):
        del inputdict[iele]
  elif mode==2: # for bar chart, ignore the contribution less than 1%, numbers are displayed in percentange
    for iele in list(inputdict.keys()):
      if(inputdict[iele]<1.0):
        del inputdict[iele]
  elif mode==3: # for bar chart, ignore the contribution less than 1/nb 
    for iele in list(inputdict.keys()):
      if(inputdict[iele]<1e-3):
        del inputdict[iele]

  sorted_dictionary = dict(sorted(inputdict.items(), key=lambda item: item[1]))
  print(sorted_dictionary)
  return sorted_dictionary

def bar_plot(inputdict, ax=None,**plt_kwargs):
    if ax is None:
        ax = plt.gca()
    plt.barh( list(inputdict.keys()), list(inputdict.values())) ## example plot here
    return(ax)


def pie_plot(inputdict, ax=None, **plt_kwargs):
  if ax is None:
    ax = plt.gca()
    plt.pie( list(inputdict.values()), labels=list(inputdict.keys()),  autopct='%1.1f%%', **plt_kwargs) ## example plot here
#    plt.pie( list(inputdict.values()), labels=None,  autopct='%1.1f%%', **plt_kwargs) ## example plot here
    return(ax)


### :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
      
# AS WE HAVE ALL THE DATA NOW WE CAN CALCULATE LOSES
# FOR EXAMPLE LOSES PER SUBSYSTEMS
subsystems = ["tracker-pixel", "tracker-strip", "tracker-track", "ecal-ecal", "ecal-es", "hcal-hcal", "csc-csc", "dt-dt", "l1t-l1tmu", "l1t-l1tcalo", "hlt-hlt", "egamma-egamma", "muon-muon", "jetmet-jetmet"]
subsystems_loss = defaultdict( float )

dcs_sub =   ["bpix_ready", "fpix_ready", "tibtid_ready", "tecm_ready", "tecp_ready", "tob_ready", "hbhea_ready", "hbheb_ready", "hbhec_ready", "hf_ready", "ho_ready"]
dcs_loss = defaultdict( float )

detector_sub = {}
detector_sub["PixelPhase1"] = ["tracker-pixel", "bpix_ready", "fpix_ready"]
detector_sub["SiStrip"] = ["tracker-strip", "tibtid_ready", "tecm_ready", "tecp_ready","tob_ready"]
detector_sub["ECAL"] = ["ecal-ecal"]
detector_sub["ES"] = ["ecal-es"]
detector_sub["HCAL"] = ["hcal-hcal", "hbhea_ready","hbheb_ready","hbhec_ready","hf_ready","ho_ready"]
detector_sub["CSC"] = ["csc-csc"]
detector_sub["DT"] = ["dt-dt"]
detector_sub["L1T"] = ["l1t-l1tcalo","l1t-l1tmu"]
detector_sub["HLT"] = ["hlt-hlt"]
detector_sub["Tracking"] = ["tracker-track"]
detector_sub["MuonPOG"] = ["muon-muon"]
detector_sub["JetMET"] = ["jetmet-jetmet"]
detector_sub["EGamma"] = ["egamma-egamma"]


detector_loss = defaultdict(dict)
# For dumping run,LS vs lumi loss for each system
subsystem_run_loss = defaultdict()
subsystem_run_LS = defaultdict()

## Initialize the values of detector_loss
cms_sub = list(detector_sub.keys())
for isub in cms_sub:
    list2 = list(detector_sub[isub])
    for isub2 in list2:
        detector_loss[isub][isub2] = 0.0



cms_frac_exclusive_loss = defaultdict( float )
cms_detailed_frac_exclusive_loss = defaultdict( float )
cms_numerator_exclusive_loss = defaultdict( float )
cms_exclusive_loss = defaultdict( float )
cms_inclusive_loss = defaultdict( float )
cms_status = defaultdict( bool )

total_recorded = 0.0
total_loss = 0.0

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Give list of file names')
  parser.add_argument("-c", "--csv",
                    dest="csvfile", type=str, default="Era/output_eraB.csv", help="Path to csv file from the previous step")
  parser.add_argument("-p", "--period",
                    dest="period", type=str, default="eraB", help="Period name, will be used as postfix")
  parser.add_argument("-d", "--dir",
                    dest="dirname", type=str, default="textFiles", help="output directory")

  options = parser.parse_args()
  print(sys.argv)

  postfix = options.period
  results_csv = options.csvfile
  import csv

  lumi_file = open(results_csv, newline='')
  lumi_file_reader = csv.reader(lumi_file, delimiter='$')


  for row in lumi_file_reader:
    run  = int(row[0])
    LS   = int(row[1])
    #  print("Run ",run, ":", LS)
    delivered = float(row[2])/1000000.
    recorded  = float(row[3])/1000000.
    total_recorded += recorded
    bits = eval( row[4] )
    if not bits : continue # all good in JSON
  
    for subsystem in subsystems:
      if bits[subsystem] == "GOOD" : continue
      subsystems_loss[ subsystem ] += recorded

    for dcs_subsystem in dcs_sub:
      if bits[dcs_subsystem] == True : continue
      #    print("bit ",bits[dcs_subsystem])
      dcs_loss[ dcs_subsystem ] += recorded


    # set each subsystem to true by default
    for icms in cms_sub: 
      cms_status[ icms ] = True

    for isub in cms_sub:
      list2 = list(detector_sub[isub])
      for isub2 in list2:
        if bits[isub2] == True or bits[isub2]== "GOOD" : continue
        cms_status [ isub ] = False 
        detector_loss[isub][isub2] += recorded

  # Now check if there are mixed system
    count = 0 
    detector_blame = "" 
    for icms in cms_sub:
      if cms_status [ icms ] == False: 
        cms_inclusive_loss [ icms ] += recorded 
        detector_blame = detector_blame + icms + " "
        count += 1
      
    if count > 1: 
      cms_numerator_exclusive_loss [ "Mixed" ] += recorded
    elif count == 1: 
      cms_numerator_exclusive_loss [ detector_blame ] += recorded

    if count >= 1:
      cms_exclusive_loss [ detector_blame ] += recorded
      total_loss += recorded
      if detector_blame not in subsystem_run_loss:
        subsystem_run_loss[detector_blame] = defaultdict(float)
      if detector_blame not in subsystem_run_LS:
        subsystem_run_LS[detector_blame] = defaultdict(list)
      subsystem_run_loss[detector_blame][run] += recorded
      subsystem_run_LS[detector_blame][run].append(LS)

# After accumulation of all LSs
# Check the fraction of luminosity loss due to each subsystem
  if total_loss > 0.0:
    for icms in list(cms_numerator_exclusive_loss.keys()):
      cms_frac_exclusive_loss [ icms ] = cms_numerator_exclusive_loss [ icms ]/total_loss
    for icms in list(cms_exclusive_loss.keys()):
      cms_detailed_frac_exclusive_loss [ icms ] = 100*cms_exclusive_loss [ icms ]/total_loss



  print( "Total recorded luminosity for these runs is: ", total_recorded, "/pb")
  print( "Total recorded luminosity loss for these runs is: ", total_loss, "/pb")

# sort all dictionaries
  sorted_subsystems_loss = sort_dict(subsystems_loss)
  sorted_dcs_loss = sort_dict(dcs_loss)

  sorted_cms_inclusive_loss = sort_dict(cms_inclusive_loss)
  sorted_cms_exclusive_loss = sort_dict(cms_exclusive_loss, 3)
  sorted_cms_numerator_exclusive_loss = sort_dict(cms_numerator_exclusive_loss)
  sorted_cms_frac_exclusive_loss = sort_dict(cms_frac_exclusive_loss, 1)
  sorted_cms_detailed_frac_exclusive_loss = sort_dict(cms_detailed_frac_exclusive_loss, 2)

  print(subsystem_run_loss)
#  print(subsystem_run_LS)
  #dump loss vs run in text files
  dirName = options.dirname
#  os.mkdir(dirName)
#  for isub in list(subsystem_runLS_loss.keys()):
  for isub in list(sorted_cms_detailed_frac_exclusive_loss.keys()):
    filename = isub.replace(' ', '_')
    filename = dirName + '/' + filename + 'loss_'+ postfix + '.txt'
    print(filename)
    with open(filename,'w') as file:
      with redirect_stdout(file):
        for irun in list(subsystem_run_loss[isub]):
          print(irun, ":", subsystem_run_LS[isub][irun])
          print(irun, ":", subsystem_run_loss[isub][irun], '/pb \n')
    file.close()

