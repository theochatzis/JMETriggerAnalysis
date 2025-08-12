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
* NanoAnalysis

For the last two there is available documentation in the subdirectories. (Note: need instructions for PFHC - to be added)

----------
----------

**Note**: for instructions on HLT PF-Hadron calibrations and Jet Energy Scale Corrections,
please ignore this `readme`, and follow the instructions in the dedicated `readme` files:
- [JECs instructions](https://github.com/theochatzis/JMETriggerAnalysis/tree/master/JESCorrections/readme.md)
- [PFHCs instructions](https://github.com/theochatzis/JMETriggerAnalysis/blob/master/PFHadronCalibration/readme.md)

----------
----------

### Setup instructions

To setup the framework you need CMSSW and as such a working LXPLUS account. Currently the recommended LXPLUS version is LXPLUS8, so login as follows:
```
ssh -Y <user_name>@lxplus8.cern.ch
```
then in any directory setup the framework:
```
cmsrel CMSSW_15_0_11
cd CMSSW_15_0_11/src
cmsenv
git cms-init
## --- You can find bellow useful additions to standard CMSSW for relevant studies ---
# Needed: Merge updates from tracking for 2025 - CA automation for patatrack params + mkFit for track building
git cms-merge-topic elusian:1501_newCAtuning 

## -----------------------------------------------------------------------------------

git clone git@github.com:theochatzis/JMETriggerAnalysis.git

## Additional studies
## Only use those in case you want to perform such a study. 
# Optional: Use this merge-topic in case you want to study removal of low pT jets in MHT
git cms-merge-topic theochatzis:testMHTforFwd

# Optional: Used for PUPPI studies
git cms-merge-topic theochatzis:puppiRun3Customizer_15_0_X
 

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
### Performing a trigger analysis 
#### Step 1: The input
Here the main structure of the logic in the framework and the production of NTuples scripts is decribed. The basic input we use are the `JMETriggerNTuples`. These can be created in two ways:
1. **Re-Run HLT configuration (RAW):** This way is the slowest since we need to run the whole reconstruction from `RAW` datasets (for data or `GEN-SIM-RAW` in MC). In this way the full HLT info gets available. This is essential if you want to test something that is not available in the deployed HLT reconstruction. 
It is also the way studies that need full information like JECs and PFHCs need to get the info since there is no full information in later tiers. Only available info later is the trigger object for triggers that fired in the event, and the trigger decisions.  
2. **Run on already reco samples (MINIAOD):** This method refers to running on miniAOD. It is much faster and can be used mainly for data already collected to evaluated the trigger performances. Also it is best for studies that do not need every piece of HLT information because usually the `RAW` samples are stored only on Tape after a while and need a tape re-call to access them.

For both ways we run configuration files with the naming `jmeTriggerNTuple*`. 

Bellow there are subsections on the 2 ways. For both ways to run on batch jobs submissions one can find general instructions [here](https://github.com/theochatzis/JMETriggerAnalysis/tree/master/NTuplizers/test#readme).

For analyzing the events there are scipts in the `NTupleAnalysis` directory of the framework. A dedicated subsection exists also on this part.

##### Re-run HLT from RAW
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

**Batch submission** For submitting jobs re-running the HLT CRAB and HTC Condor scripts are supported. CRAB is most recommended for the studies. 
- *CRAB* : The basic example script for batch submission with crab is stored in `NTuplizers/test/crab/multicrab_reHLT.py`. You can find a basic description of this file [here](https://github.com/theochatzis/JMETriggerAnalysis/tree/master/NTuplizers/test#multicrab-when-re-running-hlt).
- *HTC Condor* : Alternatively there is the support of condor submission. You can find example scripts running on condor in `JMETriggerAnalysis/NTuplizers/scripts` and [documentation](https://github.com/theochatzis/JMETriggerAnalysis/tree/master/NTuplizers/test#htc-condor) explaining how these work.

##### Run on MiniAOD 
For running on samples `MINIAOD` format one can use the script `jmeTriggerNTuple_miniAOD_cfg.py`. The script can be tested as follows:
```
cmsRun jmeTriggerNTuple2023Data_miniAOD_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root

```

This script by default applies some selection criteria on using a muon skim i.e. requiring `HLT_IsoMu27` and some offline selection quality criteria. Thus it is recommended to run on a Muon dataset as is. The skim cut a lot the size of the output file.

But can be modified for more general purposes and also include JetMET dataset.

Some basic options that one has to take into account when running on different data periods:
* `globalTag` : here one defines what input tag `process.GlobalTag.globaltag` uses.
* `offlineJecs` : In case the JECs are reapplied offline, this defines the name of the `.db` file that is used. The name should be given without the `.db` in the end, which is assumed by the script. The sqlite files can be found in the [official JERC repository](https://github.com/cms-jet/JECDatabase). One can see how these corrections behave with [this tool](https://cmsjetmettools.web.cern.ch/JECViewer/#Autumn18_V19_MC;AK4PFchs;L1FastJet;Eta;Rho%20=%2040.00,%20PT%20=%20100.00;Hidden=false&Autumn18_V19_MC;AK4PFchs;L2Relative;Eta;Rho%20=%2040.00,%20PT%20=%20100.00;Hidden=false?LogX=false&LogY=true). The offline JECs are stored from the database in the `NTuplizers/test/jecsDBFile` area.

**Batch submission**
With this batch submissions for different eras can be run using a python script that makes different CRAB jobs:
```
cd NTuplizers/test/crab
./crab/multicrab.py [configuration file] -i [regular expression]
```
this tool will submit the jobs and the different crab configs with the specified
- `dataset`
- `globalTag`
- `offline JECs files`
- `luminosity JSON` 

which are defined in `createCrabConfigFilesMiniAOD.py`. More detailed documentation [here](https://github.com/theochatzis/JMETriggerAnalysis/tree/master/NTuplizers/test#multicrab-for-miniaodnanoaod-analysis).

#### Step 2: Analyzing the JMETrigger NTuples
The directory for Analysis of the output JME Trigger NTuples is the `NTupleAnalysis`. You can see a structure with different plugins that are used for analysis, and python scripts that utilize those or provide tools in the `test` directory.

A description of the basic tools and how to use them can be found [here](https://github.com/theochatzis/JMETriggerAnalysis/tree/master/NTupleAnalysis/test#readme).

The core steps of the analysis process are described first here, and below you can find three basic use cases examples of using the code.

**Tree -> Histograms production**: 

The first step is making histograms from the `Events` TTree of the NTuples as input. There are cpp based plugins that are analyzing this structure of events branches in `NTupleAnalysis/src/`, the ones used is `JMETriggerAnalysisDriverRun3`. To use an analyzer in a configurable way we have python script `run.py` which feeds the settings of the analyzer with a `driver configuration YAML file`. Examples of such YAML files exist in `NTupleAnalysis/test/analysisDriver_configurations`.

You can see bellow one example:

```yaml
# determines which from the available detector jet regions categories on eta,phi, pt etc will be used. These are defined in JMETriggerAnalysisDriverRun3::jetBelongsToCategory(...) function in NTupleAnalysis/src/JMETriggerAnalysisDriverRun3.cc
jetCategoryLabels:
  - _HB
  - _HE1
  - _HE2
  - _HF
# determines which from the available run periods to be used. These are defined in JMETriggerAnalysisDriverRun3::runPeriod(...) function in NTupleAnalysis/src/JMETriggerAnalysisDriverRun3.cc
runPeriods: []
# with this provides very minimal output for efficiencies calculations only. It will contain only offline quantities in the output directories with minimal info, needed for efficiencies.
lightVersion: true 
# this will skip the NoSelection category. In case of MC can be set to False to provide denominators for efficiencies/unbiased selections for performances.
useOnlyTriggers: true
# this will use only run periods definitions for categories selection. For MC should be deactivated.
useOnlyRunPeriods: false

# Booleans paths to be used in the analysis for defining regions. Make sure both your numerator and denominators are here for efficiencies calculations.
jettriggers:
  - HLT_PFJet60
  - HLT_PFJet500

httriggers:
  - HLT_PFHT1050

mettriggers: # []
  - HLT_PFMET120_PFMHT120_IDTight
```

To run this plugin a condor submission script is used, that will process your input directory files simultaneously. To use this you can run `runAnalysis_hltRun3_submitter.sh` as follows:

```bash
./runAnalysis_hltRun3_submitter.sh [--base-dir DIR] [--out-eos-dir DIR] [--jobs-dir-name NAME] [--driver-config PLUGIN_CONFIGURATION_YAML_FILE] [--data-keys key1,key2,...]

# Example case
./runAnalysis_hltRun3_submitter.sh --base-dir /eos/user/t/tchatzis/JetTriggerInput/ \
  --out-eos-dir OutputSubmitter \
  --jobs-dir-name OutputSubmitter \
  --driver-config efficiencies_miniaod \
  --data-keys JetMET0_Run2024DV1,JetMET0_Run2024FV1
```

Options description:

- `base-dir`: Base dir. Could be on EOS or anywhere.
- `out-eos-dir`: Output is stored in an EOS dir.
- `jobs-dir-name`: Name of condor submissions jobs directory. This is appearing locally.
- `driver-config`: Name of file to use for plugin configuration. See analysisDriver_configurations directory for such configs examples.
- `data-keys`: Comma seperated list of keys of data sub-directories to be used. If none is given will just take everything inside the BASE_DIR.

After you run this you should see many jobs submitting. You can control the number of events per job and condor max runtime etc by adjusting the options of `batch_driver` in the script.

**What is the output?**
Good question!

The output should contain histograms splitted in folders which correspond to different selection categories. As examples `NoSelection` which as the name states, has nothing as requirement or `HLT_PFJet500` which states the trigger HLT_PFJet500 passes for those events.

In each of these folders histograms exist with a "standard structure":
```
[Object Collection name]_[selection category]_[quantity(ies)]
```
#examples:
offlineAK4PFPuppiJetsCorrected_HB_pt0 # -> this means the Offline Puppi leading jet pt (pt0) of jets selected in Barrel (HB).

offlineAK4PFPuppiJetsCorrected_MatchedToGEN_HB_pt0 # -> the same but only matched to generated jets are selected.
```
Histograms exist both in 1D and 2D maps e.g. for making response vs reference pT etc. Those histograms encode all the info needed to make analysis plots.

**Adding/Merging output and/or Harvesting**: 
After having produced the basic histogams with the analysis driver one can jump directly into making plots already.

For this purpose there is an additional script with the functionality:
- first adding the different outputs, using ROOT's `hadd`. 
- second harvesting the output and coverting it into a new ouput file. Harvesting step is copying histograms existing and in addition creating TGraph objects with Efficiencies/Responses etc where it applies. 

In practice this is done by the `runAnalysis_hltRun3_harvester.sh` script. 

```bash
./runAnalysis_hltRun3_harvester.sh [--skip-harvest] [--out-dir DIR] [--output-file NAME]

# example:
./runAnalysis_hltRun3_harvester.sh --out-dir OutputSubmitter --output-file merged_ouput
```

Options description:

- `skip-harvest`: Skip the harvesting step. This step is needed only if you want to make Graphs of efficiency, response etc. If histos is all you need can skip it.

- `out-dir`: This is the directory that you will use as base for your output.

- `output-file`: This is the ouput file name 


Note: There is also `runAnalysis_hltRun3_harvester_batch.sh` which supports adding the histograms in batches. This is something that can be used in case your adding gets too slow.

```bash
./runAnalysis_hltRun3_harvester_batch.sh [--skip-harvest] [--out-dir DIR] [--output-file NAME] [--batch-size NUMBER OF FILES PER BATCH FOR HADD]
```

Then by using available plotting scripts or writing your own you can create any plot you wish :).

##### Use Case: Making Efficiencies from MiniAOD (DPNote Style)

For this we need two steps. 

First making the histograms with the analysis driver:
```bash
./runAnalysis_hltRun3_submitter.sh /eos/user/t/tchatzis/JetTriggers_DPNote/ DPNoteSubmitter DPNoteSubmitter efficiencies_miniaod
```
this will submit the jobs for histograms creation. After these are done one can plot directly the efficiencies. 
For DPNote style can use the `plotEfficienciesDPNote.py`. This script merges the output first on its own and then can make all the trigger efficiencies for different categories of events.

```bash
python3 plotEfficienciesDPNote.py \
  --input [input directory with subdirs containing ROOT files with histograms] \
  --merged_file [merged histograms ouput file - if it exists already will be just re-used as input not produced] \
  --config [configuration YAML file which is taken from plotsEfficiencies_configs - defining axes, triggers to be used etc] \
  --output_dir [output directory where plots will be saved in a structured way]
```

An example use is in `dpnote_efficiencies.sh`:
```bash
python3 plotEfficienciesDPNote.py \
  --input /eos/user/t/tchatzis/DPNoteSubmitter/ \
  --merged_file /eos/user/t/tchatzis/DPNoteSubmitter/merged.root \
  --config ./plotsEfficiencies_configs/dpnote_config.yaml \
  --output_dir /eos/user/t/tchatzis/DPNotePlots
```

##### Use Case: Making Efficiencies from RAW

First making the histograms with the analysis driver:

```bash
./runAnalysis_hltRun3_submitter.sh /eos/user/t/tchatzis/JetTriggers_RawNTuples/ RawEfficienciesSubmitter RawEfficienciesSubmitter efficiencies_raw
```

then add the histograms (if you want can skip the harvesting step with `--skip-harvest` to be faster...):

```bash
./runAnalysis_hltRun3_harvester.sh --out-dir OutputSubmitter --output-file merged_ouput --skip-harvest
```

Then from the `merged_ouput.root` file you can plot efficiencies. For examples scripts check
```
# In these scripts the names of triggers etc need to be adjusted inside, not configurable yet (TO-DO).
# Data efficiencies
bash plotEfficiencies_Data.sh
# MC efficiencies
bash plotEfficiencies_MC.sh
```

##### Use Case : Performances plots (only from RAW)

First making the histograms with the analysis driver:

```bash
./runAnalysis_hltRun3_submitter.sh /eos/user/t/tchatzis/JetTriggers_RawNTuples/ RawPerformancesSubmitter RawPerformancesSubmitter performances_raw
```

then add the histograms (if you want can skip the harvesting step with `--skip-harvest` to be faster...):

```bash
./runAnalysis_hltRun3_harvester.sh --out-dir OutputSubmitter --output-file merged_ouput
```

Then from the harvested output one can use the following script. 
```
# Example script for run performances
bash plotPerformances_config.sh
```
the basic script that is used is `jmePlots.py` which for example runs as:
```bash
jmePlots.py -k [key for selected plots - check file for key selection]  \
-o [output directory to save plots] \
-i [harvesting file 1]:'Reco Option 1':632:1:20 \ # inputs with adjusted colors:marker size:marker style etc.
   [harvesting file 2]:'Reco Option 2':800:1:20 \
   [...]
-l [label e.g. '#font[61]{CMS} #font[52]{Run-3 Simulation}']
```

Note that this script supports using multiple harvested outputs for comparisons. This is something one typically wants. In this case need to run separately for each case the harvester step to make a harvesting ROOT file.

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


