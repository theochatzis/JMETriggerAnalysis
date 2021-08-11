#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=-1

if [ $# -eq 1 ]; then
  ODIR=${1}
  ODIR_cmsRun=$1
else
  ODIR=${1}
  ODIR_cmsRun=${2}
fi

if [ -d ${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  exit 1
fi

declare -A samplesMap

# QCD Pt-Flat
samplesMap["Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200"]="/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT"

# VBF H(125)->Invisible
samplesMap["Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200"]="/VBF_HToInvisible_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"

recoKeys=(
  HLT_TRKv06p1_TICL
  HLT_75e33
)

# options (JobFlavour and AccountingGroup)
opts=""
if [[ ${HOSTNAME} == lxplus* ]]; then
  opts+="--JobFlavour longlunch"
  if [[ ${USER} == missirol ]]; then
    opts+=" --AccountingGroup group_u_CMS.CAF.PHYS"
  fi
fi

for recoKey in "${recoKeys[@]}"; do
  python jmeTriggerNTuple_cfg.py dumpPython=/tmp/${USER}/${recoKey}_cfg.py numThreads=1 reco=${recoKey} trkdqm=1 pvdqm=1 pfdqm=1

  for sampleKey in ${!samplesMap[@]}; do
    sampleName=${samplesMap[${sampleKey}]}

    # number of events per sample
    numEvents=${NEVT}
    if [[ ${sampleKey} == *MinBias* ]]; then
      numEvents=2000000
    fi

    htc_driver -c /tmp/${USER}/${recoKey}_cfg.py --customize-cfg -m ${numEvents} -n 250 --cpus 1 --memory 2000 --runtime 10800 ${opts} \
      -d ${sampleName} -p 0 -o ${ODIR}/${recoKey}/${sampleKey} --cmsRun-output-dir ${ODIR_cmsRun}/${recoKey}/${sampleKey}
  done
  unset sampleKey numEvents sampleName

done
unset recoKey opts recoKeys samplesMap NEVT ODIR ODIR_cmsRun
