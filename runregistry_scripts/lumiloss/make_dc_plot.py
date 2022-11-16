
from collections import defaultdict
import runregistry
import matplotlib

def sort_dict(inputdict, mode=0):
  if mode==1: # for pie chart, ignore the contribution less than 1%
    for iele in list(inputdict.keys()):
      if(inputdict[iele]<1e-2):
        del inputdict[iele]
  elif mode==2: # for bar chart, ignore the contribution less than 1%, numbers are displayed in percentange
    for iele in list(inputdict.keys()):
      if(inputdict[iele]<1.0):
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
    return(ax)

### SET FOLLOWING :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# - path to our results output
results_csv = "output.csv"
### :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

### GET ALL DATA WE NEED ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import csv
lumi_file = open(results_csv, newline='') 
lumi_file_reader = csv.reader(lumi_file, delimiter='$')

### :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
      
# AS WE HAVE ALL THE DATA NOW WE CAN CALCULATE LOSES
# FOR EXAMPLE LOSES PER SUBSYSTEMS
subsystems = ["tracker-pixel", "tracker-strip", "tracker-track", "ecal-ecal", "ecal-es", "hcal-hcal", "l1t-l1tmu", "l1t-l1tcalo", "hlt-hlt", "egamma-egamma", "muon-muon", "jetmet-jetmet"]
subsystems_loss = defaultdict( float )

dcs_sub =   ["bpix_ready", "fpix_ready", "tibtid_ready", "tecm_ready", "tecp_ready","tob_ready","ebm_ready","ebp_ready","eem_ready","eep_ready","esm_ready","esp_ready","hbhea_ready","hbheb_ready","hbhec_ready","hf_ready","ho_ready","dtm_ready","dtp_ready","dt0_ready","cscm_ready","cscp_ready"]
dcs_loss = defaultdict( float )

detector_sub = {}
detector_sub["Tracker"] = ["tracker-pixel", "tracker-strip", "tracker-track", "bpix_ready", "fpix_ready", "tibtid_ready", "tecm_ready", "tecp_ready","tob_ready"]
detector_sub["ECAL"] = ["ecal-ecal", "ecal-es", "ebm_ready","ebp_ready","eem_ready","eep_ready","esm_ready","esp_ready"]
detector_sub["HCAL"] = ["hcal-hcal", "hbhea_ready","hbheb_ready","hbhec_ready","hf_ready","ho_ready"]
detector_sub["Muon"] = ["muon-muon", "dtm_ready","dtp_ready","dt0_ready","cscm_ready","cscp_ready"]
detector_sub["L1T"] = ["l1t-l1tcalo","l1t-l1tmu"]
detector_sub["HLT"] = ["hlt-hlt"]
detector_sub["JetMET"] = ["jetmet-jetmet"]
detector_sub["EGamma"] = ["egamma-egamma"]

detector_loss = defaultdict(dict)

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
  sorted_cms_exclusive_loss = sort_dict(cms_exclusive_loss)
  sorted_cms_numerator_exclusive_loss = sort_dict(cms_numerator_exclusive_loss)
  sorted_cms_frac_exclusive_loss = sort_dict(cms_frac_exclusive_loss, 1)
  sorted_cms_detailed_frac_exclusive_loss = sort_dict(cms_detailed_frac_exclusive_loss,2)

  import matplotlib.pyplot as plt

# NOW MAKE PLOT FROM DICTIONARY VALUES
  plot_dict= defaultdict(dict)
  title_dict= defaultdict(list)
  xtitle_default = 'Luminosity Loss (/pb)'
  ytitle_default = 'Subsystem'

  # DQM flag
  plot_dict['subsystemDQMFlag_loss'] = sorted_subsystems_loss
  title_dict['subsystemDQMFlag_loss'] = ['DQM Flags vs. Inclusive Loss',xtitle_default,'DQM Flag']
  
  # DCS bits
  plot_dict['DCS_loss'] = sorted_dcs_loss
  title_dict['DCS_loss'] = ['DCS Bits vs. Inclusive Loss',xtitle_default,'DCS Bit']

  # CMS subsystem inclusive loss
  plot_dict['cms_inclusive_loss'] = sorted_cms_inclusive_loss
  title_dict['cms_inclusive_loss'] = ['Inclusive Loss from Each CMS Subsystem',xtitle_default,ytitle_default]

  
  # CMS subsystem exclusive loss
  plot_dict['cms_exclusive_loss'] = sorted_cms_exclusive_loss
  title_dict['cms_exclusive_loss'] = ['Exclusive Loss from Each CMS Subsystem',xtitle_default,ytitle_default]

  #Now make a detailed bar chart: fraction of exclusive loss due to each subdetector
  plot_dict['cms_detailed_fraction_exclusive_loss'] = sorted_cms_detailed_frac_exclusive_loss
  title_dict['cms_detailed_fraction_exclusive_loss'] = ['Fraction of Exclusive Loss from Each CMS Subsystem', 'Percentage %', ytitle_default]


  #loop over plot_dict
  icount=0
  for isub in list(plot_dict.keys()):
    dict_this = defaultdict(float)
    dict_this = plot_dict[isub]
#    print(dict_this)
    icount += 1
#    axes = plt.figure(icount, [5, 20]) # this line moved and figure size changed to suit data
    axes = plt.figure(icount) # this line moved and figure size changed to suit data
    plt.tick_params(axis='both', which='major', labelsize=6) # makes axis labels smaller
    bar_plot(dict_this,ax=axes)
    plt.title(title_dict[isub][0], fontsize=14)
    plt.xlabel(title_dict[isub][1], fontsize=14)
    plt.ylabel(title_dict[isub][2], fontsize=14)
    plt.savefig( isub+".pdf", bbox_inches='tight')




#Now make inclusive loss due to each sub system separately
  for isub in cms_sub:
    list2 = list(detector_sub[isub])
    dict_this = defaultdict(float)
    icount +=1
    for isub2 in list2:
        dict_this[isub2] = detector_loss[isub][isub2]
    sorted_thissub = sort_dict(dict_this)
    axes = plt.figure(icount)
    bar_plot(sorted_thissub,ax=axes)
    plt.title('Inclusive Loss of ' + isub + ' System', fontsize=14)
    plt.xlabel(xtitle_default, fontsize=14)
    plt.ylabel('Component', fontsize=14)
    plt.savefig( isub+"_loss.pdf", bbox_inches='tight')




#Now make a pie chart: fraction of exclusive loss due to each subdetector
  axes = plt.figure(icount+1)  
  myexplode = []
  ele = 0
  for isub in list(sorted_cms_frac_exclusive_loss.keys()):
    myexplode.append(0.01+ele*0.01)
    ele +=1 
  pie_plot(sorted_cms_frac_exclusive_loss,ax=axes,explode=myexplode)
  plt.title('Fraction of Exclusive Loss from Each CMS Subsystem', fontsize=14)
  plt.savefig( "cms_piechart_exclusive_loss.pdf", bbox_inches='tight')



#plt.show()
#plt.close('all')














