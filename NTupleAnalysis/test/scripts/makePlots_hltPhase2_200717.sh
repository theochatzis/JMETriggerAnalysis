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

inpdir_R=${JMEANA_BASE}/output_hltPhase2_200702_v01
inpdir_0=${JMEANA_BASE}/output_hltPhase2_200717_PuppiMod0_v02
inpdir_1=${JMEANA_BASE}/output_hltPhase2_200730_PuppiMod3_v01
#inpdir_2=${JMEANA_BASE}/output_hltPhase2_200717_PuppiMod2_v02

outdir=plots_hltPhase2_200730_v03_comparePuppi

samples=(
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_NoPU
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200
  Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU
  Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
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

#  opts_i=""
#  if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-m 'NoSel*/*Jets*' 'NoSel*/*MET_*' 'NoSel*/*/offline*MET*_pt' -s '*MET*GEN*'"
#  elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-m 'NoSel*/*MET_*' 'NoSel*/*/offlineMETs*_pt'"
#  fi
#
#  jmePlots.py -k jme_compare ${opts_i} \
#    -o ${outd_i}/HLT_TRKv06_TICL_compare/11_1_2 -l ${sample} -e ${exts[*]} -i \
#    ${inpdir_R}/harvesting/HLT_TRKv06_TICL/${sample}.root:'11_1_0_pre6':1:1:20 \
#    ${inpdir_0}/harvesting/HLT_TRKv06_TICL/${sample}.root:'11_1_2':2:2:22

#  opts_i=""
#  if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-m 'NoSel*/*PuppiJetsCorr*' 'NoSel*/*PuppiMET_*' 'NoSel*/*/offlinePuppiMET*_pt' -s '*MET*GEN*'"
#  elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-m 'NoSel*/*PuppiMET_*' 'NoSel*/*/offlinePuppiMETs*_pt'"
#  fi
#
#  jmePlots.py -k jme_compare ${opts_i} \
#    -o ${outd_i}/HLT_TRKv06_compare/Puppi_BTuned -l ${sample} -e ${exts[*]} -i \
#    ${inpdir_0}/harvesting/HLT_TRKv06/${sample}.root:'11_1_2':1:1:20 \
#    ${inpdir_1}/harvesting/HLT_TRKv06/${sample}.root:'+ B-Tuned':2:1:22 \
#    ${inpdir_2}/harvesting/HLT_TRKv06/${sample}.root:'+ PU-1or2':4:1:24

  opts_i=""
  if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-m 'NoSel*/*GenJets*MatchedTo*eff' 'NoSel*/*JetsCorr*' 'NoSel*/*MET_*' 'NoSel*/*/offline*MET*_pt' -s '*MET*GEN*'"
  elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-m 'NoSel*/*MET_*' 'NoSel*/*/offline*METs*_pt'"
  fi

#  jmePlots.py -k phase2_jme_compareTRK1 ${opts_i} \
#    -o ${outd_i}/HLT_TRKv06/Puppi_tuneHLT1 -l ${sample} -e ${exts[*]} -i \
#    ${inpdir_1}/harvesting/HLT_TRKv06/${sample}.root:'':1:1:20
#
#  jmePlots.py -k phase2_jme_compareTRK1_withL1T ${opts_i} \
#    -o ${outd_i}/HLT_TRKv06_withL1T/Puppi_tuneHLT1 -l ${sample} -e ${exts[*]} -i \
#    ${inpdir_1}/harvesting/HLT_TRKv06/${sample}.root:'':1:1:20

  jmePlots.py -k phase2_jme_comparePuppi ${opts_i} \
    -o ${outd_i}/HLT_TRKv06_compare -l ${sample} -e ${exts[*]} -i \
    ${inpdir_0}/harvesting/HLT_TRKv06/${sample}.root:'Puppi':4:1:20 \
    ${inpdir_1}/harvesting/HLT_TRKv06/${sample}.root:'Puppi retuned':921:1:20 \
    ${inpdir_1}/harvesting/HLT_TRKv06_TICL/${sample}.root:'Puppi retuned + TICL':801:1:20

  jmePlots.py -k phase2_jme_compare ${opts_i} \
    -o ${outd_i}/HLT_TRKv06_compareTICL -l ${sample} -e ${exts[*]} -i \
    ${inpdir_1}/harvesting/HLT_TRKv06/${sample}.root:'w/o TICL':1:1:20 \
    ${inpdir_1}/harvesting/HLT_TRKv06_TICL/${sample}.root:'w/ TICL':2:1:24

  unset -v outd_i opts_i
done
unset -v sample

if [ ${tar_output} -gt 0 ] && [ -d ${outdirbase} ]; then
  tar cfz ${outdirbase}.tar.gz ${outdirbase}
  rm -rf ${outdirbase}
fi

unset -v inpdir outdir samples exts outdirbase tar_output
