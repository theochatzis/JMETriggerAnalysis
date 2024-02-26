----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:
- [JECs instructions](https://github.com/theochatzis/JMETriggerAnalysis/tree/run3_13_3_X_jecs/JESCorrections/readme.md)
- [PFHCs instructions](https://github.com/theochatzis/JMETriggerAnalysis/blob/run3_13_3_X_jecs/PFHadronCalibration/readme.md)

----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_13_3_1_patch1
cd CMSSW_13_3_1_patch1/src
cmsenv
git cms-init

git clone https://github.com/theochatzis/JMETriggerAnalysis.git -b run3_13_3_X_jecs

scram b -j 12
```

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------
