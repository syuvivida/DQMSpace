import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#declaring lists for eras B, C, D, E, F, G
lhc_delivered = [127.74, 7006.97, 3804.41, 6749.48, 20158.45, 3618.47]
cms_recorded = [114.80, 6377.68, 3377.34, 6264.89, 18604.90, 3274.76]
                                                                                                            
DC_processed = [114.60, 6375.95, 3376.98, 6202.45, 18547.89, 3246.70]
certified = [96.56, 5019.58,  2970.05, 5806.95, 17782.22, 3085.99]


eras = ['ERA B', 'ERA C', 'ERA D', 'ERA E', 'ERA F', 'ERA G']

fig, ax = plt.subplots()

for i in range(len(eras)):
  ax.bar(eras[i], (certified[i]/DC_processed[i]))
  

ax.bar('ALL-IN', sum(certified)/sum(DC_processed))
ax.set_ylabel('% DC Performance')
ax.set_xlabel('ERAS')
ax.set_ylim([0, 1.])
ax.set_title('2022 Performance of Data Certification per ERA')


plt.legend((eras[0]+' - '+ str(np.round(100*certified[0]/DC_processed[0], 1))+'%', 
            eras[1]+' - '+ str(np.round(100*certified[1]/DC_processed[1], 1))+'%', 
            eras[2]+' - '+ str(np.round(100*certified[2]/DC_processed[2], 1))+'%', 
            eras[3]+' - '+ str(np.round(100*certified[3]/DC_processed[3], 1))+'%',
            eras[4]+' - '+ str(np.round(100*certified[4]/DC_processed[4], 1))+'%',
            eras[5]+' - '+ str(np.round(100*certified[5]/DC_processed[5], 1))+'%',
            'BCDEFG - '+ str(np.round(100*sum(certified)/sum(DC_processed), 1))+'%'),
            scatterpoints=1,
            loc='lower left',
            ncol=2,
            fontsize=8)
#plt.show()
plt.savefig('2022_eras_DC_performance.png')

print('The sum of lhc_delivered is ', sum(lhc_delivered), '/fb')
print('The sum of CMS_recorded is ', sum(cms_recorded), '/fb')
print('The sum of DC_processed is ', sum(DC_processed), '/fb')
print('The sum of certified is ', sum(certified), '/fb')
