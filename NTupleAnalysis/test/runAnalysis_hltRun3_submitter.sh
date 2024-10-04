#!/bin/bash
source env.sh
BASE_DIR=/eos/user/s/slehti/CoffTeaNTuples_v1407_Run2023BCD_20240905T1544/
OUT_EOS_DIR=/samples2023/DPNote2023/
JOBS_DIR_NAME=DPNote2023

dataKeys=(
  JetMET0_Run2023CV2
)

FIRST_USER_LETTER=${USER:0:1}

for dataKey in "${dataKeys[@]}"; do
  echo ${dataKey}
  # directory with input JMETriggerNTuple(s)
  INPDIR=${BASE_DIR}${dataKey}"/*/*/*/*"
  #directory with outputs of NTupleAnalysis
  OUTDIR=./${JOBS_DIR_NAME}/${dataKey}
  OUTPUTDIR=/eos/user/${FIRST_USER_LETTER}/${USER}/${OUT_EOS_DIR}/${dataKey}/

  mkdir -p ${OUTDIR}
  [ -d ${OUTDIR}/ntuples ] || (ln -sf ${INPDIR} ${OUTDIR}/ntuples)
  batch_driver.py -l 1 -n 100000 -p JMETriggerAnalysisDriverRun3 \
   -i ${INPDIR}/*.root -o ${OUTDIR}/jobs \
   -od ${OUTPUTDIR} \
   --JobFlavour espresso
  
  mkdir -p ${OUTPUTDIR}

  batch_monitor.py -i ${OUTDIR}/jobs -r #--repe -f 1200
done

unset recoKey recoKey

