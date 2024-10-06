### Itroduction
Welcome to JMETriggerAnalysis framework! 

This framework is used for HLT studies and more specificaly it has three main functionalities:
* Production of JME Trigger NTuples. These NTuples are containing information per event about trigger bits (e.g. if the event is accepted by a given path)and the Jets and MET objects (hlt and offline). 
* Analysis of the NTuples produced by the framework. This means creating plots of performances of objects like responses of jets w.r.t. offline/generated and trigger efficiencies. 
* Production of NTuples used in Jet Energy Corrections (JECs).
* Production of NTuples used in PF hadron calibrations (PFHCs).

For each of the above there is a corresponding directory:
* NTuplizers
* NTupleAnalysis
* JESCorrections
* PFHadronCalibration

For the last two there is available documentation in the subdirectories. (Note: need instructions for PFHC - to be added)

----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:
- [JECs instructions](https://github.com/theochatzis/JMETriggerAnalysis/tree/run3_13_3_X_jecs/JESCorrections/readme.md)
- [PFHCs instructions](https://github.com/theochatzis/JMETriggerAnalysis/blob/run3_13_3_X_jecs/PFHadronCalibration/readme.md)

----------
----------

### Setup instructions

To setup the framework you need CMSSW and as such a working LXPLUS account. Currently the recommended LXPLUS version is LXPLUS8, so login as follows:
```
ssh -Y <user_name>@lxplus8.cern.ch
```
then in any directory setup the framework:
```
cmsrel CMSSW_14_0_14
cd CMSSW_14_0_14/src
cmsenv
git cms-init
## --- You can find bellow useful additions to standard CMSSW for relevant studies ---
## Only use those in case you want to perform such a study. 
# Use this merge-topic in case you want to study removal of low pT jets in MHT
git cms-merge-topic theochatzis:testMHTforFwd

# In case you want to study the new CaloTowers update
git cms-addpkg RecoLocalCalo/CaloTowersCreator
git cherry-pick 979e2299d39a803bcdfec5b20ad083e67f7a30dc
## -----------------------------------------------------------------------------------

git clone git@github.com:theochatzis/JMETriggerAnalysis.git -b run3_14_0_X


# Build
scram b -j 12
```
Make sure the menu is updated (see bellow section : Getting the HLT Menu configuration).
Do:
```
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/Common/test
./dumpHLTMenus_mcRun3.sh
```

Test command:
```
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root
```

----------

### Tools for JME studies on the Run-3 HLT reconstruction

<<<<<<< HEAD
Here the main structure of the logic in the framework and the production of NTuples scripts is decribed. 
To begin with, there are 2 ways that we access the information for HLT objects.
1. Re-run HLT configuration: This way is the slowest since we need to run the whole reconstruction from `RAW` datasets (for data or `GEN-SIM-RAW` in MC). In this way the full HLT info gets available. This is essential if you want to test something that is not available in the deployed HLT reconstruction. 
It is also the way studies that need full information like JECs and PFHCs need to get the info since there is no full information in later tiers. Only available info later is the trigger object for triggers that fired in the event, and the trigger decisions.  
2. Run over already reconstructed objects samples: This method refers to running on miniAOD. It is much faster and can be used mainly for data already collected to evaluated the trigger performances. Also it is best for studies that do not need every piece of HLT information because usually the `RAW` samples are stored only on Tape after a while and need a tape re-call to access them.

Bellow there are subsections on the 2 ways. For both ways to run on batch jobs submissions one can find general instructions [here](https://github.com/theochatzis/JMETriggerAnalysis/tree/run3_12_4_12_testTrk/NTuplizers/test#readme).

For analyzing the events there are scipts in the `NTupleAnalysis` directory of the framework. A dedicated subsection exists also on this part bellow.

### Re-run HLT
In case you want to re-run HLT there are 2 basic ingredients. First one needs to specify a given HLT configuration. This is created by the `hltGetConfiguration` command. The corresponding commands are provided by STORM group and you can find them [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT). See bellow "Getting the HLT Menu configuration details".

These commands are stored in the `Common/test` directory, since these are common for all functionalities of the framework.
Then in a configuration in `NTuplizers/test` this created configuration file to re-run HLT is used to load the process. Then the `NTuplizers/plugins/JMETriggerNTuple` is used to run over the produced events and get the information in a TTree. 
The configuration files running this analyzer are denoted as `jmeTriggerNTuple_XXX.py`. 

For example:

```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

One thing that is important is that one can also customize the HLT menu that runs on the events. That is done by using "customizer scripts" i.e. python scripts of the form:
```
def customizationFunction(process):
    # do customizations here
    return process
```
these scripts again are usually stored in `Common/python` directory. They can be added directly in the `jmeTriggerNTuple` script or used directly in `hltGetConfiguration` command with option `--customize`.

### Run on MiniAOD
For running on samples `MINIAOD` format one can use the script `jmeTriggerNTuple2023Data_miniAOD_cfg.py`. The script can be tested as follows:
```
cmsRun jmeTriggerNTuple2023Data_miniAOD_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

This script by default applies some selection criteria on using a muon skim i.e. requiring `HLT_IsoMu27` and some offline selection quality criteria. Thus it is recommended to run on a Muon dataset as is. The skim cut a lot the size of the output file.

But can be modified for more general purposes and also include JetMET dataset.

Some basic options that one has to take into account when running on different data periods:
* `globalTag` : here one defines what input tag `process.GlobalTag.globaltag` uses.
* `offlineJecs` : In case the JECs are reapplied offline, this defines the name of the `.db` file that is used. The name should be given without the `.db` in the end, which is assumed by the script. The sqlite files can be found in the [official JERC repository](https://github.com/cms-jet/JECDatabase). One can see how these corrections behave with [this tool](https://cmsjetmettools.web.cern.ch/JECViewer/#Autumn18_V19_MC;AK4PFchs;L1FastJet;Eta;Rho%20=%2040.00,%20PT%20=%20100.00;Hidden=false&Autumn18_V19_MC;AK4PFchs;L2Relative;Eta;Rho%20=%2040.00,%20PT%20=%20100.00;Hidden=false?LogX=false&LogY=true).

Recommended batch submission:
With this batch submissions for different eras can be run using a python script that makes different CRAB jobs:
```
cd NTuplizers/crab/
python3 createCrabConfigFilesMiniAOD.py
```
it will create a script that will submit the jobs and the different crab configs with the specified globalTag, offline JECs files, luminosity JSON.

### Analyzing Events from NTuples
The directory for Analysis of the output NTuples is the `NTupleAnalysis`. You can see a structure with different plugins that are used for analysis, and python scripts that utilize those or provide tools in the `test` directory.

A description of the basic tools and how to use them can be found [here](https://github.com/theochatzis/JMETriggerAnalysis/tree/run3_13_0_X/NTupleAnalysis/test#readme).



----------


### Getting the HLT Menu configuration details

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
This command generates automatically a process `HLTX` that runs the trigger menu.
Options explanation:

- *globalTag* : declares which is the global tag your HLTX process will run. Using auto is preferable cause it will update it from `autoCond.py` in CMSSW release.
- *mc* : this shows if you run on MC or data to get the appropriate menu e.g. one containing the MC paths. These paths are useful as they just generate the objects with no cut in events selection.
- *unprescale* : ignore the prescale table - when we re-run HLT we don't want to lose more events for the studies from PS!
- *output* : shows the event content of the `ROOT` file the `cmsRun` would produce. We do not need this output.
- *max-events* : maximum number of events running
- *input* : name of input ROOT file.
- *eras* : determines the era for geometry etc.
- *--l1-emulator* : needed only if you want to re-emulate L1. You can ignore this if you do not care about L1.
- *--l1* : xml file containing the menu from L1T to re-run.
- *--path* : option is not mandatory, but can help to process the events faster as it only creates a sub-menu with the paths listed. You always need the `Status*`,`HLTriggerFinalPath` as these techincal paths are essential for a trigger menu to run.

We store the menus in `Common/python/configs` directory and use shell scripts to produce them in `Common/test`. For example you can do:
```
./dumpHLTMenus_mcRun3.sh
```
and get the menu produced.


