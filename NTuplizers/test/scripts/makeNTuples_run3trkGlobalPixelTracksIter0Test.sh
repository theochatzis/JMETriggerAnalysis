#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "\n%s\n\n" ">>> argument missing - specify path to output directory"
  exit 1
fi

NEVT=50000

OUTDIR_ROOT=${1}
OUTDIR_JSON=${1}_json

if [ ! -d ${OUTDIR_JSON} ]; then

  mkdir -p ${OUTDIR_JSON}

  das_jsondump -p 1 -v -m ${NEVT} \
   -d /QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/MINIAODSIM \
   -o ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_15to3000_Flat_14TeV.json

  das_jsondump -p 1 -v -m ${NEVT} \
   -d /QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v2/MINIAODSIM \
   -o ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_50to80_14TeV.json

  das_jsondump -p 1 -v -m ${NEVT} \
   -d /QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v2/MINIAODSIM \
   -o ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_170to300_14TeV.json

  das_jsondump -p 1 -v -m ${NEVT} \
   -d /DYToLL_M-50_TuneCP5_14TeV-pythia8/Run3Winter20DRMiniAOD-DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/MINIAODSIM \
   -o ${OUTDIR_JSON}/Run3Winter20_DYToLL_M50_14TeV.json

  das_jsondump -p 1 -v -m ${NEVT} \
   -d /ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6-v3/MINIAODSIM \
   -o ${OUTDIR_JSON}/Run3Winter20_ZprimeToMuMu_M6000_14TeV.json

  das_jsondump -p 1 -v -m ${NEVT} \
   -d /VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v1/MINIAODSIM \
   -o ${OUTDIR_JSON}/Run3Winter20_VBF_HToInvisible_14TeV.json
fi

recos=(
  HLT
  HLT_globalPixelTracks_v01
)

for reco in "${recos[@]}"; do

  OUTDIR_ROOT=$1/${reco}

  if [ -d ${OUTDIR_ROOT} ]; then
    printf "%s\n" ">>> output directory already exists: ${OUTDIR_ROOT}"
    continue
  fi

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_15to3000_Flat_14TeV.json -p 1 \
   -o ${OUTDIR_ROOT}/Run3Winter20_QCD_Pt_15to3000_Flat_14TeV \
   -m ${NEVT} reco=${reco} trkdqm=1 pfdqm=1 globalTag=110X_mcRun3_2021_realistic_v6

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_50to80_14TeV.json -p 1 \
   -o ${OUTDIR_ROOT}/Run3Winter20_QCD_Pt_50to80_14TeV \
   -m ${NEVT} reco=${reco} trkdqm=1 pfdqm=1 globalTag=110X_mcRun3_2021_realistic_v6

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_170to300_14TeV.json -p 1 \
   -o ${OUTDIR_ROOT}/Run3Winter20_QCD_Pt_170to300_14TeV \
   -m ${NEVT} reco=${reco} trkdqm=1 pfdqm=1 globalTag=110X_mcRun3_2021_realistic_v6

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_DYToLL_M50_14TeV.json -p 1 \
   -o ${OUTDIR_ROOT}/Run3Winter20_DYToLL_M50_14TeV \
   -m ${NEVT} reco=${reco} trkdqm=1 pfdqm=1 globalTag=110X_mcRun3_2021_realistic_v6

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_ZprimeToMuMu_M6000_14TeV.json -p 1 \
   -o ${OUTDIR_ROOT}/Run3Winter20_ZprimeToMuMu_M6000_14TeV \
   -m ${NEVT} reco=${reco} trkdqm=1 pfdqm=1 globalTag=110X_mcRun3_2021_realistic_v6

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 2000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_VBF_HToInvisible_14TeV.json -p 1 \
   -o ${OUTDIR_ROOT}/Run3Winter20_VBF_HToInvisible_14TeV \
   -m ${NEVT} reco=${reco} trkdqm=1 pfdqm=1 globalTag=110X_mcRun3_2021_realistic_v6

  unset -v OUTDIR_ROOT

done
unset -v reco

unset -v NEVT OUTDIR_JSON
