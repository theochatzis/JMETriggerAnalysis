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

samplesMap["Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200"]="/TT_TuneCP5_14TeV-powheg-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_AllTP_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD"

# additional options for bdriver 
#opts="--submit"
opts=""

python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_L1Only_cfg.py dumpPython=.tmp_L1_cfg.py
python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py reco=default dumpPython=.tmp_cfg.py numThreads=1
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
  
  if [[ "${sampleName}" == *"GEN-SIM-DIGI-RAW"* ]]; then
  bdriver -c .tmp_cfg.py -cl1 .tmp_L1_cfg.py --customize-cfg -m ${numEvents} -n 50 --memory 16G --time 02:00:00 ${opts} --batch-system htc \
  -d ${sampleName} -p 0 -o ${ODIR}/${sampleKey} \
  --final-output ${FINAL_OUTPUT_DIR} \
  --submit \
  --customise-commands \
  '# output [TFileService]' \
  "if hasattr(process, 'TFileService'):" \
  '  process.TFileService.fileName = opts.output' 
  unset numEvents sampleName
  fi

done

unset sampleKey

rm -f .tmp_cfg.py
rm -f .tmp_L1_cfg.py

unset opts samplesMap NEVT ODIR FINAL_OUTPUT_DIR
