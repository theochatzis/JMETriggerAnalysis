# multicrab
#
# Usage:   multicrab.py <pset> [options]
# Datasamples defined in crab/createCrabConfigFilesMiniAOD.py

# Example:
cd CMSSW_X_Y_Z/src/JMETriggerAnalysis/NTuplizers/test
voms-proxy-init -voms cms
crab/multicrab.py jmeTriggerNTuple2023Data_miniAOD_cfg.py -i 2024                                                                                                    

# Help:
crab/multicrab.py -h

Usage: Step1: make flat ntuples with crab
      multicrab.py <pset> [-options]
      multicrab.py --status [<dir>]
      multicrab.py --resubmit [<dir>]

Options:
  -h, --help            show this help message and exit
  --status              Flag to check the status of CRAB jobs
  --resubmit            Flag to resubmit CRAB jobs
  -i, --include         Regexp for including tasks
                        Only perform action for this dataset(s) [default: ""]
  -e, --exclude         Regexp for excluding tasks
                        Exclude this dataset(s) from action [default: ""]
  -d, --dir             Use existing multicrab [default: ""]
  -l, --list            List datasets and exit


If you need to resubmit dataset X:
-go to the multicrab dir
-rm the problem dataset
-cd ..
-multicrab.py <pset> -d <the-multicrab-dir>
The script will submit only those datasets which are missing (=the one just removed)
