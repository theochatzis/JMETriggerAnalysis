----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:

 * [`readme` for HLT PF-Hadron Calibrations](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3_12_3_X/PFHadronCalibration/readme.md)
 * [`readme` for HLT Jet Energy Scale Corrections](https://github.com/missirol/JMETriggerAnalysis/blob/run3/JESCorrections/readme.md)

----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_12_4_0_pre3
cd CMSSW_12_4_0_pre3/src
cmsenv
git clone https://github.com/cghuh/JMETriggerAnalysis.git -b run3_13_0_X

# PFHC: preliminary HLT-PFHC for Run-3
cp /afs/cern.ch/user/c/chuh/public/PFCalibration/CMSSW_1300_126X/PFCalibration.db ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/
cp /afs/cern.ch/user/c/chuh/public/PFCalibration/HLT_dev_CMSSW_13_0_0_GRun_configDump.py ${CMSSW_BASE}/src/JMETriggerAnalysis/PFHadronCalibration/test/
cp /afs/cern.ch/user/c/chuh/public/PFCalibration/HLT_dev_CMSSW_13_0_0_GRun_configDump.py ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/

scram b -j 12
```

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------
