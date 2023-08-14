#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

# number of total events to run 
NEVT=1000000000

# directory in EOS space
OUTPUT_DIR_EOS=/eos/user/t/tchatzis/CoffteaNTuples
# output directory name 
# this will appear in EOS space and a folder locally containing the Condor submission scripts and config file.
ODIR=${1}

# Create a samples map with key and file name in DAS.
# You can have more than one samples.
declare -A samplesMap

# MuonEraC 
samplesMap["data"]='/Muon0/Run2023C-PromptReco-v4/MINIAOD'

# Just a check the output directories do not exist. If they do ask permission to delete them.
if [ -d ${OUTPUT_DIR_EOS}/${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  echo "If you continue the following directories will get overwritten: "
  read -p "Do you want to continue? [y/n]" yn
  case $yn in
      [Yy]* ) echo "Continuing the process...";;
      [Nn]* ) echo "Exiting..."; unset recoKey recoKeys samplesMap NEVT ODIR; exit 1;;
      * ) echo "Please answer with y/n.";;
  esac
fi

# Create configuration file for condor scripts
python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple2023Data_miniAOD_cfg.py globalTag=130X_dataRun3_Prompt_v3 dumpPython=.tmp_cfg.py 

for sampleKey in ${!samplesMap[@]}; do
  sampleName=${samplesMap[${sampleKey}]}
    
  # number of events per sample
  numEvents=${NEVT}
    
  # directory for the jobs output ntuples
  FINAL_OUTPUT_DIR=${OUTPUT_DIR_EOS}/${ODIR}/${sampleKey} 

  # removing the output directory and its contents if it already exists
  if [ -d ${FINAL_OUTPUT_DIR} ]; then rm -rf ${OUTPUT_DIR_EOS}/${ODIR}/; fi
  
  mkdir -p ${FINAL_OUTPUT_DIR}
    
  if [ -d ${ODIR}/${sampleKey} ]; then rm -rf ${ODIR}/${sampleKey}; fi
  
  # Create condor scripts and submit them (if --submit is used)
  # if --submit not used here you can submit the job later with bmonitor script (see bellow) 
  bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 10000000 --memory 2G --time 02:00:00 \
    -d ${sampleName} -p 0 -o ${ODIR}/${sampleKey} \
    --final-output ${FINAL_OUTPUT_DIR} \
    --submit \
    --customise-commands \
    '# output [TFileService]' \
    "if hasattr(process, 'TFileService'):" \
    '  process.TFileService.fileName = opts.output'
done
unset sampleKey numEvents sampleName

rm -f .tmp_cfg.py

# bmonitor script used for resubmiting jobs ( -r)
# or for checking jobs progress 
# e.g. with -f 60 --repeat 20 means every 60 seconds check the jobs, and do this 20 times 
# so 20 minutes it will check the jobs - and if -r is there it will resubmit any job without output file.
#bmonitor -i ${ODIR} -r -f 60 --repeat 20 

unset recoKey samplesMap NEVT ODIR
