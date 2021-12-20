#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  exit 1
fi

inpdir=${JMEANA_BASE}/run3_v04_analysis/harvesting
outdir=plots_run3test_pfBlockAlgoRemovePS_compareFiles

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
     ${inpdir}/HLT/${sample}.root:'Run-2':1 \
     ${inpdir}/HLT_pfBlockAlgoRemovePS/${sample}.root:'PFBlock w/o PS':2

    unset -v outd_i
  done
  unset -v sample

  tar cfz ${outdir%%/*}.tar.gz ${outdir%%/*}
  rm -rf ${outdir%%/*}
fi

unset -v inpdir outdir samples
