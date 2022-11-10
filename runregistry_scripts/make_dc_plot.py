
from collections import defaultdict
import runregistry
import matplotlib

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
subsystems = ["l1t-l1tmu", "l1t-l1tcalo", "hlt-hlt", "tracker-pixel", "tracker-strip", "tracker-track", "ecal-ecal", "ecal-es", "egamma-egamma", "hcal-hcal", "muon-muon", "jetmet-jetmet"]
subsystems_loss = defaultdict( float )

dcs_sub =   ["bpix_ready", "fpix_ready", "tibtid_ready", "tecm_ready", "tecp_ready","tob_ready","ebm_ready","ebp_ready","eem_ready","eep_ready","esm_ready","esp_ready","hbhea_ready","hbheb_ready","hbhec_ready","hf_ready","ho_ready","dtm_ready","dtp_ready","dt0_ready","cscm_ready","cscp_ready"]
dcs_loss = defaultdict( float )

tracker_sub =   ["tracker-pixel", "tracker-strip", "tracker-track", "bpix_ready", "fpix_ready", "tibtid_ready", "tecm_ready", "tecp_ready","tob_ready"]
tracker_loss = defaultdict( float )

ecal_sub =   ["ecal-ecal", "ecal-es", "ebm_ready","ebp_ready","eem_ready","eep_ready","esm_ready","esp_ready"]
ecal_loss = defaultdict( float )

hcal_sub =   ["hcal-hcal", "hbhea_ready","hbheb_ready","hbhec_ready","hf_ready","ho_ready"]
hcal_loss = defaultdict( float )


muon_sub =   ["muon-muon", "dtm_ready","dtp_ready","dt0_ready","cscm_ready","cscp_ready"]
muon_loss = defaultdict( float )

cms_sub = ["Tracker", "ECAL", "HCAL", "Muon"]
cms_loss = defaultdict( float )
cms_status = defaultdict( bool )

for row in lumi_file_reader:
  run  = int(row[0])
#  print("Run ",run)
  delivered = float(row[2])/1000000.
  recorded  = float(row[3])/1000000.
  
  bits = eval( row[4] )
  if not bits : continue # all good in JSON
  
  for subsystem in subsystems:
    if bits[subsystem] == "GOOD" : continue
    subsystems_loss[ subsystem ] += recorded

  for dcs_subsystem in dcs_sub:
    if bits[dcs_subsystem] == True : continue
#    print("bit ",bits[dcs_subsystem])
    dcs_loss[ dcs_subsystem ] += recorded

   # Now check tracker
  cms_status [ "Tracker" ] = True 
  for itrack in tracker_sub:
    if bits[itrack] == True or bits[itrack]== "GOOD" : continue
    cms_status [ "Tracker" ] = False 
    tracker_loss[ itrack ] += recorded 
  if cms_status [ "Tracker" ] == False: cms_loss [ "Tracker" ] += recorded

   # Now check ECAL
  cms_status [ "ECAL" ] = True 
  for iecal in ecal_sub:
    if bits[iecal] == True or bits[iecal]== "GOOD" : continue
    cms_status [ "ECAL" ] = False 
    ecal_loss[ iecal] += recorded 
  if cms_status [ "ECAL" ] == False: cms_loss [ "ECAL" ] += recorded

   # Now check HCAL
  cms_status [ "HCAL" ] = True 
  for ihcal in hcal_sub:
    if bits[ihcal] == True or bits[ihcal]== "GOOD" : continue
    cms_status [ "HCAL" ] = False 
    hcal_loss[ ihcal] += recorded 
  if cms_status [ "HCAL" ] == False: cms_loss [ "HCAL" ] += recorded

   # Now check Muon
  cms_status [ "Muon" ] = True 
  for imuon in muon_sub:
    if bits[imuon] == True or bits[imuon]== "GOOD" : continue
    cms_status [ "Muon" ] = False 
    muon_loss[ imuon] += recorded 
  if cms_status [ "Muon" ] == False: cms_loss [ "Muon" ] += recorded

print( subsystems_loss )
print( dcs_loss )
print( tracker_loss )
print( ecal_loss )
print( hcal_loss )
print( muon_loss )
print( cms_loss )

# NOW MAKE PLOT FROM DICTIONARY VALUES
import matplotlib.pyplot as plt
plt.figure(1)
plt.barh( list(subsystems_loss.keys()), list(subsystems_loss.values()) )
plt.title('Subsystem v.s. Loss', fontsize=14)
plt.xlabel('Luminosity loss (/pb)', fontsize=14)
plt.ylabel('Subsystem', fontsize=14)
plt.savefig( "subsystemDQMFlag_loss.pdf", bbox_inches='tight')


#Now make inclusive loss due to DCS figures
plt.figure(2)
plt.barh( list(dcs_loss.keys()), list(dcs_loss.values()) )
plt.title('DCS bit v.s. Loss', fontsize=14)
plt.xlabel('Luminosity loss (/pb)', fontsize=14)
plt.ylabel('Subsystem', fontsize=14)
plt.savefig( "DCS_loss.pdf", bbox_inches='tight')


#Now make inclusive loss due to Tracker
plt.figure(3)
plt.barh( list(tracker_loss.keys()), list(tracker_loss.values()) )
plt.title('Loss of Tracker System', fontsize=14)
plt.xlabel('Luminosity loss (/pb)', fontsize=14)
plt.ylabel('Component', fontsize=14)
plt.savefig( "tracker_loss.pdf", bbox_inches='tight')


#Now make inclusive loss due to ECAL
plt.figure(4)
plt.barh( list(ecal_loss.keys()), list(ecal_loss.values()) )
plt.title('Loss of ECAL System', fontsize=14)
plt.xlabel('Luminosity loss (/pb)', fontsize=14)
plt.ylabel('Component', fontsize=14)
plt.savefig( "ecal_loss.pdf", bbox_inches='tight')


#Now make inclusive loss due to HCAL
plt.figure(5)
plt.barh( list(hcal_loss.keys()), list(hcal_loss.values()) )
plt.title('Loss of HCAL System', fontsize=14)
plt.xlabel('Luminosity loss (/pb)', fontsize=14)
plt.ylabel('Component', fontsize=14)
plt.savefig( "hcal_loss.pdf", bbox_inches='tight')

#Now make inclusive loss due to Muon
plt.figure(6)
plt.barh( list(muon_loss.keys()), list(muon_loss.values()) )
plt.title('Loss of Muon System', fontsize=14)
plt.xlabel('Luminosity loss (/pb)', fontsize=14)
plt.ylabel('Component', fontsize=14)
plt.savefig( "muon_loss.pdf", bbox_inches='tight')

plt.show()



plt.close('all')














