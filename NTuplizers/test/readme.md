### Production of NTuples
## The NTuplizer
The basic configuration file for producing the NTuples is the `jmeTriggerNTuple_cfg.py`. In this file we re-run the HLT configuration and then collect results for Trigger paths and HLT Objects collections to analyze the triggers and the objects performances.

You can try to run this script locally to produce an NTuple named `out_HLT_Run3TRK.root`: 
```
cmsRun jmeTriggerNTuple_cfg.py maxEvents=10 output=out_HLT_Run3TRK.root
```
Options definitions:
* `maxEvents`  maximum number of events 
* `output`  name of output file 

**Note:** For seeing exactly the full configuration file the `cmsRun` command runs above you can use the dumpPython option. For example you can get the `test_config.py` with:
```
python3 jmeTriggerNTuple_cfg.py dumpPython=test_config.py
```

## Running batch jobs
The above configuration file can be used in a batch system to produce large size samples. The used in this setup are with CRAB or HTC Condor. You can find some instructions for both of them bellow.

# CRAB
## Intro
For CRAB you can find some configuration scripts used in the `JMETriggerAnalysis/NTuplizers/test/crab` folder.
One example of a submission to CRAB:
```
crab submit -c crab3_test.py
```
one can change the outputfiles location from options:
`config.Site.storageSite` for the Site and `config.Data.outLFNDirBase` for the output directory path. 

The framework supports multiple submissions in `CRAB` with Multicrab. See the next subsection.
## Multicrab (when re-running HLT)
There is an executable that allows to use the config file that re-runs HLT `multicrab_reHLT.py`. E.g. the `jmeTriggerNTuple2023Data_cfg.py`
You can change the following parameters in the script according to your study:
- `job_name` : this is just the name of the output crab job   
- `primary_dataset`, `secondary_dataset` : define the primary and secondary dataset you use, this should be a MINIAOD and a RAW in order to have both offline PAT collections and the raw info to re-reco HLT. If you need no PAT/Offline quantities you could just use the primary dataset with `RAW`. E.g. a use case is a MC where you want only the `GEN-SIM-RAW` to use the generated quantities.    
- `recoOptions` : these are the options supported in `jmeTriggerNTuple2023Data_cfg.py` that you want to use
- `recoOptionsPFHCs` : dictionary providing a PFHCs file per separate crab job
- `recoOptionsJECs` : dictionary providing a JECs file per separate crab job
Then you can just run the executable by:
```
multicrab_reHLT.py
```
you should be able to see the submission in CRAB for the different reconstructions.

## Multicrab (for MiniAOD/NanoAOD analysis)

**Usage**:\
`multicrab.py <pset> [options]`\
Datasamples defined in crab/createCrabConfigFilesMiniAOD.py

**Example**:

`cd CMSSW_X_Y_Z/src/JMETriggerAnalysis/NTuplizers/test` \
`cmsenv`\
`source /cvmfs/cms.cern.ch/crab3/crab.(c)sh`\
`voms-proxy-init -voms cms` \
`crab/multicrab.py jmeTriggerNTuple2023Data_miniAOD_cfg.py -i 2024`\
\
\
`crab/multicrab.py -l -i 'Muon\S+2024'`

**Help**:

`crab/multicrab.py -h`

multicrab.py &lt;pset&gt; [-options]\
multicrab.py --status [&lt;dir&gt;]\
multicrab.py --resubmit [&lt;dir&gt;]

| Options ||
| --- | --- |
|-h, --help   | Show this help message and exit |
|--status     | Flag to check the status of CRAB jobs  |
|--resubmit   | Flag to resubmit CRAB jobs |
|-i, --include| Regexp for including tasks. Only perform action for this dataset(s) [default: ""] |
|-e, --exclude| Regexp for excluding tasks. Exclude this dataset(s) from action [default: ""] |
|-d, --dir    | Use existing multicrab [default: ""] |
|-l, --list   | List datasets and exit  |


*If you need to resubmit dataset X*:
 - go to the multicrab dir
 - rm the problem dataset
 - cd ..
 - multicrab.py &lt;pset&gt; -d &lt;the-multicrab-dir&gt;


The script will submit only those datasets which are missing (=the one just removed)


# HTC Condor
For HTC Condor there are 2 python scripts that are used, located in `JMETriggerAnalysis/NTuplizers/scripts`.
* `bdriver.py`: this script creates condor configuration files, each containing a different subset of events, and the corresponding executables (`.sh` scripts) that these use. It can also submit the jobs right after the configuration files creation using the `--submit` option. 
For the creation of the executables it needs a config file as input, which we produce via the `dumpPython` option mentioned above.
* `bmonitor.py`: this script can be used to monitor and submit scripts created by bdriver. 
To run these scripts one can use an executable shell scripts like the ones located in `JMETriggerAnalysis/NTuplizers/test/scripts`. An example of such a script is:
```
./makeNTuples_run3_latest.sh
```
for the output dir you can change the `OUTPUT_DIR_EOS` inside the script.

It is handy if you want to submit the same configuration with different reconstructions as you can give the different `reco` options in a list of the bash script. Also you can simultaneously analyze multiple datasets with the same configuration.

As inputs you can use `*RAW*` e.g. for MC `GEN-SIM-RAW` (in case you need only the GEN and HLT objects info). If you also want the offline objects use `MINIAOD` and the option `-p 2` in `bdriver` command. This option `-p N` will search through `dasgoclient` for files that are the Nth "ancestor" of the file i.e. 
```
parent ...(N times)...  parent "FILE_NAME"
``` 
in our case `RAW` info is 2nd parent of MINIAOD `datasets`. 