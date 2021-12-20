#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=200000

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
samplesMap["Run3Winter20_QCD_PtFlat15to3000_14TeV_NoPU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-NoPU_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM"
samplesMap["Run3Winter20_QCD_PtFlat15to3000_14TeV_PU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM"

# VBF H(125)->Invisible
samplesMap["Run3Winter20_VBF_HToInvisible_14TeV_PU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v1/MINIAODSIM"

recoKeys=(
  HLT_GRun
  HLT_Run3TRK
  HLT_Run3TRKWithPU
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
  python jmeTriggerNTuple_cfg.py dumpPython=/tmp/${USER}/${recoKey}_cfg.py numThreads=1 reco=${recoKey} #globalTag=

  for sampleKey in ${!samplesMap[@]}; do
    sampleName=${samplesMap[${sampleKey}]}

    # number of events per sample
    numEvents=${NEVT}
    if [[ ${sampleKey} == *MinBias* ]]; then
      numEvents=2000000
    fi

    htc_driver -c /tmp/${USER}/${recoKey}_cfg.py --customize-cfg -m ${numEvents} -n 500 --cpus 1 --memory 2000 --runtime 10800 ${opts} \
      -d ${sampleName} -p 1 -o ${ODIR}/${recoKey}/${sampleKey} --cmsRun-output-dir ${ODIR_cmsRun}/${recoKey}/${sampleKey}
  done
  unset sampleKey numEvents sampleName

done
unset recoKey opts recoKeys samplesMap NEVT ODIR ODIR_cmsRun
