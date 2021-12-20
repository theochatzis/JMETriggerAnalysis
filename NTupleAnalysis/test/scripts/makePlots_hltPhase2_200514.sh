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

inpdir=${JMEANA_BASE}/output_hltPhase2_200514_v02
outdir=plots_hltPhase2_200514_v02

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

  if [[ ${sample} == "Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_"* ]]; then

    jmePlots.py -k phase2_dqm_compareTRK \
      -o ${outd_i}/dqm_compareTRK -l ${sample} -e pdf root png -i \
      ${inpdir}/ntuples/HLT_TRKv00/${sample}.root:'TRK v0':921:1:20 \
      ${inpdir}/ntuples/HLT_TRKv02/${sample}.root:'TRK v2':600:1:24 \
      ${inpdir}/ntuples/HLT_TRKv06/${sample}.root:'TRK v6':880:1:25 \
      ${inpdir}/ntuples/HLT_TRKv06_skimmedTracks/${sample}.root:'TRK v6 + skimTrk':801:1:26

    jmePlots.py -k phase2_dqm_compareTRK -m 'PFCandidateHistograms_*' \
      -o ${outd_i}/dqm_compareTRK_TICL -l ${sample} -e pdf root png -i \
      ${inpdir}/ntuples/HLT_TRKv00_TICL/${sample}.root:'TRK v0 + TICL':921:1:20 \
      ${inpdir}/ntuples/HLT_TRKv02_TICL/${sample}.root:'TRK v2 + TICL':600:1:24 \
      ${inpdir}/ntuples/HLT_TRKv06_TICL/${sample}.root:'TRK v6 + TICL':880:1:25 \
      ${inpdir}/ntuples/HLT_TRKv06_TICL_skimmedTracks/${sample}.root:'TRK v6 + skimTrk + TICL':801:1:26

    jmePlots.py -k phase2_dqm_compareTRK2 \
      -o ${outd_i}/dqm_compareTICL/TRKv06 -l ${sample} -e pdf root png -i \
      ${inpdir}/ntuples/HLT_TRKv06/${sample}.root:'TRK v6':1:1:20 \
      ${inpdir}/ntuples/HLT_TRKv06_TICL/${sample}.root:'TRK v6 + TICL':1:2:20

    jmePlots.py -k phase2_dqm_compareTRK2 \
      -o ${outd_i}/dqm_compareTICL/TRKv06_skimmedTracks -l ${sample} -e pdf root png -i \
      ${inpdir}/ntuples/HLT_TRKv06_skimmedTracks/${sample}.root:'TRK v6 + skimTrk':1:1:20 \
      ${inpdir}/ntuples/HLT_TRKv06_TICL_skimmedTracks/${sample}.root:'TRK v6 + skimTrk + TICL':1:2:20
  fi

  jmePlots.py -k phase2_jme_compareTRK1 ${opts_i} \
    -o ${outd_i}/jme_TRKv6 -l ${sample} -e pdf root png -i \
    ${inpdir}/harvesting/HLT_TRKv06/${sample}.root:'TRK v6':1:1:20 \

  jmePlots.py -k phase2_jme_compareTRK2 ${opts_i} \
    -o ${outd_i}/jme_compareTRK2_TICL -l ${sample} -e pdf root png -i \
    ${inpdir}/harvesting/HLT_TRKv06_TICL/${sample}.root:'TRK v6 + TICL':1:1:20 \
    ${inpdir}/harvesting/HLT_TRKv06_TICL_skimmedTracks/${sample}.root:'TRK v6 + skimTrk + TICL':1:2:24

  jmePlots.py -k phase2_jme_compareTRK5 ${opts_i} \
    -o ${outd_i}/jme_compareTRK5 -l ${sample} -e pdf root png -i \
    ${inpdir}/harvesting/HLT_TRKv00/${sample}.root:'TRK v0':921:1:20 \
    ${inpdir}/harvesting/HLT_TRKv02/${sample}.root:'TRK v2':600:1:24 \
    ${inpdir}/harvesting/HLT_TRKv06/${sample}.root:'TRK v6':880:1:25 \
    ${inpdir}/harvesting/HLT_TRKv06_skimmedTracks/${sample}.root:'TRK v6 + skimTrk':801:1:26

  jmePlots.py -k phase2_jme_compareTRK5 ${opts_i} \
    -o ${outd_i}/jme_compareTRK5_TICL -l ${sample} -e pdf root png -i \
    ${inpdir}/harvesting/HLT_TRKv00_TICL/${sample}.root:'TRK v0 + TICL':921:1:20 \
    ${inpdir}/harvesting/HLT_TRKv02_TICL/${sample}.root:'TRK v2 + TICL':600:1:24 \
    ${inpdir}/harvesting/HLT_TRKv06_TICL/${sample}.root:'TRK v6 + TICL':880:1:25 \
    ${inpdir}/harvesting/HLT_TRKv06_TICL_skimmedTracks/${sample}.root:'TRK v6 + skimTrk + TICL':801:1:26

  unset -v outd_i opts_i
done
unset -v sample

if [ ${tar_output} -gt 0 ] && [ -d ${outdirbase} ]; then
  tar cfz ${outdirbase}.tar.gz ${outdirbase}
  rm -rf ${outdirbase}
fi

unset -v inpdir outdir samples outdirbase tar_output
