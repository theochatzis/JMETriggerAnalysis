#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  printf "%s\n" "environment variable JMEANA_BASE does not contain a valid directory: JMEANA_BASE=${JMEANA_BASE}"
  exit 1
fi

tar_output=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tar) tar_output=1; shift;;
  esac
done

inpdir=${JMEANA_BASE}/output_hltPhase2_valTICL1116
outdir=plots_hltPhase2_210113_valTICL1116

samples=(
# Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_NoPU
  Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200
# Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU
# Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
)

exts=(
  pdf
  png
# root
)

outdirbase=${outdir%%/*}

if [ ${tar_output} -gt 0 ] && [ -f ${outdirbase}.tar.gz ]; then
  printf "%s\n" ">> target output file already exists: ${outdirbase}.tar.gz"
  exit 1
fi

if [ -d ${outdirbase} ]; then
  printf "%s\n" ">> target output directory already exists: ${outdirbase}"
  exit 1
fi

for sample in "${samples[@]}"; do

  outd_i=${outdir}/${sample}

  opts_i=""
  if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-m 'NoSel*/*JetsCorr*' 'NoSel*/*MET_*' 'NoSel*/*/offline*MET*_pt' -s '*MET*GEN*'"
  elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-m 'NoSel*/*MET_*' 'NoSel*/*/offline*METs*_pt'"
  fi

  jmePlots.py -k phase2_jme_comparePFPuppi ${opts_i} \
    -o ${outd_i}/compareTRK_TICL -l ${sample} -e ${exts[*]} -i \
    ${inpdir}/harvesting/HLT_TRKv06p1_TICL_1113p/${sample}.root:'TRK-v6.1 [11_1_3]':1:1:20 \
    ${inpdir}/harvesting/HLT_TRKv06p1_TICL_1116/${sample}.root:'TRK-v6.1 [11_1_6]':2:1:24

  jmePlots.py -k phase2_jme_compareTRK1 ${opts_i} \
    -o ${outd_i}/compareTRK1_TRKv06p1_TICL_1113p -l ${sample} -e ${exts[*]} -i \
    ${inpdir}/harvesting/HLT_TRKv06p1_TICL_1113p/${sample}.root:'TRK-v6.1 [11_1_3]':1:1:20

  jmePlots.py -k phase2_jme_compareTRK1 ${opts_i} \
    -o ${outd_i}/compareTRK1_TRKv06p1_TICL_1116 -l ${sample} -e ${exts[*]} -i \
    ${inpdir}/harvesting/HLT_TRKv06p1_TICL_1116/${sample}.root:'TRK-v6.1 [11_1_6]':1:1:20

  unset outd_i opts_i
done
unset sample

if [ ${tar_output} -gt 0 ] && [ -d ${outdirbase} ]; then
  tar cfz ${outdirbase}.tar.gz ${outdirbase}
  rm -rf ${outdirbase}
fi

unset inpdir outdir samples exts outdirbase tar_output
