import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#declaring lists for eras B, C, D, E, F, G
lhc_delivered = [128.677708816, 6923.811533014, 3744.766288761, 6591.521279814,  19963.428480688, 3588.249028983]
cms_recorded = [115.431714499, 6301.260269901, 3323.165454419, 6117.173986822, 18364.160197481, 3247.131159904]
                                                                                                            
DC_processed = [115.229724697, 6300.513719316, 3322.858446144, 6064.241668777, 18364.160197481, 3245.416412439]
certified = [96.351250788, 4953.263590896,  2922.311186040, 5671.636672136, 17610.214712638, 3055.42306155]



#lhc_delivered = [0.1287,6.924,3.745,6.592,19.963,3.588]
#cms_recorded = [0.1154,6.301,3.323,6.117,18.423,3.247] 
#certified = [0.08, 4.88, 2.90, 5.53, 15.91]
#DC_processed = [0.1152,6.301, 3.323,6.064, 18.364, 3.245]
#certified = [0.0964,  4.953,2.922,5.672, 17.610,3.055]
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
