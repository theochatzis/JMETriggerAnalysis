----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:

 * [`readme` for HLT PF-Hadron Calibrations](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3/PFHadronCalibration/readme.md)
 * [`readme` for HLT Jet Energy Scale Corrections](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3/JESCorrections/readme.md)

----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

* [Tests on HLT Tracking for Run-3](#tests-on-hlt-tracking-for-run-3)

----------

### Tests on HLT Tracking for Run-3

```
cmsrel CMSSW_12_0_1
cd CMSSW_12_0_1/src
cmsenv
git cms-merge-topic pallabidas:test_HLT_12_0_1

git clone https://github.com/pallabidas/JMETriggerAnalysis.git -o pallabi -b run3

# external data
mkdir -p ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/data

# PFHC: preliminary HLT-PFHC for Run-3
cp /afs/cern.ch/work/p/pdas/public/run3/PFHC_Run3Winter20_HLT_v01.db \
   ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/data/PFHC_Run3Winter20_HLT_v01.db

# JESC: preliminary HLT-JESCs for Run-3
cp /afs/cern.ch/work/p/pdas/public/run3/JESC_Run3Winter20_V2_MC.db \
   ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter20_V2_MC.db

scram b -j 12
```

The baseline HLT menu for Run-3 in 12_0_X can be found in
[Common/python/configs/HLT_dev_CMSSW_12_0_0_GRun_V6_configDump.py](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3/Common/python/configs/HLT_dev_CMSSW_12_0_0_GRun_V6_configDump.py).

It was created with `hltGetConfiguration` via the commands listed in
[`Common/test/dumpHLTMenus_mcRun3.sh`](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3/Common/test/dumpHLTMenus_mcRun3.sh).

An example of how to enable the different tracking customisations can be found in
[`NTuplizers/test/jmeTriggerNTuple_cfg.py`](https://github.com/pallabidas/JMETriggerAnalysis/blob/run3/NTuplizers/test/jmeTriggerNTuple_cfg.py)
(see option `reco`).
Test commands:
```
# (a) Run-3 tracking: standard
cmsRun jmeTriggerNTuple_cfg.py maxEvents=1 reco=HLT_Run3TRK output=out_HLT_Run3TRK.root

# (b) Run-3 tracking: all pixel vertices
cmsRun jmeTriggerNTuple_cfg.py maxEvents=1 reco=HLT_Run3TRKWithPU output=out_HLT_Run3TRKWithPU.root
```

----------
