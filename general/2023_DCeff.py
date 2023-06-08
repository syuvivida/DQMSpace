import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#declaring lists
lhc_delivered = [1347.232724045,10953.189454178]
cms_recorded = [1206.336949574,10066.438915417] 
#certified = [0.08, 4.88, 2.90, 5.53, 15.91]
DC_processed = [1170.901819678, 10059.744398394]
certified = [696.926160397, 9883.676626747]
eras = ['ERA B', 'ERA C']

fig, ax = plt.subplots()

for i in range(len(eras)):
  ax.bar(eras[i], (certified[i]/DC_processed[i]))
  

ax.bar('ALL-IN', sum(certified)/sum(DC_processed))
ax.set_ylabel('% DC Performance')
ax.set_xlabel('ERAS')
ax.set_ylim([0, 1.])
ax.set_title('2023 Performance of Data Certification per ERA')

plt.legend((eras[0]+' - '+ str(np.round(100*certified[0]/DC_processed[0], 1))+'%', 
            eras[1]+' - '+ str(np.round(100*certified[1]/DC_processed[1], 1))+'%', 
            'BC - '+ str(np.round(100*sum(certified)/sum(DC_processed), 1))+'%'),
            scatterpoints=1,
            loc='lower left',
            ncol=2,
            fontsize=8)
#plt.show()
plt.savefig('2023_eras_DC_performance.png')

print('The sum of lhc_delivered is ', sum(lhc_delivered), '/fb')
print('The sum of CMS_recorded is ', sum(cms_recorded), '/fb')
print('The sum of DC_processed is ', sum(DC_processed), '/fb')
print('The sum of certified is ', sum(certified), '/fb')
