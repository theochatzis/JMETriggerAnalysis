#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=1000

ODIR=${1}

if [ -d ${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  exit 1
fi

declare -A samplesMap

# QCD Pt-Flat
#samplesMap["Run3Winter20_QCD_PtFlat15to3000_14TeV_NoPU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-NoPU_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM"
samplesMap["Run3Winter20_QCD_PtFlat15to3000_14TeV_PU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM"

# VBF H(125)->Invisible
samplesMap["Run3Winter20_VBF_HToInvisible_14TeV_PU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v1/MINIAODSIM"

recoKeys=(
  HLT_Run3TRK
)

MinNeutralPt_factors=(
1.0
)

MinNeutralPtSlope_factors=(
1.0
)

for recoKey in "${recoKeys[@]}"; do
  for MinNeutralPt_factor in  "${MinNeutralPt_factors[@]}"; do
      for MinNeutralPtSlope_factor in "${MinNeutralPtSlope_factors[@]}"; do

      python ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi.py dumpPython=.tmp_${recoKey}_cfg.py numThreads=1 reco=${recoKey} \
             #puppiParamsHB=MinNeutralPt:${MinNeutralPt_factor},MinNeutralPtSlope:${MinNeutralPtSlope_factor} \
             puppiParamsHE1=MinNeutralPt:${MinNeutralPt_factor},MinNeutralPtSlope:${MinNeutralPtSlope_factor} \
             #puppiParamsHE2=MinNeutralPt:${MinNeutralPt_factor},MinNeutralPtSlope:${MinNeutralPtSlope_factor} \
             #puppiParamsHF=MinNeutralPt:${MinNeutralPt_factor},MinNeutralPtSlope:${MinNeutralPtSlope_factor} 
      done
  done

  for sampleKey in ${!samplesMap[@]}; do
    sampleName=${samplesMap[${sampleKey}]}

    # number of events per sample
    numEvents=${NEVT}
    if [[ ${sampleKey} == *MinBias* ]]; then
      numEvents=2000000
    fi

    bdriver -c .tmp_${recoKey}_cfg.py --customize-cfg -m ${numEvents} -n 1000 --cpus 1 --mem 2G --JobFlavor "microcentury" \
      -d ${sampleName} -p 1 -o ${ODIR}/${recoKey}/${sampleKey} \
      --customise-commands \
       '# output [TFileService]' \
       "if hasattr(process, 'TFileService'):" \
       '  process.TFileService.fileName = opts.output'
  done
  unset sampleKey numEvents sampleName

  rm -f .tmp_${recoKey}_cfg.py
done
unset recoKey recoKeys samplesMap NEVT ODIR
