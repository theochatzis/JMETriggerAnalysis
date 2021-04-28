### Tools for JME studies on the Phase-2 HLT reconstruction

* [Setup](#setup)
* [Instructions to generate configuration files for HLT Phase-2 reconstruction](#instructions-to-generate-configuration-files-for-hlt-phase-2-reconstruction)
* [Configuration with JME trigger paths for testing](#configuration-with-jme-trigger-paths-for-testing)
* [Inputs for HLT Jet Energy Scale Corrections workflow](#inputs-for-hlt-jet-energy-scale-corrections-workflow)
* [Additional Notes](#additional-notes)

----------

### Setup

```shell
scramv1 project CMSSW CMSSW_11_1_8
cd CMSSW_11_1_8/src
eval `scramv1 runtime -sh`

git cms-merge-topic cms-sw:32903

# [optional; required only for PF-Hadron calibrations]
# workaround for PFSimParticle::trackerSurfaceMomentum
# ref: hatakeyamak:FBaseSimEvent_ProtectAgainstMissingTrackerSurfaceMomentum
git cms-addpkg FastSimulation/Event
git remote add hatakeyamak https://github.com/hatakeyamak/cmssw.git
git fetch hatakeyamak
git diff 0cf67551731c80dc85130e4b8ec73c8f44d53cb0^ 0cf67551731c80dc85130e4b8ec73c8f44d53cb0 | git apply

# [optional; required only for JME-Trigger NTuple workflow with 'pvdqm > 1']
# analyzer for primary vertices (courtesy of W. Erdmann)
git clone https://github.com/missirol/PVAnalysis.git usercode -o missirol -b phase2

# [optional; required only for JME-Trigger NTuple]
mkdir -p HLTrigger
git clone https://github.com/veelken/mcStitching.git HLTrigger/mcStitching

git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b phase2
scram b -j 10
```
**Note**: when an update to this setup recipe is needed,
update this part of the `readme`, plus the content of the script
[`setup_cmssw.sh`](https://github.com/missirol/JMETriggerAnalysis/tree/phase2/setup_cmssw.sh).

----------

### Instructions to generate configuration files for HLT Phase-2 reconstruction

Configuration files are created via `cmsDriver.py`,
adding (HLT) customisations to the Phase-2 Offline reconstruction;
for an example of a `cmsDriver.py` for the Offline reconstruction (RECO step)
can be found from the setup commands of a AOD/MINIAOD sample in McM
([example](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/TSG-Phase2HLTTDRWinter20RECOMiniAOD-00010)).

 * Customisation functions are available under
   [`Common/python/`](https://github.com/missirol/JMETriggerAnalysis/tree/phase2/Common/python):

   - [**L1T**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_L1T.py#L4):
     customisation to add the L1-Trigger reconstruction as implemented in the recipe provided in the
     [``Phase-2 HLT'' TWiki](https://twiki.cern.ch/twiki/bin/view/CMS/HighLevelTriggerPhase2?rev=69#Running_and_using_the_L1T_result).

   - [**TRKv00**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_TRKv00.py#L3),
     [**TRKv02**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_TRKv02.py#L3),
     [**TRKv06**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_TRKv06.py#L3):
     customisations extracted from standalone configs developed by the TRK POG;
     guidelines to create such a customisation function
     from a standalone `trackingOnly` configuration can be found in
     [Common/test/makeTRKCustomisationFunction.md](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/test/makeTRKCustomizationFunction.md).

   - [**''skimmed tracks''**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_skimmedTracks.py#L3):
     an addon to the standard TRK sequence,
     to select a subset of tracks based on their compatibility
     with the sumPt2-leading pixel vertices.
     If using one of the TRK customisation functions,
     apply the ''skimmed tracks'' customisation only after the TRK customisation function;
     this function can be applied after any of TRK customisation functions.

   - [**PF**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_PF.py#L13):
     customisations for the standard Particle-Flow sequence (collection: `particleFlowTmp`)
     following the approach used for PF@HLT in Run-2.

   - [**JME**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/hltPhase2_JME.py#L13):
     customisations to build HLT Jets and MET collections.

   - [**Paths and Schedule**](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/customizeHLTForPhase2.py):
     wrapper functions that combine the customisations described above for individual objects (e.g. tracks, PF, jets);
     see the source code for more details, and for the full set of available customisations.

 * A set of configuration files for different TRK (v0, v2, v6, v6.1, v7.2) and HGCal (with, or without, TICL) inputs can be found in
   [Common/python/configs/hltPhase2_*_cfg.py](https://github.com/missirol/JMETriggerAnalysis/tree/phase2/Common/python/configs).

 * **Example**: configuration file to run HLT reconstruction on RAW using TRK(v06p1)+TICL:
   ```shell
   cmsDriver.py step3 \
     --geometry Extended2026D49 --era Phase2C9 \
     --conditions 111X_mcRun4_realistic_T15_v4 \
     --processName RECO2 \
     --step RAW2DIGI,RECO \
     --eventcontent RECO \
     --datatier RECO \
     --filein /store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/FEVT/PU200_castor_111X_mcRun4_realistic_T15_v1-v1/100000/DA18C0FC-1189-D64B-B3B6-44F3F96F1840.root \
     --mc \
     --nThreads 4 \
     --nStreams 4 \
     --no_exec \
     -n 10 \
     --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
     --customise JMETriggerAnalysis/Common/customizeHLTForPhase2.customise_hltPhase2_scheduleJMETriggers_TRKv06p1_TICL \
     --customise_commands 'process.prune()\n' \
     --python_filename hltPhase2_TRKv06p1_TICL_cfg.py
   ```

----------

### Inputs for HLT Jet Energy Scale Corrections workflow

A standalone configuration file to create inputs
for the HLT Jet Energy Scale Corrections (JESC) derivation
can be found under
[Common/python/configs/hltPhase2_rawJets_cfg.py](https://github.com/missirol/JMETriggerAnalysis/blob/phase2/Common/python/configs/hltPhase2_rawJets_cfg.py).

  * The configuration file loads the latest baseline reconstruction sequence
    (usually, as defined in one of the files in
    [Common/python/configs/hltPhase2_*_cfg.py](https://github.com/missirol/JMETriggerAnalysis/tree/phase2/Common/python/configs)

  * It runs on RAW (without 2-file solution),
    and creates an EDM file that contains
    only the products needed for
    the HLT-JESCs derivation
    (e.g. uncorrected jets).

  * **Example**: outputs can be produced as follows
    (parts in parentheses denote some of the optional command-line parameters).
    ```
    cmsRun hltPhase2_rawJets_cfg.py [inputFiles=file:raw.root] [output=out.root] [globalTag=TheGT] [maxEvents=1]
    ```

----------

### Additional Notes

 * [HLT Phase-2 TWiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HighLevelTriggerPhase2)

 * DAS query for the latest Phase-2 MC samples (RAW):
   ```shell
   dasgoclient --query="dataset dataset=/*/Phase2HLTTDR*ReRECO*111X*/*"
   ```

----------
