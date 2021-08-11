#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  exit 1
fi

tar_output=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tar) tar_output=1; shift;;
  esac
done

inpdir=${JMEANA_BASE}/output_hltPhase2_200702_v01
outdir=plots_hltPhase2_200702_v01

samples=(
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_NoPU
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200
  Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU
  Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
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
  if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-m '*Jets*' '*MET_*' '*/offline*MET*_pt' -s '*MET*GEN*'"
  elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-m '*MET_*' '*/offlineMETs*_pt'"
  fi

  jmePlots.py -k phase2_jme_compareTRK1 ${opts_i} \
    -o ${outd_i}/HLT_TRKv06_TICL -l ${sample} -e pdf root png -i \
    ${inpdir}/harvesting/HLT_TRKv06_TICL/${sample}.root:'TRK v6 + TICL':1:1:20 \

  jmePlots.py -k phase2_jme_compareTRK1_withL1T ${opts_i} \
    -o ${outd_i}/HLT_TRKv06_TICL_withL1T -l ${sample} -e pdf root png -i \
    ${inpdir}/harvesting/HLT_TRKv06_TICL/${sample}.root:'TRK v6 + TICL':1:1:20 \

  unset -v outd_i opts_i
done
unset -v sample

if [ ${tar_output} -gt 0 ] && [ -d ${outdirbase} ]; then
  tar cfz ${outdirbase}.tar.gz ${outdirbase}
  rm -rf ${outdirbase}
fi

unset -v inpdir outdir samples outdirbase tar_output
