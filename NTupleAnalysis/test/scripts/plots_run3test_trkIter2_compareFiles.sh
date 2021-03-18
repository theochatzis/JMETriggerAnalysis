#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  exit 1
fi

inpdir=${JMEANA_BASE}/run3_v04_analysis/harvesting
outdir=plots_run3test_trkIter2_compareFiles

samples=(
 Run3Winter20_QCD_Pt_15to3000_Flat_14TeV
 Run3Winter20_QCD_Pt_50to80_14TeV
 Run3Winter20_QCD_Pt_170to300_14TeV
 Run3Winter20_DYToLL_M50_14TeV
 Run3Winter20_ZprimeToMuMu_M6000_14TeV
)

if [ ! -f ${outdir%%/*}.tar.gz ]; then

  for sample in "${samples[@]}"; do

    outd_i=${outdir}/${sample}

    jmePlots_compareFiles.py -o ${outd_i} -l ${sample} -e pdf png root -i \
     ${inpdir}/HLT/${sample}.root:'Reg 0.4':1 \
     ${inpdir}/HLT_trkIter2RegionalPtSeed0p9/${sample}.root:'Reg 0.9':920 \
     ${inpdir}/HLT_trkIter2RegionalPtSeed2p0/${sample}.root:'Reg 2.0':800 \
     ${inpdir}/HLT_trkIter2RegionalPtSeed5p0/${sample}.root:'Reg 5.0':880 \
     ${inpdir}/HLT_trkIter2RegionalPtSeed10p0/${sample}.root:'Reg 10.0':2 \
     ${inpdir}/HLT_trkIter2GlobalPtSeed0p9/${sample}.root:'Glo 0.9':4

    unset -v outd_i
  done
  unset -v sample

  tar cfz ${outdir%%/*}.tar.gz ${outdir%%/*}
  rm -rf ${outdir%%/*}
fi

unset -v inpdir outdir samples
