#!/bin/bash

plotNames=(
  jetResponse_HB
  jetResponse_HGCal
  jetResolution
  jetMatchingEff_HLT_genMatchEff
  jetMatchingEff_HLT_recoMistagRate
  triggerRate_SingleJet
  triggerEff_SingleJet_wrtGEN
  triggerRate_HT
  triggerEff_HT_wrtGEN
  metResponse
  metResolution_perpToGEN
  triggerRate_METTypeOneMHT30
  triggerEff_METTypeOneMHT30_wrtGEN_PU200_140_VBFHToInv
)

DIROLD=fig/hltjetmetreco
DIRNEW=output_hltPhase2_201209_tdrDraft2_deltaR02_v2_plots_forCWR
OUTDIR=tmp_compare

mkdir -p "${OUTDIR}"

for plotName_i in "${plotNames[@]}"; do

  cp "${DIROLD}"/"${plotName_i}".png "${OUTDIR}"/"${plotName_i}"_old.png
  cp "${DIRNEW}"/"${plotName_i}".png "${OUTDIR}"/"${plotName_i}"_new.png
done
