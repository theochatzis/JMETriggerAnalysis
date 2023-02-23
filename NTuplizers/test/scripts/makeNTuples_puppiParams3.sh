#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=50000

OUTPUT_DIR_EOS=/eos/user/t/tchatzis/PUPPI_samples
ODIR=${1}


declare -A samplesMap

# QCD 
#samplesMap["Run3Winter21_QCD_Pt15to7000_14TeV_NoPU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-NoPU_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM"
#samplesMap["Run3Winter21_QCD_Pt15to7000_14TeV_PU"]="/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM"
#samplesMap["Run3Winter21_QCD_Pt15to7000_14TeV_PU"]="/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Winter21DRMiniAOD-FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/MINIAODSIM"
#samplesMap["Run3Winter21_QCD_Pt15to7000_14TeV_PU"]="/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Summer21MiniAOD-FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v5-v1/MINIAODSIM"
#samplesMap["Run3Winter21_QCD_Pt15to7000_14TeV_PU"]='/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Winter21DRMiniAOD-FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/GEN-SIM-DIGI-RAW'
samplesMap["Run3Winter21_QCD_Pt15to7000_14TeV_PU"]='/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Summer21DR-FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/GEN-SIM-DIGI-RAW'

# VBF H(125)->Invisible
#samplesMap["Run3Winter20_VBF_HToInvisible_14TeV_PU"]="/VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v1/MINIAODSIM"
#samplesMap["Run3Winter21_VBF_HToInvisible_14TeV_PU"]="/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8/Run3Winter21DRMiniAOD-FlatPU30to80FEVT_112X_mcRun3_2021_realistic_v16-v1/MINIAODSIM"
#samplesMap["Run3Winter21_VBF_HToInvisible_14TeV_PU"]="/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8/Run3Winter21DRMiniAOD-FlatPU30to80FEVT_112X_mcRun3_2021_realistic_v16-v1/GEN-SIM-RECO"
#samplesMap["Run3Winter21_VBF_HToInvisible_14TeV_PU"]="/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8/Run3Summer21DRPremix-120X_mcRun3_2021_realistic_v6-v2/GEN-SIM-DIGI-RAW"

# DY
#samplesMap["Run3Winter21_DYJetsToMuMu"]='/DYJetsToMuMu_M-50_TuneCP5_14TeV-madgraphMLM-pythia8/Run3Winter21DRMiniAOD-designGT_112X_mcRun3_2021_realistic_v16_ext1-v2/GEN-SIM-DIGI-RAW'
#samplesMap["Run3Winter21_DYToLL"]='/DYToLL_M-4To50_TuneCP5_14TeV-pythia8/Run3Winter21DRMiniAOD-FlatPU30to80FEVT_112X_mcRun3_2021_realistic_v16-v3/GEN-SIM-DIGI-RAW'
#samplesMap["Run3Winter21_DYToLL"]='/DYToLL_M-50_TuneCP5_13p6TeV-pythia8/Run3Winter22DR-L1TPU0to99FEVT_122X_mcRun3_2021_realistic_v9-v2/GEN-SIM-DIGI-RAW'
# TT
#samplesMap["Run3Winter21_TT"]='/TT_TuneCP5_14TeV-powheg-pythia8/Run3Winter21DRMiniAOD-FlatPU30to80FEVT_112X_mcRun3_2021_realistic_v16-v2/GEN-SIM-DIGI-RAW'
#samplesMap["Run3Winter21_TT"]='/TT_TuneCP5_14TeV-powheg-pythia8/Run3Winter21DRMiniAOD-FlatPU30to80FEVT_112X_mcRun3_2021_realistic_v16-v2/GEN-SIM-DIGI-RAW'
#samplesMap["Run3Winter21_TT"]='/TT_TuneCP5_14TeV-powheg-pythia8/Run3Summer21DRPremix-120X_mcRun3_2021_realistic_v6-v2/GEN-SIM-DIGI-RAW'

#samplesMap["Run3Winter22_TT"]='/TT_TuneCP5_13p6TeV-powheg-pythia8/Run3Winter22DR-PUForTRK_DIGI_122X_mcRun3_2021_realistic_v9-v2/GEN-SIM-DIGI-RAW'
#samplesMap["Run3Winter21_TT"]='/TT_TuneCP5_14TeV-powheg-pythia8/Run3Winter21DRMiniAOD-FlatPU20to70_for_DNN_112X_mcRun3_2021_realistic_v16_ext1-v2/GEN-SIM-DIGI-RAW'
recoKeys=(
  HLT_Run3TRK
)

MinNeutralPt_factors=(
0.0
)

MinNeutralPtSlope_factors=(
0.0
)


if [ -d ${OUTPUT_DIR_EOS}/${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  echo "If you continue the following directories will get overwritten: "
  for recoKey in "${recoKeys[@]}"; do
    for MinNeutralPt_factor in  "${MinNeutralPt_factors[@]}"; do
      for MinNeutralPtSlope_factor in "${MinNeutralPtSlope_factors[@]}"; do
        find ${OUTPUT_DIR_EOS}/${ODIR} -path ${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}
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
  for MinNeutralPt_factor in  "${MinNeutralPt_factors[@]}"; do
    for MinNeutralPtSlope_factor in "${MinNeutralPtSlope_factors[@]}"; do
      
      python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi_less_HLTonly.py useMixedTrk=True keepPFPuppi=False dumpPython=.tmp_cfg.py
            #  puppiParamsHB=MinNeutralPtSlope:0.4 \
            #  puppiParamsHE1=MinNeutralPtSlope:0.0 \
            #  puppiParamsHF=MinNeutralPtSlope:1.25 \
            #  puppiParamsHE2=MinNeutralPtSlope:4.0
      
      #python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi_less_HLTonly.py dumpPython=.tmp_cfg.py

      #python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi_less_HLTonly.py dumpPython=.tmp_cfg.py \
      #       puppiParamsHE1=MinNeutralPt:${MinNeutralPt_factor},MinNeutralPtSlope:${MinNeutralPtSlope_factor}
      
      #python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi_less_HLTonly.py useMixedTrk=True keepPFPuppi=False dumpPython=.tmp_cfg.py
      
      # good settings with PU vertices
      #python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi_less_HLTonly.py dumpPython=.tmp_cfg.py \
      #       puppiParamsHB=MinNeutralPtSlope:2.0 \
      #       puppiParamsHE1=MinNeutralPtSlope:6.0 \
      #       puppiParamsHE2=MinNeutralPtSlope:4.0 \
      #       puppiParamsHF=MinNeutralPtSlope:1.5
      
      # good settings without PU vertices
      #python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi_less_HLTonly.py dumpPython=.tmp_cfg.py \
      #       puppiParamsHB=MinNeutralPtSlope:2.0 \
      #       puppiParamsHE1=MinNeutralPtSlope:6.0 \ # probably better 10.0
      #       puppiParamsHE2=MinNeutralPtSlope:18.0 \
      #       puppiParamsHF=MinNeutralPtSlope:2.0
      
      #python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg_puppi_less_HLTonly.py dumpPython=.tmp_cfg.py \
      
      

      for sampleKey in ${!samplesMap[@]}; do
        sampleName=${samplesMap[${sampleKey}]}
        
        # number of events per sample
        numEvents=${NEVT}
        
        # directory for the jobs output ntuples
        FINAL_OUTPUT_DIR=${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/${sampleKey} 

        # removing the output directory and its contents if it already exists
        if [ -d ${FINAL_OUTPUT_DIR} ]; then rm -rf ${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}; fi
      
        mkdir -p ${FINAL_OUTPUT_DIR}
        
        if [ -d ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/${sampleKey} ]; then rm -rf ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/${sampleKey}; fi

        bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 500 --memory 2G --time 02:00:00 \
          -d ${sampleName} -p 0 -o ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/${sampleKey} \
          --final-output ${FINAL_OUTPUT_DIR} \
          --submit \
          --customise-commands \
          '# output [TFileService]' \
          "if hasattr(process, 'TFileService'):" \
          '  process.TFileService.fileName = opts.output'
      done
      unset sampleKey numEvents sampleName

      rm -f .tmp_cfg.py

    done
  done

  #bmonitor -i ${ODIR} -r -f 60 --repeat 20 

done
unset recoKey recoKeys samplesMap NEVT ODIR
