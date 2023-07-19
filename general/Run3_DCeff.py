import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


lhc_delivered = [128.677708816, 6923.811533014, 3744.766288761, 6591.521279814,  19963.428480688, 3588.249028983, 1347.232724045,20290.564409034, 528.661029963]
cms_recorded = [115.431714499, 6301.260269901, 3323.165454419, 6117.173986822, 18364.160197481, 3247.131159904, 1206.336949574,18678.382888073,489.304180405]
DC_processed = [115.229724697, 6300.513719316, 3322.858446144, 6064.241668777, 18364.160197481, 3245.416412439, 1166.744389096, 18393.593772634, 373.808188464]
certified = [96.351250788, 4953.263590896,  2922.311186040, 5671.636672136, 17610.214712638, 3055.423061552, 646.606229207, 17885.342426876,353.318393169]

eras = ['22-B', '22-C', '22-D', '22-E', '22-F', '22-G', '23-B', '23-C', '23-D']

fig, ax = plt.subplots()

for i in range(len(eras)):
  ax.bar(eras[i], (certified[i]/DC_processed[i]))

#2022 only
deno_2022 = 0
nume_2022 = 0
for i in range(len(eras)):
  if '22' in eras[i]:
    deno_2022 += DC_processed[i]
    nume_2022 += certified[i]
ax.bar('2022',(nume_2022/deno_2022))

#2023 only
deno_2023 = 0
nume_2023 = 0
for i in range(len(eras)):
  if '23' in eras[i]:
    deno_2023 += DC_processed[i]
    nume_2023 += certified[i]
ax.bar('2023',(nume_2023/deno_2023))
  

ax.bar('ALL-IN', sum(certified)/sum(DC_processed))
ax.set_ylabel('% DC Performance')
ax.set_xlabel('ERAS')
ax.set_ylim([0, 1.])
ax.set_title('Run 3 Performance of Data Certification per ERA')

plt.legend((eras[0]+' - '+ str(np.round(100*certified[0]/DC_processed[0], 1))+'%', 
            eras[1]+' - '+ str(np.round(100*certified[1]/DC_processed[1], 1))+'%', 
            eras[2]+' - '+ str(np.round(100*certified[2]/DC_processed[2], 1))+'%', 
            eras[3]+' - '+ str(np.round(100*certified[3]/DC_processed[3], 1))+'%',
            eras[4]+' - '+ str(np.round(100*certified[4]/DC_processed[4], 1))+'%',
            eras[5]+' - '+ str(np.round(100*certified[5]/DC_processed[5], 1))+'%',
            eras[6]+' - '+ str(np.round(100*certified[6]/DC_processed[6], 1))+'%',
            eras[7]+' - '+ str(np.round(100*certified[7]/DC_processed[7], 1))+'%',
            eras[8]+' - '+ str(np.round(100*certified[8]/DC_processed[8], 1))+'%',
            '2022 - ' + str(np.round(100*nume_2022/deno_2022, 1))+'%',
            '2023 - ' + str(np.round(100*nume_2023/deno_2023, 1))+'%',
            '2022+2023 - '+ str(np.round(100*sum(certified)/sum(DC_processed), 1))+'%'),
            scatterpoints=1,
            loc='lower left',
            ncol=2,
            fontsize=8)
#plt.show()
plt.savefig('run3_eras_DC_performance.png')

print('The sum of lhc_delivered is ', sum(lhc_delivered), '/fb')
print('The sum of CMS_recorded is ', sum(cms_recorded), '/fb')
print('The sum of DC_processed is ', sum(DC_processed), '/fb')
print('The sum of certified is ', sum(certified), '/fb')
