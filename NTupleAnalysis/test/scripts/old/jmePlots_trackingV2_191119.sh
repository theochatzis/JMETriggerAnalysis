#!/bin/bash

OTAG=outputs_trackingV2_191119

IDIR=${OTAG}/outputs_postHarvesting
ODIR=${OTAG}_plots

for ll in QCD_Pt_0_1000_14TeV; do

  jmePlots.py --NoPU ${IDIR}/${ll}_NoPU_temp.root --PU140 ${IDIR}/${ll}_PU140_temp.root --PU200 ${IDIR}/${ll}_PU200_temp.root -l ${ll} -o ${ODIR}/${ll} -e png pdf --skip-GenMET

done
unset -v ll

for ll in TT_14TeV VBF_HToInvisible_M125_14TeV; do

  jmePlots.py --NoPU ${IDIR}/${ll}_NoPU_temp.root --PU140 ${IDIR}/${ll}_PU140_temp.root --PU200 ${IDIR}/${ll}_PU200_temp.root -l ${ll} -o ${ODIR}/${ll} -e png pdf

done
unset -v ll

unset -v OTAG ODIR IDIR

#jmePlots_AvsB.py \
#  -A output_191104_Tracking_V0/histos/Bkg/NoPU.root:'Tracking V0' \
#  -B outputs_trackingV2_191114_test2/outputs_postHarvesting/QCD_Pt_0_1000_14TeV_NoPU_temp.root:'Tracking V2' \
#  -l QCD_Pt_0_1000_14TeV_NoPU \
#  -e png pdf \
#  -o outputs_V0vsV2_2/QCD_Pt_0_1000_14TeV_NoPU \
#  --skip-GEN
#
#jmePlots_AvsB.py -A output_191104_Tracking_V0/histos/Bkg/PU200.root:'Tracking V0' -B outputs_trackingV2_191114_test2/outputs_postHarvesting/QCD_Pt_0_1000_14TeV_PU200_temp.root:'Tracking V2' -l QCD_Pt_0_1000_14TeV_PU200 -e png pdf -o outputs_V0vsV2_2/QCD_Pt_0_1000_14TeV_PU200 --skip-GEN
#
#for dd in PU140 PU200; do jmePlots_AvsB.py -A output_191104_Tracking_V0/histos/Sig/${dd}.root:'Tracking V0' -B outputs_trackingV2_191114_test2/outputs_postHarvesting/VBF_HToInvisible_M125_14TeV_${dd}.root:'Tracking V2' -l VBF_HToInvisible_M125_14TeV_${dd} -e png pdf -o outputs_V0vsV2_2/VBF_HToInvisible_M125_14TeV_${dd}; done; unset -v dd;
