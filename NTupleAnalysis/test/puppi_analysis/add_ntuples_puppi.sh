#/bin/bash

# define the samples you want to use
recoKeys=(
  HLT_Run3TRK
)

MinNeutralPt_factors=(
0.0
)

MinNeutralPtSlope_factors=(
0.0
)

NTUPLES_IDIR=/eos/user/t/tchatzis/PUPPI_samples/$1
NTUPLES_ODIR=/eos/user/t/tchatzis/PUPPI_samples/$1

FOUND_NTUPLES_ODIR=false


for recoKey in "${recoKeys[@]}"; do
  for MinNeutralPt_factor in  "${MinNeutralPt_factors[@]}"; do
    for MinNeutralPtSlope_factor in "${MinNeutralPtSlope_factors[@]}"; do

      # clear all files that are not filled (smaller than 10kilobyte size)
      find ${NTUPLES_IDIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor} -name "*.root" -type 'f' -size -10k -delete
      
      # add the ntuples jobs from input dir
      hadd_ntuples.py -i ${NTUPLES_IDIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU -o ${NTUPLES_ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/ -l 0
      hadd_ntuples.py -i ${NTUPLES_IDIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU -o ${NTUPLES_ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/ -l 0

      
      # save the configuration file from jobs directory
      cp ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/$1/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU/cfg.py ${NTUPLES_ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/cfg_qcd.py
      cp ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/$1/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU/cfg.py ${NTUPLES_ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/cfg_higgs.py
      
      # delete the files of jobs directory
      #rm -rf ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/$1/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/
    done
  done
done





unset recoKeys MinNeutralPt_factors MinNeutralPtSlope_factors 
unset NTUPLES_IDIR NTUPLES_ODIR
unset FOUND_NTUPLE_ODIR


