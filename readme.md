----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:

----------
----------

### Tools for JME studies on the Run-3 HLT reconstruction

```
cmsrel CMSSW_14_0_14
cd CMSSW_14_0_14/src
cmsenv
git cms-init
git cms-merge-topic theochatzis:testMHTforFwd
git clone git@github.com:theochatzis/JMETriggerAnalysis.git -b run3_14_0_X

scram b -j 12
```

Test command:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root
```

----------

### Getting the HLT Menu configuration

Following the [STORM twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#CMSSW_14_0_X_presently_used_for) for menu development you can find the `hltGetConfiguration` command arguments needed to produce your HLT menu.

An example of such a command is:
```
hltGetConfiguration /dev/CMSSW_14_0_0/GRun \
   --globaltag auto:phase1_2024_realistic \
   --mc \
   --unprescale \
   --output minimal \
   --max-events 10 \
   --input /store/mc/Run3Winter24Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/133X_mcRun3_2024_realistic_v8-v2/80000/dc984f7f-2e54-48c4-8950-5daa848b6db9.root \
   --eras Run3_2024 --l1-emulator uGT --l1 L1Menu_Collisions2024_v1_3_0_xml \
   --path MC_*,HLTriggerF*,Status*,HLT_PFJet60_v*,HLT_PFJet140_v*,HLT_PFJet320_v*,HLT_PFJet500_v*,HLT_PFHT780_v*,HLT_PFHT890_v*,HLT_PFHT1050_v*,HLT_PFMET*_PFMHT*_IDTight_v* \
   > tmp.py

# dump configuration 
edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_14_0_0_GRun_configDump.py
```
the `--path` option is not mandatory, but can help to process the events faster as it only creates a sub-menu with the paths listed. You always need the `Status*`,`HLTriggerFinalPath` as these techincal paths are essential for a trigger menu to run.

We store the menus in `Common/python/configs` directory and use shell scripts to produce them in `Common/test`. For example you can do:
```
./dumpHLTMenus_mcRun3.sh
```
and get the menu produced.



