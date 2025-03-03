#!/bin/bash

set -e

if [ $# -lt 1 ]; then
  printf "%s\n" ">>> argument missing - specify path to output directory"
  exit 1
fi

NEVT=50000

OUTDIR_ROOT=${1}
OUTDIR_JSON=${1}_json

if [ ! -d ${OUTDIR_JSON} ]; then

  mkdir -p ${OUTDIR_JSON}

  das_jsondump -v -m ${NEVT} \
   -d /QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/GEN-SIM-RAW \
   -o ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_15to3000_Flat_14TeV.json

  das_jsondump -v \
   -d /QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v2/GEN-SIM-RAW \
   -o ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_50to80_14TeV.json

  das_jsondump -v \
   -d /QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Run3Winter20DRPremixMiniAOD-110X_mcRun3_2021_realistic_v6-v2/GEN-SIM-RAW \
   -o ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_170to300_14TeV.json

  das_jsondump -v -m ${NEVT} \
   -d /DYToLL_M-50_TuneCP5_14TeV-pythia8/Run3Winter20DRMiniAOD-DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/GEN-SIM-RAW \
   -o ${OUTDIR_JSON}/Run3Winter20_DYToLL_M50_14TeV.json

  das_jsondump -v -m ${NEVT} \
   -d /ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6-v3/GEN-SIM-RAW \
   -o ${OUTDIR_JSON}/Run3Winter20_ZprimeToMuMu_M6000_14TeV.json
fi

recos=(
  HLT
  HLT_pfBlockAlgoRemovePS
  HLT_trkIter2RegionalPtSeed0p9
  HLT_trkIter2RegionalPtSeed2p0
  HLT_trkIter2RegionalPtSeed5p0
  HLT_trkIter2RegionalPtSeed10p0
  HLT_trkIter2GlobalPtSeed0p9
)

for reco in "${recos[@]}"; do

  OUTDIR_ROOT=$1/${reco}

  if [ -d ${OUTDIR_ROOT} ]; then
    printf "%s\n" ">>> output directory already exists: ${OUTDIR_ROOT}"
    continue
  fi

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_15to3000_Flat_14TeV.json -p 0 \
   -o ${OUTDIR_ROOT}/Run3Winter20_QCD_Pt_15to3000_Flat_14TeV \
   -m ${NEVT} reco=${reco}

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_50to80_14TeV.json -p 0 \
   -o ${OUTDIR_ROOT}/Run3Winter20_QCD_Pt_50to80_14TeV \
   -m ${NEVT} reco=${reco}

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_QCD_Pt_170to300_14TeV.json -p 0 \
   -o ${OUTDIR_ROOT}/Run3Winter20_QCD_Pt_170to300_14TeV \
   -m ${NEVT} reco=${reco}

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_DYToLL_M50_14TeV.json -p 0 \
   -o ${OUTDIR_ROOT}/Run3Winter20_DYToLL_M50_14TeV \
   -m ${NEVT} reco=${reco}

  htc_driver -c jmeTriggerNTuple_cfg.py -n 2000 numThreads=1 --cpus 1 --memory 3000 --runtime 10800 \
   -d ${OUTDIR_JSON}/Run3Winter20_ZprimeToMuMu_M6000_14TeV.json -p 0 \
   -o ${OUTDIR_ROOT}/Run3Winter20_ZprimeToMuMu_M6000_14TeV \
   -m ${NEVT} reco=${reco}

  unset -v OUTDIR_ROOT

done
unset -v reco

unset -v NEVT OUTDIR_JSON
