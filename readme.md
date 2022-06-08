----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:

 * [`readme` for HLT PF-Hadron Calibrations](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3_12_3_X/PFHadronCalibration/readme.md)
 * [`readme` for HLT Jet Energy Scale Corrections](https://github.com/sparedes/JMETriggerAnalysis/blob/run3_12_3_X/JESCorrections/readme.md)

----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_12_4_0_pre3
cd CMSSW_12_4_0_pre3/src
cmsenv
git clone https://github.com/pallabidas/JMETriggerAnalysis.git -o pallabidas -b run3_12_4_X

# PFHC: preliminary HLT-PFHC for Run-3
cp /afs/cern.ch/work/p/pdas/public/run3/PFHC_Run3Winter21_HLT_V3.db ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/

# JESC: preliminary HLT-JESCs for Run-3
cp /afs/cern.ch/work/p/pdas/public/run3/JESC_Run3Winter21_V2_MC.db ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/

scram b -j 12
```

NOTE: HLT-menu development is presently done in the 12_3_X release cycle. This means that the HLT configs for 12_4_X (e.g. /dev/CMSSW_12_4_0/GRun) do not include some of the updates included in the HLT configs for 12_3_X (e.g. /dev/CMSSW_12_3_0/GRun). The instructions given below for the 12_4_X release cycle are thus based on the 12_3_X HLT menu (i.e. /dev/CMSSW_12_3_0/GRun).

The baseline HLT menu for Run-3 in 12_3_X can be found in
[Common/python/configs/HLT_dev_CMSSW_12_3_0_GRun_configDump.py](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3_12_4_X/Common/python/configs/HLT_dev_CMSSW_12_3_0_GRun_configDump.py).

It was created with `hltGetConfiguration` via the commands listed in
[`Common/test/dumpHLTMenus_mcRun3.sh`](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3_12_4_X/Common/test/dumpHLTMenus_mcRun3.sh).

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------
