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
cmsrel CMSSW_12_4_12
cd CMSSW_12_4_12/src
cmsenv
git cms-init
# for using mixed tracking setup
git cms-merge-topic AdrianoDee:mixed_tracks_pf_124X

# for the JME trigger setup 
git clone https://github.com/theochatzis/JMETriggerAnalysis.git -o theochatzis -b run3_12_4_12_testTrk

scram b -j 12
```

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------
