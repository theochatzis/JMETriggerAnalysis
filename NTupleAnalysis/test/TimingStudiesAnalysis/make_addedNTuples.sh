#!/bin/bash -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify name of NTuples directory"
  exit 1
fi

IDIR=${1}

# set the environment
#source ../env.sh

declare -A samplesMap

# QCD pthat 15-3000
#samplesMap["Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU140"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU140"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"
samplesMap["Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"

#samplesMap["RelValQCD_Pt15To7000_Flat_14TeV_PU200"]="/RelValQCD_Pt15To7000_Flat_14/CMSSW_12_4_0_pre3-PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/MINIAODSIM"
#samplesMap["RelValQCD_Pt15To7000_Flat_14TeV_noPU"]="/RelValQCD_Pt15To7000_Flat_14/CMSSW_12_4_0_pre3-123X_mcRun4_realistic_v11_2026D88noPU-v1/MINIAODSIM"

# VBF H(125)->Invisible
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU140"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1_ext1-v2/FEVT"
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200"]="/VBF_HToInvisible_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"

#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200"]="/VBFHToInvisible_M-125_TuneCP5_14TeV-powheg-pythia8/PhaseIISpring22DRMiniAOD-PU200_123X_mcRun4_realistic_v11-v1/GEN-SIM-DIGI-RAW-MINIAOD"

for sampleKey in ${!samplesMap[@]}; do
  sampleName=${samplesMap[${sampleKey}]}
    
  INPUT_DIR=/eos/user/t/tchatzis/MTDtiming_samples/${IDIR}/${sampleKey}

  # clear all files that are not filled (smaller than 5kilobyte size)
  find ${INPUT_DIR} -name "*.root" -type 'f' -size -5k -delete
  # add the NTuples in the directory
  ../hadd_ntuples.py -i ${INPUT_DIR} -o ${INPUT_DIR} -l 0
  # after finishing with that remove the output files of multiple jobs
  #rm ${INPUT_DIR}/out_*.root 
  unset sampleName

  cp ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/${IDIR}/${sampleKey}/cfg.py /eos/user/t/tchatzis/MTDtiming_samples/${IDIR}/${sampleKey}/

  # remove the folder with the jobs settings in NTuplizers
  printf  "removing the directory: " 
  echo ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/${IDIR}/${sampleKey}
  rm -rf ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/${IDIR}/${sampleKey}

done
unset sampleKey
 


unset samplesMap IDIR INPUT_DIR