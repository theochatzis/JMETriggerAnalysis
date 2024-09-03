# Step1: make flat ntuples with crab

## Multicrab

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
