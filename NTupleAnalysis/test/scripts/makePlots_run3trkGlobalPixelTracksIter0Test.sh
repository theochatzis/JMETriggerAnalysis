#!/bin/bash

set -e

if [ ! -d ${JMEANA_BASE} ]; then
  exit 1
fi

inpdir=${JMEANA_BASE}/output_run3trkGlobalPixelTracksIter0Test_v07
outdir=plots_run3trkGlobalPixelTracksIter0Test_v07

samples=(
  Run3Winter20_QCD_Pt_15to3000_Flat_14TeV
  Run3Winter20_QCD_Pt_50to80_14TeV
  Run3Winter20_QCD_Pt_170to300_14TeV
  Run3Winter20_DYToLL_M50_14TeV
  Run3Winter20_ZprimeToMuMu_M6000_14TeV
  Run3Winter20_VBF_HToInvisible_14TeV
)

outdirbase=${outdir%%/*}

if [ ! -f ${outdirbase}.tar.gz ] && [ ! -d ${outdirbase} ]; then

  for sample in "${samples[@]}"; do

    outd_i=${outdir}/run2_vs_iter0withPatatrack/${sample}

    opts_i=""
    if   [[ ${sample} == *"QCD_"* ]]; then opts_i="-k '*Jets*' '*MET_pt' '*/offlineMETs*_pt'"
    elif [[ ${sample} == *"DYToLL"* ]]; then opts_i="-k '*MET_*' '*/offlineMETs*_pt'"
    elif [[ ${sample} == *"ZprimeToMuMu"* ]]; then opts_i="-k '*METNoMu_*'"
    elif [[ ${sample} == *"HToInv"* ]]; then opts_i="-k '*MET_*' '*/offlineMETs*_pt'"
    fi

    dqmPlots_compareFiles.py -o ${outd_i}/dqm -l ${sample} -e pdf root -i \
      ${inpdir}/ntuples/HLT/${sample}.root:'Run-2':1:1:20 \
      ${inpdir}/ntuples/HLT_globalPixelTracks_v01/${sample}.root:'Patatrack PixTrk + Iter-0':2:1:24

    if [ ${sample} == "Run3Winter20_QCD_Pt_15to3000_Flat_14TeV" ]; then
      dqmPlots_compareObjs.py -o ${outdir}/run2/${sample}/dqm_compareObjs -l ${sample} -e pdf root -i \
        ${inpdir}/ntuples/HLT/${sample}.root:'':1:1:20

      dqmPlots_compareFilesAndObjs.py -o ${outd_i}/dqm_compareObjs -l ${sample} -e pdf root -i \
        ${inpdir}/ntuples/HLT/${sample}.root:'Run-2':1:1:20 \
        ${inpdir}/ntuples/HLT_globalPixelTracks_v01/${sample}.root:'Patatrack PixTrk + Iter-0':2:2:24
    fi

    jmePlots_compareFiles.py ${opts_i} -o ${outd_i}/jme -l ${sample} -e pdf root -i \
      ${inpdir}/harvesting/HLT/${sample}.root:'Run-2':1:1:20 \
      ${inpdir}/harvesting/HLT_globalPixelTracks_v01/${sample}.root:'Patatrack PixTrk + Iter-0':2:1:24

    jmePlots_compareObjs.py ${opts_i} -o ${outdir}/run2/${sample}/jme_compareObjs -l ${sample} -e pdf root -i \
      ${inpdir}/harvesting/HLT/${sample}.root:'':1:1:20

    jmePlots_compareFilesAndObjs.py ${opts_i} -o ${outd_i}/jme_compareObjs -l ${sample} -e pdf root -i \
      ${inpdir}/harvesting/HLT/${sample}.root:'Run-2':1:1:20 \
      ${inpdir}/harvesting/HLT_globalPixelTracks_v01/${sample}.root:'Patatrack PixTrk + Iter-0':2:2:24

    unset -v outd_i opts_i
  done
  unset -v sample

  if [ -d ${outdirbase} ]; then
    tar cfz ${outdirbase}.tar.gz ${outdirbase}
    rm -rf ${outdirbase}
  fi
fi

unset -v inpdir outdir samples outdirbase
