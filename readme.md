----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:


----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_14_0_5_patch1
cd CMSSW_14_0_5_patch1/src
cmsenv
git cms-init

git clone git@github.com:slehti/JMETriggerAnalysis.git -b run3_14_0_X

scram b -j 12
```

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------
