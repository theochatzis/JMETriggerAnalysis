----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:


----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_13_0_7_patch1
cd CMSSW_13_0_7_patch1/src
cmsenv
git cms-merge-topic  silviodonato:customizeHLTfor2023
git clone https://github.com/theochatzis/JMETriggerAnalysis.git -b run3_13_0_X

# PFHC: preliminary HLT-PFHC for Run-3
<<<<<<< HEAD
cp /afs/cern.ch/user/c/chuh/public/PFCalibration/CMSSW_1300_126X/PFCalibration.db ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/
=======
>>>>>>> 99f6750c1d15adb4a5891431db67c72ad09825ac

scram b -j 12
```

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------
