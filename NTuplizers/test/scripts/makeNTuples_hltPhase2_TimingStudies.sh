#!/bin/bash -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=10000
ODIR=${1}

#if [ -d ${ODIR} ]; then
#  printf "%s\n" "output directory already exists: ${ODIR}"
#  exit 1
#fi

declare -A samplesMap

# QCD pthat 15-3000
#samplesMap["Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_NoPU"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU140"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"

#samplesMap["Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"
samplesMap["Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200"]="/QCD_Pt-15To3000_TuneCP5_Flat_14TeV-pythia8/PhaseIISpring22DRMiniAOD-PU200_castor_123X_mcRun4_realistic_v11-v1/GEN-SIM-DIGI-RAW-MINIAOD"

# VBF H(125)->Invisible
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU140"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1_ext1-v2/FEVT"
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200"]="/VBF_HToInvisible_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"


# additional options for bdriver 
opts="--submit"

python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py dumpPython=.tmp_cfg.py numThreads=1
for sampleKey in ${!samplesMap[@]}; do
  sampleName=${samplesMap[${sampleKey}]}

  # number of events per sample
  numEvents=${NEVT}
  if [[ ${sampleKey} == *MinBias* ]]; then
    numEvents=2000000
  fi
    
  FINAL_OUTPUT_DIR=/eos/user/t/tchatzis/MTDtiming_samples/${ODIR}/${sampleKey}
    
  if [ -d ${FINAL_OUTPUT_DIR} ]; then
    printf "%s\n" "directory for saving jobs outputs already exists: ${FINAL_OUTPUT_DIR}"
    read -p "Do you want to rewrite it? [y/n]" yn
    case $yn in
      [Yy]* ) rm -rf ${FINAL_OUTPUT_DIR}; echo "Continuing the process...";;
      [Nn]* ) echo "Exiting..."; exit 1;;
      * ) echo "Please answer with y/n.";;
    esac
  fi
    
  mkdir -p ${FINAL_OUTPUT_DIR}
  
  if [ -d ./${ODIR}/${sampleKey} ]; then 
    rm -rf ./${ODIR}/${sampleKey}
  fi 

  # Note: You can automatically run the jobs after creating them by using --submit option of bdriver
  bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 100 --cpus 1 --memory 2G --time 00:45:00 ${opts} --batch-system htc \
  -d ${sampleName} -p 1 -o ${ODIR}/${sampleKey} \
  --final-output ${FINAL_OUTPUT_DIR} \
  --customise-commands \
  '# output [TFileService]' \
  "if hasattr(process, 'TFileService'):" \
  '  process.TFileService.fileName = opts.output' 
      
  unset numEvents sampleName

done

unset sampleKey

rm -f .tmp_cfg.py

unset opts samplesMap NEVT ODIR FINAL_OUTPUT_DIR
