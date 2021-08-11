#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  printf "%s\n" "\${JMEANA_BASE} is not a valid directory: ${JMEANA_BASE}"
  exit 1
fi

inpdir=${JMEANA_BASE}/run3_v04_analysis/harvesting
outdir=plots_run3test_trkIter2

if [ ! -f ${outdir%%/*}.tar.gz ]; then

  # ----
  sample=Run3Winter20_QCD_Pt_15to3000_Flat_14TeV

  jmePlots_run3.py -o ${outdir}/${sample}/HLT -l ${sample} -e pdf png root --PU200 \
   ${inpdir}/HLT/${sample}.root --skip-GenMET

  jmePlots_run3.py -o ${outdir}/${sample}/HLT_trkIter2GlobalPtSeed0p9 -l ${sample} -e pdf png root --PU200 \
   ${inpdir}/HLT_trkIter2GlobalPtSeed0p9/${sample}.root --skip-GenMET
  # ----

  # ----
  sample=Run3Winter20_QCD_Pt_50to80_14TeV

  jmePlots_run3.py -o ${outdir}/${sample}/HLT -l ${sample} -e pdf png root --PU200 \
   ${inpdir}/HLT/${sample}.root --skip-GenMET

  jmePlots_run3.py -o ${outdir}/${sample}/HLT_trkIter2GlobalPtSeed0p9 -l ${sample} -e pdf png root --PU200 \
   ${inpdir}/HLT_trkIter2GlobalPtSeed0p9/${sample}.root --skip-GenMET
  # ----

  # ----
  sample=Run3Winter20_ZprimeToMuMu_M6000_14TeV

  jmePlots_run3.py -o ${outdir}/${sample}/HLT -l ${sample} -e pdf png root --PU200 \
   ${inpdir}/HLT/${sample}.root

  jmePlots_run3.py -o ${outdir}/${sample}/HLT_trkIter2GlobalPtSeed0p9 -l ${sample} -e pdf png root --PU200 \
   ${inpdir}/HLT_trkIter2GlobalPtSeed0p9/${sample}.root
  # ----

  unset -v sample

  tar cfz ${outdir%%/*}.tar.gz ${outdir%%/*}
  rm -rf ${outdir%%/*}

else
  printf "%s\n" "output .tar.gz file already exists: ${outdir%%/*}.tar.gz"
  exit 1
fi

unset -v inpdir outdir
