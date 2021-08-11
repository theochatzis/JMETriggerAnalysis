#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  exit 1
fi

tar_output=0
while test $# -gt 0; do
  case "$1" in
    --tar) tar_output=1;;
  esac
  shift
done

inpdir=${JMEANA_BASE}/output_hltPhase2_200429_v01
outdir=plots_hltPhase2_200429_v01

samples=(
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_NoPU
  Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200
  Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU
  Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
)

recos=(
  TRKv00
  TRKv06
)

outdirbase=${outdir%%/*}

if [ ! -f ${outdirbase}.tar.gz ] && [ ! -d ${outdirbase} ]; then

  for reco_key in "${recos[@]}"; do

    for sample in "${samples[@]}"; do

      outd_i=${outdir}/${reco_key}_compareWithTICL/${sample}

      sample_label=${sample/Phase2HLTTDR_/}

      opts_i=""
      if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-k '*Jets*' '*MET_pt'"
      elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-k '*MET_*'"
      elif [[ ${sample} == *"DYToLL"* ]]; then opts_i="-k '*MET_*'"
      elif [[ ${sample} == *"ZprimeToMuMu"* ]]; then opts_i="-k '*METNoMu_*'"
      fi

#      dqmPlots_compareFiles.py -o ${outd_i}/tracksAndPFlow -l "["${reco_key}"] "${sample_label} -e pdf png -i \
#        ${inpdir}/ntuples/HLT_${reco_key}/${sample}.root:'':1:1:20 \
#        ${inpdir}/ntuples/HLT_${reco_key}_TICL/${sample}.root:'[w/ TICL]':2:1:24

      if [[ ${sample} == *"Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV"* ]]; then
        dqmPlots_compareObjs.py -u -o ${outdir}/${reco_key}/${sample}/tracksAndPFlow_compareObjs -l "["${reco_key}"] "${sample_label} -e pdf png root -i \
          ${inpdir}/ntuples/HLT_${reco_key}/${sample}.root:'':1:1:20

        dqmPlots_compareFilesAndObjs.py -u -o ${outd_i}/tracksAndPFlow_compareObjs -l "["${reco_key}"] "${sample_label} -e pdf png -i \
          ${inpdir}/ntuples/HLT_${reco_key}/${sample}.root:'':1:1:20 \
          ${inpdir}/ntuples/HLT_${reco_key}_TICL/${sample}.root:'[w/ TICL]':2:2:24
      fi

#      jmePlots_compareFiles.py -u ${opts_i} -o ${outd_i}/jme -l "["${reco_key}"] "${sample_label} -e pdf root -i \
#        ${inpdir}/harvesting/HLT_${reco_key}/${sample}.root:'':1:1:20 \
#        ${inpdir}/harvesting/HLT_${reco_key}_TICL/${sample}.root:'[w/ TICL]':2:1:24
#
#      jmePlots_compareObjs.py -u ${opts_i} -o ${outdir}/${reco_key}/${sample}/jme_compareObjs -l "["${reco_key}"] "${sample_label} -e pdf root -i \
#        ${inpdir}/harvesting/HLT_${reco_key}/${sample}.root:'':1:1:20
#
#      jmePlots_compareFilesAndObjs.py -u ${opts_i} -o ${outd_i}/jme_compareObjs -l "["${reco_key}"] "${sample_label} -e pdf root -i \
#        ${inpdir}/harvesting/HLT_${reco_key}/${sample}.root:'':1:1:20 \
#        ${inpdir}/harvesting/HLT_${reco_key}_TICL/${sample}.root:'[w/ TICL]':2:2:24

      unset -v outd_i opts_i
    done
    unset -v sample

  done
  unset -v reco_key

  if [ ${tar_output} -gt 0 ] && [ -d ${outdirbase} ]; then
    tar cfz ${outdirbase}.tar.gz ${outdirbase}
    rm -rf ${outdirbase}
  fi
fi

unset -v inpdir outdir samples recos outdirbase tar_output
