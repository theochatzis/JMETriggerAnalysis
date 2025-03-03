#!/bin/bash

OUTDIR=l2only_full_ntuples_standardPlusGausFit

set -e

mkdir -p ${OUTDIR}
cd ${OUTDIR}
unset OUTDIR

# pre-processing
if [ ! -f step0.sh ]; then
  JRA_PU=${CMSSW_BASE}/src/ntup_5M/flatpu.root
  echo "mkdir -p jraNTuples && \\
${CMSSW_BASE}/src/JetMETAnalysis/JetAnalyzers/scripts/renameJRADirs.py -v 2 -i ${JRA_PU} -o jraNTuples/PU.root  2>&1 | tee step0.log" > step0.sh
  unset JRA_PU
  source step0.sh
fi


## L2+L3
if [ ! -f step6.done ]; then
  echo "jet_response_analyzer_x ${CMSSW_BASE}/src/JetMETAnalysis/JetAnalyzers/config/jra_hltPhase2.config -input jraNTuples/PU.root -algs ak4puppi -nbinsabsrsp 0 -nbinsetarsp 0 -nbinsphirsp 0 -nbinsrelrsp 200 -doflavor false -output histogram_ak4puppi_step6.root -useweight false -nrefmax 20 -relrspmin 0.0 -relrspmax 5.0 2>&1 | tee step6.log" > step6.sh
  source step6.sh && touch step6.done
fi

if [ ! -f step7.done ]; then
  echo "jet_l2_correction_x -input histogram_ak4puppi_step6.root -algs ak4puppi -era ERA -output l2p3.root -outputDir ./ -makeCanvasVariable AbsCorVsJetPt:JetEta -l2l3 true -batch true -histMet median -l2pffit Standard+Gaussian -maxFitIter 30 -ptclipfit false 2>&1 | tee step7.log" > step7.sh
  source step7.sh && touch step7.done
fi

if [ ! -f step8.done ]; then
  echo "mkdir -p plots_step8 && jet_correction_analyzer_x -evtmax 0 -ptmin 30 -inputFilename jraNTuples/PU.root -algs ak4puppi -drmax 0.1 -L1FastJet false -useweight false -path ./ -era ERA -levels 2 -outputDir ./plots_step8 -nbinsrelrsp 200 -relrspmin 0.0 -relrspmax 5.0 -nrefmax 20 2>&1 | tee step8.log" > step8.sh
  source step8.sh && touch step8.done
fi

if [ ! -f step9.done ]; then
  echo "jet_draw_closure_x -path plots_step8 -filename Closure_ak4puppi -histMet median -outputDir plots_step9 -draw_guidelines true -doPt true -doEta true -doRatioPt false -doRatioEta false 2>&1 | tee step9.log" > step9.sh
  source step9.sh && touch step9.done
fi
