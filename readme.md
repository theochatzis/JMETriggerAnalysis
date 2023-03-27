----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:


----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_13_0_0
cd CMSSW_13_0_0/src
cmsenv
git cms-merge-topic  silviodonato:customizeHLTfor2023
git clone https://github.com/cghuh/JMETriggerAnalysis.git -b run3_13_0_X

# PFHC: preliminary HLT-PFHC for Run-3
cp /afs/cern.ch/user/c/chuh/public/PFCalibration/CMSSW_1300_126X/PFCalibration.db ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/
cp /afs/cern.ch/user/c/chuh/public/PFCalibration/CMSSW_1300_126X/HLT_dev_CMSSW_13_0_0_GRun_configDump.py ${CMSSW_BASE}/src/JMETriggerAnalysis/PFHadronCalibration/test/
cp /afs/cern.ch/user/c/chuh/public/PFCalibration/CMSSW_1300_126X/HLT_dev_CMSSW_13_0_0_GRun_configDump.py ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/

scram b -j 12
```

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------
