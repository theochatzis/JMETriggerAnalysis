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

inpdir=${JMEANA_BASE}/output_hltRun3_testTRK_210225
outdir=output_hltRun3_testTRK_210225_plots

samples=(
#  Run3Winter20_QCD_PtFlat15to3000_14TeV_NoPU
  Run3Winter20_QCD_PtFlat15to3000_14TeV_PU
#  Run3Winter20_VBF_HToInvisible_14TeV_NoPU
  Run3Winter20_VBF_HToInvisible_14TeV_PU
)

exts=(
  pdf
  png
#  root
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
  if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-m 'NoSelection/*Jets*' 'NoSelection/*MET*_*' -s '*MET*GEN*'"
  elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-m 'NoSelection/*Jets*' 'NoSelection/*MET*_*'"
  fi

  jmePlots.py -k run3_jme_compareTRK1 ${opts_i} \
    -o ${outd_i}/jme_GRun -l ${sample} -e ${exts[*]} -i \
    ${inpdir}/harvesting/HLT_GRun/${sample}.root:'GRun':1:1:20

  jmePlots.py -k run3_jme_compareTRK1 ${opts_i} \
    -o ${outd_i}/jme_Run3TRK -l ${sample} -e ${exts[*]} -i \
    ${inpdir}/harvesting/HLT_Run3TRK/${sample}.root:'Run-3 TRK':1:1:20

  jmePlots.py -k run3_jme_compareTRK1 ${opts_i} \
    -o ${outd_i}/jme_Run3TRKWithPU -l ${sample} -e ${exts[*]} -i \
    ${inpdir}/harvesting/HLT_Run3TRKWithPU/${sample}.root:'Run-3 TRK-WithPU':1:1:20

  jmePlots.py -k run3_jme_compareTRK2 ${opts_i} \
    -o ${outd_i}/jme_compareTRK2 -l ${sample} -e ${exts[*]} -i \
    ${inpdir}/harvesting/HLT_GRun/${sample}.root:'GRun':1:1:20 \
    ${inpdir}/harvesting/HLT_Run3TRK/${sample}.root:'Run-3 TRK':2:2:24 \
    ${inpdir}/harvesting/HLT_Run3TRKWithPU/${sample}.root:'Run-3 TRK-WithPU':4:4:22

  jmePlots.py -k run3_jme_compareTRK5 ${opts_i} \
    -o ${outd_i}/jme_compareTRK5 -l ${sample} -e ${exts[*]} -i \
    ${inpdir}/harvesting/HLT_GRun/${sample}.root:'GRun':921:1:20 \
    ${inpdir}/harvesting/HLT_Run3TRK/${sample}.root:'Run-3 TRK':600:1:24 \
    ${inpdir}/harvesting/HLT_Run3TRKWithPU/${sample}.root:'Run-3 TRK-WithPU':880:1:25
#    ${inpdir}/harvesting/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p10/${sample}.root:'Patatrack+SingleIter, F=0.10':801:1:26 \
#    ${inpdir}/harvesting/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p30/${sample}.root:'Patatrack+SingleIter, F=0.30':632:1:27

  unset outd_i opts_i
done
unset sample

if [ ${tar_output} -gt 0 ] && [ -d ${outdirbase} ]; then
  tar cfz ${outdirbase}.tar.gz ${outdirbase}
  rm -rf ${outdirbase}
fi

unset inpdir outdir samples exts outdirbase tar_output
