#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=10000

ODIR=${1}


declare -A samplesMap

# QCD Pt-Flat
#samplesMap["Run3Winter20_QCD_PtFlat15to3000_14TeV_NoPU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-NoPU_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM"
samplesMap["Run3Winter20_QCD_PtFlat15to3000_14TeV_PU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM"

# VBF H(125)->Invisible
samplesMap["Run3Winter20_VBF_HToInvisible_14TeV_PU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v1/MINIAODSIM"

recoKeys=(
  HLT_Run3TRK
)

RMSEtaSF_factors=(
0.1
0.25
0.5
1.5
2.0
5.0
10.0
)

MedEtaSF_factors=(
1.0
)


if [ -d ${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  echo "If you continue the following directories will get overwritten: "
  for recoKey in "${recoKeys[@]}"; do
    for RMSEtaSF_factor in  "${RMSEtaSF_factors[@]}"; do
      for MedEtaSF_factor in "${MedEtaSF_factors[@]}"; do
        find ./${ODIR} -path ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}
      done
    done
  done
  read -p "Do you want to continue? [y/n]" yn
  case $yn in
      [Yy]* ) echo "Continuing the process...";;
      [Nn]* ) echo "Exiting..."; unset recoKey recoKeys samplesMap NEVT ODIR; exit 1;;
      * ) echo "Please answer with y/n.";;
  esac
fi



for recoKey in "${recoKeys[@]}"; do
  for RMSEtaSF_factor in  "${RMSEtaSF_factors[@]}"; do
    for MedEtaSF_factor in "${MedEtaSF_factors[@]}"; do
      
      
      python ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi_less.py dumpPython=.tmp_cfg.py numThreads=1 reco=${recoKey} puppiParamsHE1=MinNeutralPt:1.0,MinNeutralPtSlope:1.0 \
             puppiParamsHB=MinNeutralPt:1.0,MinNeutralPtSlope:1.0 \
             puppiParamsHE2=MinNeutralPt:1.0,MinNeutralPtSlope:1.0,RMSEtaSF:${RMSEtaSF_factor},MedEtaSF:${MedEtaSF_factor} \
             puppiParamsHF=MinNeutralPt:1.0,MinNeutralPtSlope:1.0
             #,RMSEtaSF:${RMSEtaSF_factor},MedEtaSF:${MedEtaSF_factor}
      
      # removing the output directory and its contents if it already exists
      if [ -d ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor} ]; then rm -rf ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}; fi

      for sampleKey in ${!samplesMap[@]}; do
        sampleName=${samplesMap[${sampleKey}]}

        # number of events per sample
        numEvents=${NEVT}

        bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 500 --memory 2G --time 00:30:00 \
          -d ${sampleName} -p 1 -o ${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/${sampleKey} \
          --customise-commands \
          '# output [TFileService]' \
          "if hasattr(process, 'TFileService'):" \
          '  process.TFileService.fileName = opts.output'
      done
      unset sampleKey numEvents sampleName

      rm -f .tmp_cfg.py

    done
  done

done
unset recoKey recoKeys samplesMap NEVT ODIR
