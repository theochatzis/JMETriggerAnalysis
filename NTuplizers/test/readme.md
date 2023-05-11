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
For CRAB you can find some configuration scripts used in the `JMETriggerAnalysis/NTuplizers/test/crab` folder.
One example of a submission to CRAB:
```
crab submit -c crab3_test.py
```
one can change the outputfiles location from options:
`config.Site.storageSite` for the Site and `config.Data.outLFNDirBase` for the output directory path. 

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
