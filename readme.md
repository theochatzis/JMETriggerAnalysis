----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:

 * [`readme` for HLT PF-Hadron Calibrations](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3_12_3_X/PFHadronCalibration/readme.md)
 * [`readme` for HLT Jet Energy Scale Corrections](https://github.com/sparedes/JMETriggerAnalysis/blob/run3/JESCorrections/readme.md)

----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_12_3_0_pre4
cd CMSSW_12_3_0_pre4/src
cmsenv
git clone https://github.com/pallabidas/JMETriggerAnalysis.git -o pallabidas -b run3_12_3_X

# PFHC: preliminary HLT-PFHC for Run-3
cp /afs/cern.ch/work/p/pdas/public/run3/PFHC_Run3Winter21_HLT_V3.db ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/

# JESC: preliminary HLT-JESCs for Run-3
cp /afs/cern.ch/work/p/pdas/public/run3/JESC_Run3Winter21_V2_MC.db ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/

scram b -j 12
```

The baseline HLT menu for Run-3 in 12_3_X can be found in
[Common/python/configs/HLT_dev_CMSSW_12_3_0_GRun_configDump.py](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3_12_3_X/Common/python/configs/HLT_dev_CMSSW_12_3_0_GRun_configDump.py).

It was created with `hltGetConfiguration` via the commands listed in
[`Common/test/dumpHLTMenus_mcRun3.sh`](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3_12_3_X/Common/test/dumpHLTMenus_mcRun3.sh).

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------
