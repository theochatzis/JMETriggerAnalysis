----------
----------
**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:

 * [`readme` for HLT PF-Hadron Calibrations](https://github.com/theochatzis/JMETriggerAnalysis/blob/run3_12_4_12_testTrk/PFHadronCalibration/readme.md)
 * [`readme` for HLT Jet Energy Scale Corrections](https://github.com/theochatzis/JMETriggerAnalysis/blob/run3_12_4_12_testTrk/JESCorrections/readme.md)

----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_12_4_12
cd CMSSW_12_4_12/src
cmsenv
git cms-init
# for using mixed tracking setup
git cms-merge-topic theochatzis:adriano_mixed_tracks_pf_124X

# for the JME trigger setup 
git clone https://github.com/theochatzis/JMETriggerAnalysis.git -o theochatzis -b run3_12_4_12_testTrk

scram b -j 12
```

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------

# For PUPPI paths development
The "NTuplizer" you want to run is the `jmeTriggerNTuple_cfg.py`.
You can run it as follows
```
cd JMETriggerAnalysis/NTuplizers/test
cmsRun jmeTriggerNTuple_cfg_puppiPaths.py maxEvents=10 output=test.root useMixedTrk=True
```
Options definitions:
* `maxEvents`  maximum number of events 
* `output`  name of output file 
* `useMixedTrk`  is a boolean that says if you use the modified tracks collection for PUPPI or not.

**Note** For a working PUPPI `useMixedTrk` should be set to `True`. But the "default" triggers in the current menu do not use this the PF paths used for comparison should be with this turned off.

The development of PUPPI paths can be done in the customizer `customise_hlt_puppi.py`. 
It can be found in this directory `JMETriggerAnalysis/Common/python/`.
There is a test PFPuppi path as reference namely `HLT_PFPuppiJet40_v1` trigger.

----------
