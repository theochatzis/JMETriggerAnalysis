## Tools for JME studies on the Phase-2 HLT reconstruction
* [Setup](##Setup)
* [Useful links](###-Useful-links)
* [Phase 2 Tasks](##-Phase-2-Tasks)

----------

## Setup
### Test setup 

```shell
cmsrel CMSSW_15_1_0_pre4
cd CMSSW_15_1_0_pre4/src
cmsenv
git cms-init
#git cms-merge-topic theochatzis:trimmedTrackingPUPPI # add trimming from tracking + mixed tracks modifications for PUPPI. # Commented for now
git clone git@github.com:theochatzis/JMETriggerAnalysis.git -b master_phase2
scram b -j 12
```

## Instructions
### Making the menu config file
To make the configuration file of the trigger menu we use the `cmsDriver` commands from the central page:
https://cmshltupgrade.docs.cern.ch/RunningInstructions/ 

There is an executable script which makes such config files in `JMETriggerAnalysis/Common/python/configs/simplifiedMenuConfig.sh`. This script produces both the L1 and the HLT Menus configs.

### Running the menu and making NTuples
For this we use the `NTuplizers/test` area. There you can find the two useful scripts:
- `jmeTriggerNTuple_L1Only_cfg.py` : this script just runs the L1 Menu and removes info from the output to reduce heavily the space allocated by the output file.
- `jmeTriggerNTuple.cfg` : From this script we are able to make "JMETriggerNTuple"-structured output ROOT files.  

First should create the L1 output fed to the HLT step after.

You can test locally by using the `./runLocally.sh` shell script.

For batch submission one can use an executable in CRAB and run the two steps using a crab config file. An example crab config file that can be used is `crab_cfg.py`.

### JECs derivation (Fast JECs iteration)
Additionally to the JMETriggerAnalysis package, you need to add the JetMETAnalysi using:
```
git clone https://github.com/theochatzis/JetMETAnalysis.git -b hlt_run3
```
Steps:
- Make JRA NTuples with `NTuplizers/test/jescJRA_cfg.py`. Example at `runLocallyJRA.sh`.
- Run the analysis for deriving JECs.

### Useful links
- [Phase 2 Google Doc](https://docs.google.com/document/d/1EkEUHmPk8S2aB78rGi_Bh-89ip59Pyg-PclPrdL6iGs/edit?usp=sharing)
- [HLT Phase2 documentation](https://cmshltupgrade.docs.cern.ch/)
- [HLT Phase-2 TWiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HighLevelTriggerPhase2)

## Phase 2 Tasks
### HGCAL TICL update
*Motivation*
HGCAL is the game changer in our calorimetry for CMS in Phase 2. As the basic clustering/"particle flow" algorithm for HGCAL changes (TICL) we need to check the performance improvements on our hadrons/jets.

New report from PF:
https://indico.cern.ch/event/1590668/contributions/6703246/subcontributions/573268/attachments/3154421/5602539/PFPlans.pdf 

Action items:
- Check if regression can be helpful 
- new TICLv5 jecs and performance comparison

### Performance Validation
*Motivation*
PUPPI Jets/MET performance is changing due to releases updates from developments in CMSSW. We need to make sure no degradation is observed and potentially see where our weaknesses are to improve as we move on.

Action item:
- Try the validation framework from NGT which is centrally available from now on.
- Check Sam's tool for GUI plotting effiicencies (so far has limited paths but we can add). (presentation from Sam: https://indico.cern.ch/event/1502063/#21-phase2-hlt-validation-confd)

### PF+PUPPI performance with new tracking and updates
*Motivation*
Tracking is the basic component for PUPPI as it heavily affects the algorithm by relying on it. For this reason we study:
- Changes from TRK POG in how track is reconstructred. Migration from Legacy to new tracking (Patatrack + LST -> MkFit)
- Study how we can improve events where the leading vertex is not correct.

Action items:
- So far waiting for recipe from TRK POG for new tracking. No need for comparison with current developments.

### Calo Jets for Phase 2 
*Motivation*
Create calo based jets i.e. no tracking which are fast and can help in :
- preselection filters in our triggers
- create potentially regional tracking - this could improve our tracking performance for PUPPI.

Action items:
- Make a dummy customization that adds a calo jet collection in the HLT Phase 2 menu.

### PUPPI PU Jet ID 
*Motivation*
Idea is to create an MVA discriminator (BDT for starters) to create a PU Jet ID on top of PUPPI jets. This can use standard ID from Phase 1, but also new precision timing variables. In context of Phase 2 we can use the PU Jet ID for:
- Assisting PUPPI gain purity in regions without tracks (from jet shape variables).
- Regaining efficiency when PUPPI is "too agressive" by relaxing it and letting ID help with remaining PU jets.

Action items:
- Add variables in our "JMETriggerNTuple", using the interface and plugins in NTuplizers/test for the PF reco jets object type.
