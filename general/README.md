# scripts to make DC efficiency bar plots

1. environment setup

```
bash
source setup_virtualenv_plot.sh
```

2. Find out the LHC delivered, CMS recorded integrated luminosity. Say if your run range is xxxxxx and yyyyyy, the LHC delivered and CMS recorded luminosity could be found out by running brilcalc
```
bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
brilcalc lumi -b "STABLE BEAMS" --amodetag PROTPHYS --begin xxxxxx --end yyyyyy -c web -u /pb
```


3. Find out the DC Processed luminosity. There are two ways to obtain these numbers. The first one is more precise but the difference between these two numbers is less than 1%. 

   a. Use the output of the inputcsv step from the luminosity loss scripts, say eraC.json. This step includes all the LSs from Collision runs (of a given list) that have beam_present and beam_stable flags = true and magnetic field >=3.7 Tesla
```
bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
pip install --user brilws
brilcalc lumi -b "STABLE BEAMS" -c web -i eraC.json -u /pb 
```

   b. Use the list of runs you send for DC. For example, eraC_runs.txt and this script https://github.com/syuvivida/DQMSpace/blob/main/brilcalc_scripts/run_brilcalc_runByFile.sh
```
  ./run_brilcalc_runByFile.sh eraC_runs.txt
```


4. Replace the numbers in these arrays https://github.com/syuvivida/DQMSpace/blob/main/general/2023_DCeff.py#L6-L9
and make DC efficiency plots (Certified/DC processed). Note the units of these numbers are in pb.
```
python 2023_DCeff.py
```


5. Replace the numbers in these arrays https://github.com/syuvivida/DQMSpace/blob/main/general/2023_Fraction.py#L5-L8
and make DC efficiency plots (Certified/DC recorded). Note the units of these numbers are in pb.
```
python 2023_Fraction.py
```

