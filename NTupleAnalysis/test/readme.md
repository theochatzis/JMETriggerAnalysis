## Tools for analysis of JMETrigger NTuples

### Recipe using tools mentioned in sections bellow
#### Running the analysis step
The first step is to make histograms from the NTuples you have produced. The histograms are derived using the `run.py` python script which executes one of the plugins that exist in the `NTupleAnalysis/src` directory.
The plugins basic functionality is :
- Define objects collections that we want to analyze and the corresponding reference collections. The code will try to match the objects of the collection to the ones of the reference in order to be able to define things like Efficiency, Purity, Response etc.
These are defined through label maps e.g. `labelMap_jetAK4_` in the `JMETriggerAnalysisDriverRun3.cc`. Also the matching can be performed in different regions of the detector defined as well in the scripts.
- Define regions of selections (based on trigger bits in the NTuples) : The Analysis script books/fills histograms based on categorizing the events in different triggers, selections of PU, Run etc. As such you can have the same histograms in different phase space allowing to define trigger efficiencies.

In order to run the scripts with batch jobs you could use the executable `runAnalysis_hltRun3_submitter.sh`.
First make sure the directories are set correctly:
- `BASE_DIR` : This is tha base directory of the crab/condor jobs. The script loops over subdirectories of this `BASE_DIR` called `data_keys` and does the procedure for all these subfolders. The outputs will be saved also based on the subfolders names.
- `OUT_EOS_DIR` : This is the directory in your private eos space where you want to save the results.
- `JOBS_DIR_NAME` : This is just a local directory that will be created and condor submission jobs will be stored. You can inspect this and see the executable shell and condor submission scripts exist.

After the directories are correctly you can do:
```
./runAnalysis_hltRun3_submitter.sh
```
which will show jobs getting submitted.

**Note (Recommendation when you re-run HLT)**: 
If you use the script as it is you will get most likely one job per file. In case your files are too many (when re-running HLT normally this is the case because `RAW` inputs have very few events per file), it is better to first add the files in a big one using `hadd` or the private tool `hadd_ntuples` and then use this file as input. The jobs will be split accroding to the `-n` option in `batch_driver.py` which is the maximum number of events per job. 
You can see an example of adding NTuples from:
```
addNTuples_2023Data.sh
```

#### Running the harvesting step
After the jobs from the analysis step are finished you will end up with a lot of ROOT files containing the needed histograms for the analysis. Another step then is the "harvesting", which is doing essentially 2 jobs:
1. Adding the output histograms all together
2. Creating new plots like matching efficiency, responses and resolutions. 

Again there is a script demonstrating how this can be done the `runAnalysis_hltRun3_harvester.sh`:
- Make sure `OUT_EOS_DIR` is the same as in the analysis script.
- You can give any name you like to the merged output file by `OUTPUT_FILE_NAME`.
```
./runAnalysis_hltRun3_harvester.sh
```
This step should be fast and produce a single file in the `${OUT_EOS_DIR}/harvesting` directory in your EOS space.
If you inspect the `.root` file you should be able to see for the different selection directories the previous histograms you had but also the matching efficiencies, responses etc.

#### Plotting
After the harvesting root file is produced we use it as input to create the final plots.
There are some available scripts for this job, most basic ones are:
- `jmePlots.py` this is essentially looping over all the histograms (histograms keys) and looks for specific patterns to save and plot based on the keyword it is given (`-k` option). You can find an example in `plotPerformancesData_config.sh`
- `plotEfficiencies*.py` scripts. These are just using numerators and denominators. You can find an example of calling the script from `plotEfficiencies_2023Data.sh`.

ToDo: Add the new plotting scripts used for the DPNote (and the recipe).

### Basic tools definitions

Workflow to produce Jet/MET performance plots from "flat" ROOT NTuples

#### Setup

* Update global environment variables:
```
source env.sh
```

#### Prepare Analysis NTuples from batch/crab3 outputs

* Create output directory with one .root for each crab3 task:
```
hadd_ntuples.py -i [DIRS] -o [OUTDIR] -l 0 -s DQM
```

#### Submit Analysis Jobs to Batch System (HT-Condor)

* Create scripts for submission of batch jobs:
```
batch_driver.py -i ${NTUDIR}/*root -o ${OUTDIR}/jobs -n 50000 -l 0 # -p $PLUGIN
```

* Monitoring and (re)submission of batch jobs:
```
batch_monitor.py -i ${OUTDIR}
```

#### Harvesting of Outputs

* Merge outputs of batch jobs:
```
merge_batchOutputs.py -i ${OUTDIR}/jobs/*.root -o ${OUTDIR}/outputs -l 0
```

* Harvest outputs (manipulates histograms, produces profiles, efficiencies, etc):
```
jmeAnalysisHarvester.py -i ${OUTDIR}/outputs/*.root -o ${OUTDIR}/harvesting -l 0
```
