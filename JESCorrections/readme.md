This directory contains tools and instructions
to derive Jet Energy Scale Corrections
for the jets used in the High-Level Trigger (HLT).

#### Setup

Instructions to set up the CMSSW area to produce JRA NTuples, and derive JESCs:
```
cmsrel CMSSW_14_0_14
cd CMSSW_14_0_14/src
cmsenv
git cms-init

# Was used to test skipping forward PFHC corrections application.  
#git cms-merge-topic theochatzis:optionForSkipForwardPFHC

# In case you want to study the new CaloTowers update
git cms-addpkg RecoLocalCalo/CaloTowersCreator
git cherry-pick 979e2299d39a803bcdfec5b20ad083e67f7a30dc

git clone https://github.com/theochatzis/JetMETAnalysis.git -b hlt_run3
git clone https://github.com/theochatzis/JMETriggerAnalysis.git -b run3_14_0_X
scram b -j 8
```

Make sure the menu is updated (see section on main page `readme.md`: Getting the HLT Menu configuration).
Do:
```
cd ${CMSSW_BASE}/JMETriggerAnalysis/Common/test
./dumpHLTMenus_mcRun3.sh
```

Note: 
Currently working on `LXPLUS8` so use:
```
ssh -Y user@lxplus8.cern.ch
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
You need generally 2 submissions:
- one for `QCD with noPU` (or equivalently Epsilon PU) sample,
- and one for a `flatPT spectrum QCD` (so there isn't a bias in the pT for the corrections derivation).
The noPU sample is used for the L1 Offset correction. If you intend to only derive corrections for PUPPI, and you don't think you need this type of corrections, you may ommit this file production.
Examples for crab submission scripts are:
```bash
#example for noPU crab script
crab/sub_noPU.py
#example for flatPT crab script
crab/sub_flatPU.py 
```
Note: You might need to change the line where the `.db` file of the PFHCs is picked up so that CRAB can find the file. 

Once the crab jobs are finished, the output `.root` files can be found in the Tier2 (T2) specified in the configuration file,
and then transferred over to `eos` for the next steps. 

The output files need to be merged using `hadd` into one single file for the next steps to work.

#### Derive Jet Energy Scale Corrections from JRA NTuples

Once JRA NTuples have been produced,
JESCs can be derived from them by running
the executables of the `JetMETAnalysis` package. 
The `fitJESCs` script is an example of
a wrapper executing the various steps of the JESCs derivation.
The `fitJESCs` script is an example of
a wrapper executing the various steps of the JESCs derivation. 
(caveat: the script presently includes several hard-coded parameters).
Some basic options are:
`-o`: output directory \
`-n`: number of events to run \
`--skip-L1-PFPuppi`: in case you want to skip the L1 step for PUPPI \
`-j`: execute only for one type of collection e.g. `ak4pfHLT` \
`-b`: for batch mode 

You need to define the `JRA NTuples` at the beginning of the script.
Note that the NTuples need to be single files, so you should have added the files from the CRAB jobs.

The corrections usually take some time, so best is to run condor jobs. The `-b` and `-j` flags can be used to run one HTCondor job for each jet collection's correction (see the submission script `test/sub_jecs.htc` for an example). 
```
condor_submit sub_jecs.htc
```

A local example of running the whole procedure is the following:

```
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/
./fitJESCs -o output_dir -n -1
```



##### Run on HTCondor


##### Sample information
The necessary samples are large QCD simulated datasets with a flat p<sub>T</sub> over a large range.
The `L1` correction needs to match jets from samples generated with and without pileup, so we will need to produce two JRANtuples. 
The samples used for the latest run 3 preliminary JECs are the following:
```
# FlatPU
/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter24Digi-FlatPU0to120_133X_mcRun3_2024_realistic_v9-v3/GEN-SIM-RAW

# NoPU
/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter24Digi-NoPU_133X_mcRun3_2024_realistic_v9-v3/GEN-SIM-RAW
```
You can find them in DAS searching for:
```
dasgoclient -query="/QCD*15to7000*/Run3Winter24*/*RAW*"
```
##### Create the `db` files
To create the `.db` files for providing them to AlCa contact for upload in `confDB`(or load them locally in a configuration) you can use the `jescTxtToDBConverter_cfg.py` script, as follows:
```bash
## In this example the output_dir is the directory defined in -o option for fitJECs in previous step.

# make a directory to save the db file. 
mkdir ./output_dir/DBfile

# run the jescTxtToDBConverter tool. 
# as input it needs the .txt files in the jesc directory. It outputs an executable that will make the db file.
python3 jescTxtToDBConverter_cfg.py input=${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/output_dir/ak4pf/jesc/ output=./output_dir/DBfile dumpPython=make_db_file_tmp.py

# run the executable
cmsRun make_db_file_tmp.py 

# after the procedure is done this isn't needed, you can remove it
rm make_db_file_tmp.py
``` 
##### Reading the tags of the `.db` files
If you want to check the tags registered to the `.db` files you can use the following command:
```bash
## check the db file
conddb --db ./output_dir/DBfile/Run3Winter23_MC.db search JetCorr
```
where here the `search` option is for identifying the desired tag. `JetCorr` is a good example cause usually those start like `JetCorrection...`
##### For BPix issue treatment (Updated)
For the BPix area one has to split the corrections based on the eta *and phi*. The procedure currently done is to define for separate phi cases the eta pT rho ... corrections (L1FastJet and L2Relative). To do so there are 2 steps. One is creating the JRA Ntuples separately for the regions of interest e.g. `NoBPix` are jets not affected from the BPix issue. 
For Calo jets nothing changes since these are not affected by this. 
1. **JRA Files** : One has to produce types of JRA files, depending on how much the PF jets are affected by BPIX. These can be given by the option `bpixMode`. 
For example if we want to keep only BPix jets:
```
cmsRun jescJRA_cfg.py  maxEvents=100  output=test_jra_step.root bpixMode=BPix
```
supported options are: 
"noBPix": jets are far enough from BPix in phi. (the jet axis is more than half a radius away)
"BPix": jet axis falls inside the BPix region.
"BPixPlus" : jet axis falls less than half a radius from BPIX region, from the "positive phi" side.
 "BPixMinus" : jet axis falls less than half a radius from BPIX region, from the "positive phi" side.

To do batch submissions for producing the JRA NTuples you can use the `./crab/multicrab_bpix.py`. This can be done as follows : 
First make sure there exists the directory `/eos/user/t/[username]/JRA_NTuples_Winter24`. If it doesn't or you prefer to use another script you can change the `JRA_NTuples_Winter24` part, although note that will be needed to change in next steps. 
Then execute the multi-CRAB command:
```
python3 multicrab_bpix.py
```
this should automatically create all the jobs you need.

After the jobs have ended you need to add the output ntuples. For this one can use :
```
./merge_root_files.sh 
```
where again if you have changed the output dir of the crab jobs you need to modify the input files directory.


2. **Corrections derivation** :
After the JRA NTuples are ready you can make the submission script for condor that will push the jobs to derive different corrections for each case. This is done by `make_condor_scripts_bpix.py`, which makes a single HTC Condor configuration file (`sub_jecs_total_forBPix.htc`) that can submit all the possible cases jobs. 
You can inspect it and for example make sure that the `CaloJets` are produced only in the `noBPix` case.

To use this script do:
```
python3 make_condor_scripts_bpix.py 
condor_submit sub_jecs_total_forBPix.htc
```
You should see that the jobs are submitted.

Again the only assumption is that you have used `/eos/user/t/[username]/JRA_NTuples_Winter24` as directory.

3. **Corrections merging** : In the end we want a single `.db` file where the .txts for all categories (BPix, NoBpix etc.) are merged into one, and there is a separate treatment for the affected eta-phi region. To achieve this one can use the `createTxtFilesBPix` as:
```
./createTxtFilesBPix 
``` 
This file is consistent with the previous steps naming, and should produce a directory `corrections_2024` where inside it has the `.txt` files and a sqlit file `DBfile/Run3Winter24Digi.db`. The conddb command is used to verify this file was created successfuly. 

The assumption in the above file is the condor jobs output directories from the previous step.


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

      - JRA NTuples affected by a bug in the `rho` value saved for Calo and PFCluster (AK4 and AK8) HLT jets:
        the `rho` based on PF-candidates was erronously used,
        instead of the `rho` values calculated from calo-towers and PFClusters, respectively.
