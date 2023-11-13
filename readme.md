
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

### Setup instructions
To setup the framework you need CMSSW and as such a working LXPLUS account. Currently the recommended LXPLUS version is LXPLUS8, so login as follows:
```
ssh -Y <user_name>@lxplus8.cern.ch
```
then in any directory setup the framework:
```
cmsrel CMSSW_13_0_7_patch1
cd CMSSW_13_0_7_patch1/src
cmsenv

git clone https://github.com/theochatzis/JMETriggerAnalysis.git -b run3_13_0_X

# For PFHC no need this for now. We use the Offline PFHC (tag '' instead of 'HLT')
# PFHC: preliminary HLT-PFHC for Run-3
#cp /afs/cern.ch/user/c/chuh/public/PFCalibration/CMSSW_1300_126X/PFCalibration.db ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/

# Build
scram b -j 12
```

Test command that the setup works:
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

----------

### Tools for JME studies on the Run-3 HLT reconstruction

Here the main structure of the logic in the framework and the production of NTuples scripts is decribed. 
To begin with, there are 2 ways that we access the information for HLT objects.
1. Re-run HLT configuration: This way is the slowest since we need to run the whole reconstruction from `RAW` datasets (for data or `GEN-SIM-RAW` in MC). In this way the full HLT info gets available. This is essential if you want to test something that is not available in the deployed HLT reconstruction. 
It is also the way studies that need full information like JECs and PFHCs need to get the info since there is no full information in later tiers. Only available info later is the trigger object for triggers that fired in the event, and the trigger decisions.  
2. Run over already reconstructed objects samples: This method refers to running on miniAOD. It is much faster and can be used mainly for data already collected to evaluated the trigger performances. Also it is best for studies that do not need every piece of HLT information because usually the `RAW` samples are stored only on Tape after a while and need a tape re-call to access them.

Bellow there are subsections on the 2 ways. For both ways to run on batch jobs submissions one can find general instructions [here](https://github.com/theochatzis/JMETriggerAnalysis/tree/run3_12_4_12_testTrk/NTuplizers/test#readme).

For analyzing the events there are scipts in the `NTupleAnalysis` directory of the framework. A dedicated subsection exists also on this part bellow.

### Re-run HLT
In case you want to re-run HLT there are 2 basic ingredients. First one needs to specify a given HLT configuration. This is created by the `hltGetConfiguration` command. The corresponding commands are provided by STORM group and you can find them [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT).
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

A description of the basic tools can be found [here](https://github.com/theochatzis/JMETriggerAnalysis/tree/run3_13_0_X/NTupleAnalysis/test#readme).

Utilizing those tools usually one can make scripts performing an analysis or a part of it. Some indicative scripts for the different parts are following:

1. Adding the output NTuples:
```
JMETriggerAnalysis/NTupleAnalysis/test/addNTuples_2023Data.sh
```
2. Analyzing the NTuples creating multiple histograms with objects quantities/performances between different matched collections, for selections based on a trigger or any other selection. This contains all the needed information to make a trigger efficiency plot or performance plots.
```
JMETriggerAnalysis/NTupleAnalysis/test/runAnalysis_hltRun3_2023Data.sh
```
3. Plotting scripts. There are plotting scripts for performances like the following:
```
JMETriggerAnalysis/NTupleAnalysis/test/plotVersionCheck.sh
```
or for trigger efficiencies. For example:
```
JMETriggerAnalysis/NTupleAnalysis/test/plotEfficiencies_2023Data.sh
```

