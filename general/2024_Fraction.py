import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#declaring lists for eraB, C, D, E
lhc_delivered = [785.95,8147.51,9119.37,3471.73]
cms_recorded = [693.27,7616.89,8505.05, 3192.19] 
DC_processed = [511.50,7613.56, 8321.01, 3191.36]
certified = [134.73,7416.59, 8151.88,3138.27]
eras = ['ERA B', 'ERA C', 'ERA D', 'ERA E']

fig, ax = plt.subplots()

for i in range(len(eras)):
  ax.bar(eras[i], (certified[i]/cms_recorded[i]))
  

ax.bar('ALL-IN', sum(certified)/sum(cms_recorded))
ax.set_ylabel('% Fraction')
ax.set_xlabel('ERAS')
ax.set_ylim([0, 1.])
ax.set_title('2024 Fraction of Recorded Data for Physics Analysis per ERA')

plt.legend((eras[0]+' - '+ str(np.round(100*certified[0]/cms_recorded[0], 1))+'%', 
            eras[1]+' - '+ str(np.round(100*certified[1]/cms_recorded[1], 1))+'%', 
            eras[2]+' - '+ str(np.round(100*certified[2]/cms_recorded[2], 1))+'%', 
            eras[3]+' - '+ str(np.round(100*certified[3]/cms_recorded[3], 1))+'%', 
            'BCDE - '+ str(np.round(100*sum(certified)/sum(cms_recorded), 1))+'%'),
            scatterpoints=1,
            loc='lower left',
            ncol=2,
            fontsize=8)
#plt.show()
plt.savefig('2024_eras_phy_performance.png')

print('The sum of lhc_delivered is ', sum(lhc_delivered), '/pb')
print('The sum of CMS_recorded is ', sum(cms_recorded), '/pb')
print('The sum of DC_processed is ', sum(DC_processed), '/pb')
print('The sum of certified is ', sum(certified), '/pb')
