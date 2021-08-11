#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  exit 1
fi

inpdir=${JMEANA_BASE}/output_200410_v03/harvesting
outdir=plots_phase2_200410_v03

samples=(
 Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200
# Phase2HLTTDR_VBF_HToInvisible_14TeV_NoPU
# Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
)

outdirbase=${outdir%%/*}

if [ ! -f ${outdirbase}.tar.gz ]; then

  for sample in "${samples[@]}"; do

    outd_i=${outdir}/${sample}

    opts_i=""
    if [[ ${sample} == *"QCD_"* ]]; then opts_i="-k *Jets* *MET*_pt"
    elif [[ ${sample} == *"ToInv"* ]]; then opts_i="-k *MET*"
    fi

    jmePlots_compareFiles.py ${opts_i} -u -o ${outd_i} -l ${sample} -e pdf root -i \
     ${inpdir}/hltPhase2_TRKv02/${sample}.root:'TRK v02':2:1:20 \
     ${inpdir}/hltPhase2_TRKv06/${sample}.root:'TRK v06':4:2:24

    jmePlots_compareFilesAndObjs.py ${opts_i} -u -o ${outd_i}/objs -l ${sample} -e pdf root -i \
     ${inpdir}/hltPhase2_TRKv02/${sample}.root:'TRK v02':2:1:20 \
     ${inpdir}/hltPhase2_TRKv06/${sample}.root:'TRK v06':4:2:24

    unset -v outd_i opts_i
  done
  unset -v sample

  if [ -d ${outdirbase} ]; then
    tar cfz ${outdirbase}.tar.gz ${outdirbase}
    rm -rf ${outdirbase}
  fi
fi

unset -v inpdir outdir samples outdirbase
