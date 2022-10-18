#!/bin/bash -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=20000
ODIR=${1}

#TUNE_QUANTITY="MinNeutralPt"
#TUNE_QUANTITY="MinNeutralPtSlope"
#TUNE_QUANTITY="DeltaZCut"


# TUNE_VALUES=(
#   0.1
#   0.2
#   0.3
#   0.5
#   100.0
# )

# TUNE_VALUES=(
#   0.00
#   0.25
#   0.50
#   0.75
#   1.00
# )

TUNE_VALUES=(
  0.1
  0.2
  0.3
)

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

#samplesMap["RelValQCD_Pt15To7000_Flat_14TeV_PU200"]="/RelValQCD_Pt15To7000_Flat_14/CMSSW_12_4_0_pre3-PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/MINIAODSIM"
#samplesMap["RelValQCD_Pt15To7000_Flat_14TeV_noPU"]="/RelValQCD_Pt15To7000_Flat_14/CMSSW_12_4_0_pre3-123X_mcRun4_realistic_v11_2026D88noPU-v1/MINIAODSIM"

# VBF H(125)->Invisible
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_111X_mcRun4_realistic_T15_v1-v1/FEVT"
#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU140"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1_ext1-v2/FEVT"

#samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200"]="/VBFHToInvisible_M-125_TuneCP5_14TeV-powheg-pythia8/PhaseIISpring22DRMiniAOD-PU200_123X_mcRun4_realistic_v11-v1/GEN-SIM-DIGI-RAW-MINIAOD"



# additional options for bdriver 
opts="--submit"

for VALUE in ${TUNE_VALUES[@]}; do
  python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_puppiTune_cfg.py dumpPython=.tmp_cfg.py numThreads=1 \
    puppiParamsCentral1=MinNeutralPt:1.0,MinNeutralPtSlope:1.0 \
    puppiParamsCentral2=MinNeutralPt:1.0,MinNeutralPtSlope:1.0 \
    puppiParamsForward=MinNeutralPt:1.0,MinNeutralPtSlope:1.0 \
    DeltaZCut=0.3 \
    DeltaTCut=${VALUE} 
  
  for sampleKey in ${!samplesMap[@]}; do
    sampleName=${samplesMap[${sampleKey}]}

    # number of events per sample
    numEvents=${NEVT}
    if [[ ${sampleKey} == *MinBias* ]]; then
      numEvents=2000000
    fi
      
    FINAL_OUTPUT_DIR=/eos/user/t/tchatzis/MTDtiming_samples/${ODIR}/${sampleKey}/value_${VALUE}/
      
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
    
    if [ -d ./${ODIR}/${sampleKey}/value_${VALUE} ]; then 
      rm -rf ./${ODIR}/${sampleKey}/value_${VALUE}
    fi 

    # Note: You can automatically run the jobs after creating them by using --submit option of bdriver
    
    if [[ "${sampleName}" == *"GEN-SIM-DIGI-RAW"* ]]; then
    bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 100 --cpus 1 --memory 2G --time 02:00:00 ${opts} --batch-system htc \
    -d ${sampleName} -p 0 -o ${ODIR}/${sampleKey}/value_${VALUE} \
    --final-output ${FINAL_OUTPUT_DIR} \
    --customise-commands \
    '# output [TFileService]' \
    "if hasattr(process, 'TFileService'):" \
    '  process.TFileService.fileName = opts.output' 
    else
    bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 100 --cpus 1 --memory 2G --time 02:00:00 ${opts} --batch-system htc \
    -d ${sampleName} -p 1 -o ${ODIR}/${sampleKey}/value_${VALUE} \
    --final-output ${FINAL_OUTPUT_DIR} \
    --customise-commands \
    '# output [TFileService]' \
    "if hasattr(process, 'TFileService'):" \
    '  process.TFileService.fileName = opts.output' 
    fi
        
    unset numEvents sampleName

  done
  unset sampleKey
done



rm -f .tmp_cfg.py

unset opts samplesMap NEVT ODIR FINAL_OUTPUT_DIR TUNE_VALUES
