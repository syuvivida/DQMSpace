
from collections import defaultdict
import runregistry
import matplotlib
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

## this is used for the inclusive loss of each subsystem
detector_inclusive_loss = defaultdict(dict)

## this is used for exclusive loss of the subcomponent of each subsystem
detector_exclusive_loss = defaultdict(dict)


## Initialize the values of detector_inclusive_loss
cms_sub = list(detector_sub.keys())
for isub in cms_sub:
  list2 = list(detector_sub[isub])
  for isub2 in list2:
    detector_inclusive_loss[isub][isub2] = 0.0
    detector_exclusive_loss[isub][isub2] = 0.0
  detector_exclusive_loss[isub]['Mixed'] = 0.0



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
  parser.add_argument("-d", "--outdir",
                    dest="outdir", type=str, default="figures_eraB", help="directory of output figures")

  options = parser.parse_args()
  print(sys.argv)

  outputdir = options.outdir
  postfix = options.period
  results_csv = options.csvfile
  import csv

  lumi_file = open(results_csv, newline='') 
  lumi_file_reader = csv.reader(lumi_file, delimiter='$')

  for row in lumi_file_reader:
    run  = int(row[0])
    #  print("Run ",run)
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
      count_list2 = 0
      subcomponent_blame= ""
      for isub2 in list2:
        if bits[isub2] == True or bits[isub2]== "GOOD" : continue
        count_list2 += 1
        subcomponent_blame= isub2 
        cms_status [ isub ] = False 
        detector_inclusive_loss[isub][isub2] += recorded
      # for each subsystem, check the exclusive loss
      if count_list2 > 1:
        detector_exclusive_loss[isub]['Mixed'] += recorded
      elif count_list2 ==1:
        detector_exclusive_loss[isub][subcomponent_blame] += recorded

  # Now check if there are mixed system
    count = 0 
    detector_blame = "" 
    for icms in cms_sub:
      if cms_status [ icms ] == False: 
        cms_inclusive_loss [ icms ] += recorded 
        detector_blame = detector_blame + icms + " "
        count += 1
    ## Since L1T and HLT mark a LS bad due to upstream detector issues
    ## put the exclusive loss of L1T and HLT into Mixed
    if count > 1 or "L1T" in detector_blame or "HLT" in detector_blame: 
      cms_numerator_exclusive_loss [ "Mixed" ] += recorded
    elif count == 1: 
     cms_numerator_exclusive_loss [ detector_blame ] += recorded

    if count >= 1:
      if count == 1 and ("L1T" in detector_blame or "HLT" in detector_blame):
        detector_blame = detector_blame+ "+ detectors"
      elif count == 2 and "L1T" in detector_blame and "HLT" in detector_blame:
        detector_blame = detector_blame+ "+ detectors"        
      cms_exclusive_loss [ detector_blame ] += recorded
      total_loss += recorded

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

  import matplotlib.pyplot as plt

# NOW MAKE PLOT FROM DICTIONARY VALUES
  xtitle_default = 'Luminosity Loss (/pb)'
  ytitle_default = 'Subsystem'
  labelsize_default = 10
  small_labelsize = labelsize_default 
  titlesize_default = 14
  
  # DQM flag
  plot_dict = defaultdict(MyPlot)
  plot_dict['subsystemDQMFlag_loss'] = MyPlot('DQM Flags vs. Inclusive Loss', xtitle_default, 'DQM Flag', labelsize_default, sorted_subsystems_loss)
  
  # DCS bits
  plot_dict['DCS_loss'] = MyPlot('DCS Bits vs. Inclusive Loss', xtitle_default, 'DCS Bit', labelsize_default, sorted_dcs_loss)

  # CMS subsystem inclusive loss
  plot_dict['cms_inclusive_loss'] = MyPlot('Inclusive Loss from Each CMS Subsystem', xtitle_default, ytitle_default, labelsize_default, sorted_cms_inclusive_loss)
  
  # CMS subsystem exclusive loss
  if len(sorted_cms_exclusive_loss)>12:
    small_labelsize = 6
  plot_dict['cms_exclusive_loss'] = MyPlot('Exclusive Loss from Each Category', xtitle_default, '', small_labelsize, sorted_cms_exclusive_loss)

  #Now make a detailed bar chart: fraction of exclusive loss due to each subdetector
  plot_dict['cms_detailed_fraction_exclusive_loss'] = MyPlot('Fraction of Exclusive Loss from Each Category', 'Percentage %', '', labelsize_default, sorted_cms_detailed_frac_exclusive_loss)

  #loop over plot_dict
  icount=0
  for isub in list(plot_dict.keys()):
    dict_this = defaultdict(float)
    dict_this = plot_dict[isub].inputdict
#    print(dict_this)
    icount += 1
#    axes = plt.figure(icount, [5, 20]) # this line moved and figure size changed to suit data
    axes = plt.figure(icount) # this line moved and figure size changed to suit data
    plt.tick_params(axis='both', which='major', labelsize=plot_dict[isub].labelsize) # makes axis labels smaller
    bar_plot(dict_this,ax=axes)
    plt.title(plot_dict[isub].title, fontsize=titlesize_default)
    plt.xlabel(plot_dict[isub].xtitle, fontsize=titlesize_default)
    plt.ylabel(plot_dict[isub].ytitle, fontsize=titlesize_default)
    plt.savefig( outputdir+"/"+isub+"_"+postfix+".png", bbox_inches='tight')




#Now make inclusive loss due to each sub system separately
  for isub in cms_sub:
    list2 = list(detector_sub[isub])
    dict_this = defaultdict(float)
    icount +=1
    for isub2 in list2:
        dict_this[isub2] = detector_inclusive_loss[isub][isub2]
    sorted_thissub = sort_dict(dict_this)
    axes = plt.figure(icount)
    bar_plot(sorted_thissub,ax=axes)
    plt.title('Inclusive Loss of ' + isub + ' System', fontsize=titlesize_default)
    plt.xlabel(xtitle_default, fontsize=titlesize_default)
    plt.ylabel('Component', fontsize=titlesize_default)
    plt.savefig( outputdir+"/"+isub+"_inclusiveloss_"+postfix+".png", bbox_inches='tight')


#Now make exclusive loss due to each sub system separately
  for isub in list(detector_exclusive_loss.keys()):
    list2 = list(detector_exclusive_loss[isub])
    dict_this = defaultdict(float)
    icount +=1
    ## No need to make plots for the system with only Mixed and one flag
    ## since inclusive and exclusive loss are the same
    if len(list2) <= 2: continue 
    for isub2 in list2:
        dict_this[isub2] = detector_exclusive_loss[isub][isub2]
    sorted_thissub = sort_dict(dict_this)
    axes = plt.figure(icount)
    bar_plot(sorted_thissub,ax=axes)
    plt.title('Exclusive Loss of ' + isub + ' System', fontsize=titlesize_default)
    plt.xlabel(xtitle_default, fontsize=titlesize_default)
    plt.ylabel('Component', fontsize=titlesize_default)
    plt.savefig( outputdir+"/"+isub+"_exclusiveloss_"+postfix+".png", bbox_inches='tight')




#Now make a pie chart: fraction of exclusive loss due to each subdetector
  colors=['brown', 'purple', 'plum', 'red', 'pink', 'green', 'orange', 'yellow', 'blue', 'pink', 'orchid', 'goldenrod', 'gray', 'olive' ]
  colors_dict = defaultdict(str)
  colors_dict['Mixed'] = colors[0]
  icolor=1
  for icms in cms_sub:
    colors_dict[icms+' '] = colors[icolor]
    icolor += 1
  print(colors_dict)
  color_keys = list(sorted_cms_frac_exclusive_loss.keys())
  print(color_keys)
#  axes = plt.figure(icount+1)  
  myexplode = []
  ele = 0
  for isub in color_keys:
    myexplode.append(0.01+ele*0.01)
    ele +=1 
  plt.figure(icount+1)
  plt.pie( list(sorted_cms_frac_exclusive_loss.values()), labels=color_keys,  autopct='%1.1f%%', explode=myexplode,normalize=True,colors=[colors_dict[key] for key in color_keys]) ## example plot here
#  pie_plot(sorted_cms_frac_exclusive_loss,ax=axes,explode=myexplode,normalize=True,colors=[colors_dict[key] for key in color_keys])
#  plt.legend(loc='lower right',labels=list(sorted_cms_frac_exclusive_loss.keys()))
  plt.title('Fraction of Exclusive Loss from Each Category', fontsize=titlesize_default)
  plt.savefig( outputdir+"/cms_piechart_exclusive_loss_"+postfix+".png", bbox_inches='tight')



#plt.show()
#plt.close('all')
