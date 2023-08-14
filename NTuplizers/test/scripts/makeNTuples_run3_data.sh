#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=10000000

OUTPUT_DIR_EOS=/eos/user/t/tchatzis/samples2023
ODIR=${1}


declare -A samplesMap

# data 
#samplesMap["data"]='/JetMET/Run2022G-PromptReco-v1/MINIAOD'
#samplesMap["data"]='/Muon/Run2022G-PromptReco-v1/MINIAOD'
samplesMap["data"]='/Muon0/Run2023C-ZMu-PromptReco-v4/RAW-RECO'

recoKeys=(
  default
  #option5
  #option3
)

if [ -d ${OUTPUT_DIR_EOS}/${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  echo "If you continue the following directories will get overwritten: "
  for recoKey in "${recoKeys[@]}"; do
    find ${OUTPUT_DIR_EOS}/${ODIR} -path ${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}
  done
  read -p "Do you want to continue? [y/n]" yn
  case $yn in
      [Yy]* ) echo "Continuing the process...";;
      [Nn]* ) echo "Exiting..."; unset recoKey recoKeys samplesMap NEVT ODIR; exit 1;;
      * ) echo "Please answer with y/n.";;
  esac
fi



for recoKey in "${recoKeys[@]}"; do
  python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple2023Data_compare_cfg.py reco=${recoKey} dumpPython=.tmp_cfg.py #lumis=${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/Cert_Collisions2022_eraG_362433_362760_Golden.json 

  for sampleKey in ${!samplesMap[@]}; do
    sampleName=${samplesMap[${sampleKey}]}
    
    # number of events per sample
    numEvents=${NEVT}
    
    # directory for the jobs output ntuples
    FINAL_OUTPUT_DIR=${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}/${sampleKey} 

    # removing the output directory and its contents if it already exists
    if [ -d ${FINAL_OUTPUT_DIR} ]; then rm -rf ${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}/; fi
  
    mkdir -p ${FINAL_OUTPUT_DIR}
    
    if [ -d ${ODIR}/${recoKey}/${sampleKey} ]; then rm -rf ${ODIR}/${recoKey}/${sampleKey}; fi
    
    bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 5000 --memory 2G --time 02:00:00 \
      -d ${sampleName} -p 0 -o ${ODIR}/${recoKey}/${sampleKey} \
      --final-output ${FINAL_OUTPUT_DIR} \
      --submit \
      --customise-commands \
      '# output [TFileService]' \
      "if hasattr(process, 'TFileService'):" \
      '  process.TFileService.fileName = opts.output'
  done
  unset sampleKey numEvents sampleName

  rm -f .tmp_cfg.py

  

  #bmonitor -i ${ODIR} -r -f 60 --repeat 20 

done
unset recoKey recoKeys samplesMap NEVT ODIR
