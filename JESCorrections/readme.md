This directory contains tools and instructions
to derive Jet Energy Scale Corrections
for the jets used in the High-Level Trigger (HLT).

#### Setup

Instructions to set up the CMSSW area to produce JRA NTuples, and derive JESCs:
```
cmsrel CMSSW_12_3_0_pre4
cd CMSSW_12_3_0_pre4/src
cmsenv
git clone git@github.com:sparedes/JMETriggerAnalysis.git -o sparedes -b run3_12_3_X
git clone git@github.com:sparedes/JetMETAnalysis.git -o sparedes -b dev_run3

# PFHC: preliminary HLT-PFHC for Run-3
cp /afs/cern.ch/work/p/pdas/public/run3/PFHC_Run3Winter21_HLT_V3.db JMETriggerAnalysis/NTuplizers/test/

scram b -j 12
```

#### Produce JRA NTuples with HLT Jets
First test your setup locally: 
```bash
# First make your way to the 'test' directory
cd JMETriggerAnalysis/JESCorrections/test/
cmsRun jescJRA_cfg.py  maxEvents=1000  output=test_jra_step.root 
```
Note: You might want to double check that what is set in the `jescJRA_cfg.py`, such as the `.root` file matches the sample you want to use, or that the `.db` file of the PFHCs is up-to-date.  

If the test runs sucessfuly, you can then inspect the output root file `test_jra_step.root`  and make sure the contents are as expected.

Once all looks good you can submit your crab jobs. 
```bash
crab submit -c crab/my_crab_submission_file.py
```
Note: You might need to change the line where the `.db` file of the PFHCs is picked up so that CRAB can find the file. 

Once the crab jobs are finished, the output `.root` files can be found in the Tier2 (T2) specified in the configuration file,
and then transferred over to `eos` for the next steps.

**Note** that in order to run the ntuple-making process on CRAB, there needs to be a copy of them on **a** T2. You can request to transfer them to your local T2 by requesting it through `rucio` (find more info in the [CMS Rucio Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/Rucio)):
```bash
rucio add-rule cms:/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/GEN-SIM-RAW  1 T2_BE_IIHE --asynchronous  --ask-approval --lifetime 5184000
```
replacing the necessary dataset name, T2 name, lifetime, etc. 

#### Derive Jet Energy Scale Corrections from JRA NTuples

Once JRA NTuples have been produced,
JESCs can be derived from them by running
the executables of the `JetMETAnalysis` package.

An example of how to do this is given below:
```
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/
./fitJESCs -o output_tmp1 -n -1
```
The `fitJESCs` script is an example of
a wrapper executing the various steps of the JESCs derivation
(caveat: the script presently includes several hard-coded parameters).

##### Run on HTCondor
The `-b` and `-j` flags can be used to run one HTCondor job for each jet collection's correction (see the submission script `test/sub_jecs.htc` for an example). 

##### Sample information
The necessary samples are large QCD simulated datasets with a flat p<sub>T</sub> over a large range.
The `L1` correction needs to match jets from samples generated with and without pileup, so we will need to produce two JRANtuples. 
The samples used for the latest run 3 preliminary JECs are the following:
```
# FlatPU
/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/GEN-SIM-RAW
# NoPU
QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-NoPU_110X_mcRun3_2021_realistic_v6_ext1-v1/GEN-SIM-RAW
```
You can find them in DAS searching for:
```
dataset=/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-*0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/GEN-SIM-RAW
```
You can also find similar samples doing something like:
```
dataset=/QCD*_Pt*/*/GEN-SIM*RAW
```

##### List of Run-3 HLT JESCs:

  * `Run3Winter21_V2_MC`:

    - Description: preliminary HLT JESCs for Run-3 studies

    - Tag of `sparedes/JMETriggerAnalysis`: `HLT_JESCs_Run3Winter21_V2`

    - Tag of `sparedes/JetMETAnalysis`: `Run3Winter21_V2`

    - JRA NTuples:
      ```
      root://cms-xrd-global.cern.ch//store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/jescs_dec_PFHC_E2to500_noPU.root
      root://cms-xrd-global.cern.ch//store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/jecs_dec_PFHC_E2to500_flatPU.root      
      ```

    - executable for JESCs fits (contains settings of all JESCs fits):
      [`JESCorrections/test/fitJESCs`](https://github.com/sparedes/JMETriggerAnalysis/blob/HLT_JESCs_Run3Winter21_V2/JESCorrections/test/fitJESCs)

      
  * `Run3Winter20_V2_MC`:

    - Description: preliminary HLT JESCs for Run-3 studies

    - Tag of `JMETriggerAnalysis`: `hltJESCs_Run3Winter20_V2_MC`

    - Tag of `missirol/JetMETAnalysis`: `Run3Winter20_V2_MC`

    - JRA NTuples:
      ```
      root://cms-xrd-global.cern.ch//eos/cms/store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/npv_fix_noPU/npvFix_noPU.root
      root://cms-xrd-global.cern.ch//eos/cms/store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/npv_fix_flatPU/npvFix_flatPU.root
      ```

    - executable for JESCs fits (contains settings of all JESCs fits):
      [`JESCorrections/test/fitJESCs`](https://github.com/missirol/JMETriggerAnalysis/blob/hltJESCs_Run3Winter20_V2_MC/JESCorrections/test/fitJESCs)

    - Notes:

      - JRA NTuples affected by a bug in the `rho` value saved for Calo and PFCluster (AK4 and AK8) HLT jets:
        the `rho` based on PF-candidates was erronously used,
        instead of the `rho` values calculated from calo-towers and PFClusters, respectively.
        
      
