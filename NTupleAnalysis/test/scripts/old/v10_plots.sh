#!/bin/bash

INPDIR=analysis_v10_test50K
OUTDIR=plots_v10_test50K

### compare L1TDR samples to 11_0_0 RelVals

#./jmePlots_compare.py -e png pdf root \
# -r ${INPDIR}/trkV2/outputs_postHarvesting/PhaseIITDRSpring19_QCD_Pt_15to3000_Flat_14TeV_NoPU.root \
# -t ${INPDIR}/trkV2/outputs_postHarvesting/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_NoPU.root \
# --r-leg 'QCD Pt_15_3000_Flat NoPU, L1TDR MC' \
# --t-leg 'QCD Pt_15_7000_Flat NoPU, RelVal 11_0_0' \
# -o ${OUTDIR}/106X_vs_110X/QCD_14TeV_NoPU
#
#./jmePlots_compare.py -e png pdf root \
# -r ${INPDIR}/trkV2/outputs_postHarvesting/PhaseIITDRSpring19_QCD_Pt_15to3000_Flat_14TeV_PU200.root \
# -t ${INPDIR}/trkV2/outputs_postHarvesting/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.root \
# --r-leg 'QCD Pt_15_3000_Flat PU200, L1TDR MC' \
# --t-leg 'QCD Pt_15_7000_Flat PU200, RelVal 11_0_0' \
# -o ${OUTDIR}/106X_vs_110X/QCD_14TeV_PU200

./jmePlots_compare.py -e png pdf root \
 -r ${INPDIR}/trkV2/outputs_postHarvesting/PhaseIITDRSpring19_TTbar_14TeV_NoPU.root \
 -t ${INPDIR}/trkV2/outputs_postHarvesting/RelVal1100_2026D49_TTbar_14TeV_NoPU.root \
 --r-leg 'TTbar NoPU, L1TDR MC' \
 --t-leg 'TTbar NoPU, RelVal 11_0_0' \
 -o ${OUTDIR}/106X_vs_110X/TTbar_14TeV_NoPU

./jmePlots_compare.py -e png pdf root \
 -r ${INPDIR}/trkV2/outputs_postHarvesting/PhaseIITDRSpring19_TTbar_14TeV_PU200.root \
 -t ${INPDIR}/trkV2/outputs_postHarvesting/RelVal1100_2026D49_TTbar_14TeV_PU200.root \
 --r-leg 'TTbar PU200, L1TDR MC' \
 --t-leg 'TTbar PU200, RelVal 11_0_0' \
 -o ${OUTDIR}/106X_vs_110X/TTbar_14TeV_PU200

### ---------------------------------------

### compare trkV2 to trkV2-skimmedTracks

./jmePlots_compare.py -e png pdf root \
 -r ${INPDIR}/trkV2/outputs_postHarvesting/PhaseIITDRSpring19_VBF_HToInvisible_14TeV_NoPU.root \
 -t ${INPDIR}/trkV2_skimmedTracks/outputs_postHarvesting/PhaseIITDRSpring19_VBF_HToInvisible_14TeV_NoPU.root \
 --r-leg 'VBF-HiggsToInv NoPU, L1TDR MC, trkV2' \
 --t-leg 'VBF-HiggsToInv NoPU, L1TDR MC, trkV2 + skimmedTracks' \
 -o ${OUTDIR}/trkV2_vs_trkV2skimmedTracks/VBFHToInv_14TeV_NoPU

./jmePlots_compare.py -e png pdf root \
 -r ${INPDIR}/trkV2/outputs_postHarvesting/PhaseIITDRSpring19_VBF_HToInvisible_14TeV_PU200.root \
 -t ${INPDIR}/trkV2_skimmedTracks/outputs_postHarvesting/PhaseIITDRSpring19_VBF_HToInvisible_14TeV_PU200.root \
 --r-leg 'VBF-HiggsToInv PU200, L1TDR MC, trkV2' \
 --t-leg 'VBF-HiggsToInv PU200, L1TDR MC, trkV2 + skimmedTracks' \
 -o ${OUTDIR}/trkV2_vs_trkV2skimmedTracks/VBFHToInv_14TeV_PU200

./jmePlots_compare.py -e png pdf root \
 -r ${INPDIR}/trkV2/outputs_postHarvesting/RelVal1100_2026D49_TTbar_14TeV_NoPU.root \
 -t ${INPDIR}/trkV2_skimmedTracks/outputs_postHarvesting/RelVal1100_2026D49_TTbar_14TeV_NoPU.root \
 --r-leg 'TTbar NoPU, RelVal 11_0_0, trkV2' \
 --t-leg 'TTbar NoPU, RelVal 11_0_0, trkV2 + skimmedTracks' \
 -o ${OUTDIR}/trkV2_vs_trkV2skimmedTracks/TTbar_14TeV_NoPU

./jmePlots_compare.py -e png pdf root \
 -r ${INPDIR}/trkV2/outputs_postHarvesting/RelVal1100_2026D49_TTbar_14TeV_PU200.root \
 -t ${INPDIR}/trkV2_skimmedTracks/outputs_postHarvesting/RelVal1100_2026D49_TTbar_14TeV_PU200.root \
 --r-leg 'TTbar PU200, RelVal 11_0_0, trkV2' \
 --t-leg 'TTbar PU200, RelVal 11_0_0, trkV2 + skimmedTracks' \
 -o ${OUTDIR}/trkV2_vs_trkV2skimmedTracks/TTbar_14TeV_PU200

./jmePlots_compare.py -e png pdf root \
 -r ${INPDIR}/trkV2/outputs_postHarvesting/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_NoPU.root \
 -t ${INPDIR}/trkV2_skimmedTracks/outputs_postHarvesting/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_NoPU.root \
 --r-leg 'QCD Pt_15_7000_Flat NoPU, RelVal 11_0_0, trkV2' \
 --t-leg 'QCD Pt_15_7000_Flat NoPU, RelVal 11_0_0, trkV2 + skimmedTracks' \
 -o ${OUTDIR}/trkV2_vs_trkV2skimmedTracks/QCD_14TeV_NoPU

./jmePlots_compare.py -e png pdf root \
 -r ${INPDIR}/trkV2/outputs_postHarvesting/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.root \
 -t ${INPDIR}/trkV2_skimmedTracks/outputs_postHarvesting/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.root \
 --r-leg 'QCD Pt_15_7000_Flat PU200, RelVal 11_0_0, trkV2' \
 --t-leg 'QCD Pt_15_7000_Flat PU200, RelVal 11_0_0, trkV2 + skimmedTracks' \
 -o ${OUTDIR}/trkV2_vs_trkV2skimmedTracks/QCD_14TeV_PU200

### ---------------------------------------

unset -v INPDIR OUTDIR
