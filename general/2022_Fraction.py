import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#declaring lists for eras B, C, D, E, F, G

lhc_delivered = [127.74, 7006.97, 3804.41, 6749.48, 20158.45, 3618.47]
cms_recorded = [114.80, 6377.68, 3377.34, 6264.89, 18604.90, 3274.76]
DC_processed = [114.60, 6376.09, 3376.98, 6202.60, 18547.89, 3265.87]
certified = [96.56, 5021.66,  2970.05, 5806.95, 17782.29, 3085.99]


eras = ['ERA B', 'ERA C', 'ERA D', 'ERA E', 'ERA F', 'ERA G']


fig, ax = plt.subplots()

for i in range(len(eras)):
  ax.bar(eras[i], (certified[i]/cms_recorded[i]))
  

ax.bar('ALL-IN', sum(certified)/sum(cms_recorded))
ax.set_ylabel('% Fraction')
ax.set_xlabel('ERAS')
ax.set_ylim([0, 1.])
ax.set_title('2022 Fraction of Recorded Data for Physics Analysis per ERA')

plt.legend((eras[0]+' - '+ str(np.round(100*certified[0]/cms_recorded[0], 1))+'%', 
            eras[1]+' - '+ str(np.round(100*certified[1]/cms_recorded[1], 1))+'%', 
            eras[2]+' - '+ str(np.round(100*certified[2]/cms_recorded[2], 1))+'%',
            eras[3]+' - '+ str(np.round(100*certified[3]/cms_recorded[3], 1))+'%',
            eras[4]+' - '+ str(np.round(100*certified[4]/cms_recorded[4], 1))+'%',
            eras[5]+' - '+ str(np.round(100*certified[5]/cms_recorded[5], 1))+'%',
            'BCDEFG - '+ str(np.round(100*sum(certified)/sum(cms_recorded), 1))+'%'),
            scatterpoints=1,
            loc='lower left',
            ncol=2,
            fontsize=8)
#plt.show()
plt.savefig('2022_eras_phy_performance.png')

print('The sum of lhc_delivered is ', sum(lhc_delivered), '/fb')
print('The sum of CMS_recorded is ', sum(cms_recorded), '/fb')
print('The sum of DC_processed is ', sum(DC_processed), '/fb')
print('The sum of certified is ', sum(certified), '/fb')
