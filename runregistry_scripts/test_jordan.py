import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#declaring lists
lhc_delivered = [0.13, 6.92, 3.74, 6.59, 18.35]
#cms_recorded = [0.12, 6.30, 3.32, 6.12, 16.93]
#certified = [0.08, 4.88, 2.90, 5.53, 15.91]
cms_recorded = [0.1152,6.301, 3.323,6.064, 18.364, 3.245]
certified = [0.0846,  4.881,2.905,5.672, 17.610,2.553]
eras = ['ERA B', 'ERA C', 'ERA D', 'ERA E', 'ERA F', 'ERA G']

fig, ax = plt.subplots()

for i in range(len(eras)):
  ax.bar(eras[i], (certified[i]/cms_recorded[i]))
  

ax.bar('ALL-IN', sum(certified)/sum(cms_recorded))
ax.set_ylabel('% DC Performance')
ax.set_xlabel('ERAS')
ax.set_ylim([0, 1.])
ax.set_title('DC Performance from Recorded Luminosity per ERA')

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
#plt.savefig('eras_DC_performance.jpg')
plt.savefig('eras_DC_performance.png')

print('The sum of lhc_delivered is {sum(lhc_delivered)}')
print('The sum of cms_recorded is {sum(cms_recorded)}')
print('The sum of certified is {sum(certified)}')
