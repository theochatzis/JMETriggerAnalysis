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

inpdir_0=${JMEANA_BASE}/output_hltPhase2_200822_base
inpdir_1=${JMEANA_BASE}/output_hltPhase2_200822_head

outdir=plots_hltPhase2_200822_v01

samples=(
  Phase2HLTTDR_WJetsToLNu_14TeV_PU200
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
  if [[ ${sample} == *"WJetsToLNu_"* ]]; then opts_i="-m 'NoSel*/*GenJets*MatchedTo*eff' 'NoSel*/*JetsCorr*' 'NoSel*/*MET_*' 'NoSel*/*/offline*MET*_pt'"
  else
    break
  fi

  jmePlots.py -k phase2_jme_compare ${opts_i} \
    -o ${outd_i}/HLT_TRKv06 -l ${sample} -e ${exts[*]} -i \
    ${inpdir_0}/harvesting/HLT_TRKv06/${sample}.root:'11_0_X RAW':1:1:20 \
    ${inpdir_1}/harvesting/HLT_TRKv06/${sample}.root:'HLT-TDR ReReco':2:2:22

  jmePlots.py -k phase2_jme_compare ${opts_i} \
    -o ${outd_i}/HLT_TRKv06_TICL -l ${sample} -e ${exts[*]} -i \
    ${inpdir_0}/harvesting/HLT_TRKv06_TICL/${sample}.root:'11_0_X RAW':1:1:20 \
    ${inpdir_1}/harvesting/HLT_TRKv06_TICL/${sample}.root:'HLT-TDR ReReco':2:2:22

  jmePlots.py -k phase2_jme_comparePuppi ${opts_i} \
    -o ${outd_i}/HLT_TRKv06_comparePuppi_reReco -l ${sample} -e ${exts[*]} -i \
    ${inpdir_1}/harvesting/HLT_TRKv06/${sample}.root:'':4:1:20 \

  jmePlots.py -k phase2_jme_comparePuppi ${opts_i} \
    -o ${outd_i}/HLT_TRKv06_TICL_comparePuppi_reReco -l ${sample} -e ${exts[*]} -i \
    ${inpdir_1}/harvesting/HLT_TRKv06_TICL/${sample}.root:'':4:1:20 \

  unset -v outd_i opts_i
done
unset -v sample

if [ ${tar_output} -gt 0 ] && [ -d ${outdirbase} ]; then
  tar cfz ${outdirbase}.tar.gz ${outdirbase}
  rm -rf ${outdirbase}
fi

unset -v inpdir outdir samples exts outdirbase tar_output
