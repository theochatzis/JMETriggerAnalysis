#!/bin/bash

for sss in QCD_Pt_15to3000_Flat_14TeV_PU200 VBF_HToInvisible_M125_14TeV_PU200; do

./jmePlots_compare.py \
 -r analysis_prod_v04/outputs_postHarvesting/${sss}.root \
 -t analysis_prod_v05/outputs_postHarvesting/${sss}.root \
 --r-leg 'trkV2 + PFlow-HF-fix' \
 --t-leg 'trkV2 + PFlow-HF-fix + skimmedTracks' \
 -o tmptmptmp/${sss} \
 -e png pdf

done
unset -v sss
