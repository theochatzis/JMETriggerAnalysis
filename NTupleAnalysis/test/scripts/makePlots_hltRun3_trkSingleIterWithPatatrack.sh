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

inpdir=${JMEANA_BASE}/output_hltRun3_trkSingleIterWithPatatrack_v02
outdir=plots_hltRun3_trkSingleIterWithPatatrack_v02

samples=(
  Run3Winter20_QCD_Pt_15to3000_Flat_14TeV
  Run3Winter20_DYToLL_M50_14TeV
  Run3Winter20_VBF_HToInvisible_14TeV
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
  elif [[ ${sample} == *"DYToLL"* ]]; then opts_i="-m '*MET_*' '*/offline*MET*_pt' -s '*MET*GEN*'"
  elif [[ ${sample} == *"ZprimeToMuMu"* ]]; then opts_i="-m '*METNoMu_*'"
  elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-m '*MET_*' '*/offlineMETs*_pt'"
  fi

  if [ ${sample} == "Run3Winter20_QCD_Pt_15to3000_Flat_14TeV" ]; then

    jmePlots.py -k run3_dqm_compareTRK2 \
      -o ${outd_i}/dqm_compareTRK2 -l ${sample} -e pdf root -i \
      ${inpdir}/ntuples/HLT/${sample}.root:'Run-2':1:1:20 \
      ${inpdir}/ntuples/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p30/${sample}.root:'Patatrack+SingleIter':2:2:24

    jmePlots.py -k run3_dqm_compareTRK5 \
      -o ${outd_i}/dqm_compareTRK5 -l ${sample} -e pdf root -i \
      ${inpdir}/ntuples/HLT/${sample}.root:'Run-2':921:1:20 \
      ${inpdir}/ntuples/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p00/${sample}.root:'Patatrack+SingleIter, F=0.00':600:1:24 \
      ${inpdir}/ntuples/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p01/${sample}.root:'Patatrack+SingleIter, F=0.01':880:1:25 \
      ${inpdir}/ntuples/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p10/${sample}.root:'Patatrack+SingleIter, F=0.10':801:1:26 \
      ${inpdir}/ntuples/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p30/${sample}.root:'Patatrack+SingleIter, F=0.30':632:1:27
  fi

  jmePlots.py -k run3_jme_compareTRK1 ${opts_i} \
    -o ${outd_i}/jme_compareTRK1_trkSingleIter -l ${sample} -e pdf root -i \
    ${inpdir}/harvesting/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p30/${sample}.root:'Patatrack+SingleIter':1:1:20

  jmePlots.py -k run3_jme_compareTRK2 ${opts_i} \
    -o ${outd_i}/jme_compareTRK2 -l ${sample} -e pdf root -i \
    ${inpdir}/harvesting/HLT/${sample}.root:'Run-2':1:1:20 \
    ${inpdir}/harvesting/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p30/${sample}.root:'Patatrack+SingleIter':2:2:24

  jmePlots.py -k run3_jme_compareTRK5 ${opts_i} \
    -o ${outd_i}/jme_compareTRK5 -l ${sample} -e pdf root -i \
    ${inpdir}/harvesting/HLT/${sample}.root:'Run-2':921:1:20 \
    ${inpdir}/harvesting/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p00/${sample}.root:'Patatrack+SingleIter, F=0.00':600:1:24 \
    ${inpdir}/harvesting/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p01/${sample}.root:'Patatrack+SingleIter, F=0.01':880:1:25 \
    ${inpdir}/harvesting/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p10/${sample}.root:'Patatrack+SingleIter, F=0.10':801:1:26 \
    ${inpdir}/harvesting/HLT_singleTrkIterWithPatatrack_v01_pixVtxFrac0p30/${sample}.root:'Patatrack+SingleIter, F=0.30':632:1:27

  unset -v outd_i opts_i
done
unset -v sample

if [ ${tar_output} -gt 0 ] && [ -d ${outdirbase} ]; then
  tar cfz ${outdirbase}.tar.gz ${outdirbase}
  rm -rf ${outdirbase}
fi

unset -v inpdir outdir samples outdirbase tar_output
