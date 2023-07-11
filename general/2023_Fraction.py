import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

lhc_delivered = [1347.233,20293.138]
cms_recorded = [1206.337,18678.383] 
DC_processed = [1166.744,18393.594]
certified = [646.606, 17885.342]
eras = ['ERA B', 'ERA C']

fig, ax = plt.subplots()

for i in range(len(eras)):
  ax.bar(eras[i], (certified[i]/cms_recorded[i]))
  

ax.bar('ALL-IN', sum(certified)/sum(cms_recorded))
ax.set_ylabel('% Fraction')
ax.set_xlabel('ERAS')
ax.set_ylim([0, 1.])
ax.set_title('2023 Fraction of Recorded Data for Physics Analysis per ERA')

plt.legend((eras[0]+' - '+ str(np.round(100*certified[0]/cms_recorded[0], 1))+'%', 
            eras[1]+' - '+ str(np.round(100*certified[1]/cms_recorded[1], 1))+'%', 
            'BC - '+ str(np.round(100*sum(certified)/sum(cms_recorded), 1))+'%'),
            scatterpoints=1,
            loc='lower left',
            ncol=2,
            fontsize=8)
#plt.show()
plt.savefig('2023_eras_phy_performance.png')

print('The sum of lhc_delivered is ', sum(lhc_delivered), '/fb')
print('The sum of CMS_recorded is ', sum(cms_recorded), '/fb')
print('The sum of DC_processed is ', sum(DC_processed), '/fb')
print('The sum of certified is ', sum(certified), '/fb')