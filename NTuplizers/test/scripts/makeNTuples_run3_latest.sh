#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=500000

OUTPUT_DIR_EOS=/eos/user/t/tchatzis/samples2023
ODIR=${1}


declare -A samplesMap

# QCD 
#samplesMap["Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65"]='/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter23MiniAOD-126X_mcRun3_2023_forPU65_v1-v2/MINIAODSIM'

# VBF H(125)->Invisible
samplesMap["Run3Winter23_VBF_HToInvisible_13p6TeV_PU65"]="/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Winter24MiniAOD-133X_mcRun3_2024_realistic_v9-v3/MINIAODSIM"

recoKeys=(
  default
  testMHT
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
  python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py dumpPython=.tmp_cfg.py 

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
    
    bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 1000 --memory 2G --time 02:00:00 \
      -d ${sampleName} -p 2 -o ${ODIR}/${recoKey}/${sampleKey} \
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
