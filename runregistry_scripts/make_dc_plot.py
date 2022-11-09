
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
subsystems = ["l1t-l1tmu", "l1t-l1tcalo", "hlt-hlt", "tracker-pixel", "tracker-strip", "tracker-track", "ecal-ecal", "ecal-es", "egamma-egamma", "hcal-hcal", "muon-muon", "jetmet-jetmet", "lumi-lumi"]
subsystems_losses = defaultdict( float )

for row in lumi_file_reader:
  run  = int(row[0])
  delivered = float(row[2])/1000000.
  recorded  = float(row[3])/1000000.
  
  bits = eval( row[4] )
  if not bits : continue # all good in JSON

  for subsystem in subsystems:
    if bits[subsystem] == "GOOD" : continue
    subsystems_losses[ subsystem ] += recorded

print( subsystems_losses )

# NOW MAKE PLOT FROM DICTIONARY VALUES
import matplotlib.pyplot as plt

plt.barh( list(subsystems_losses.keys()), list(subsystems_losses.values()) )
plt.title('Subsystem v.s. Loss', fontsize=14)
plt.xlabel('Luminosity loss (/pb)', fontsize=14)
plt.ylabel('Subsystem', fontsize=14)
plt.savefig( "subsystem_loses.pdf", bbox_inches='tight')
plt.show()




















