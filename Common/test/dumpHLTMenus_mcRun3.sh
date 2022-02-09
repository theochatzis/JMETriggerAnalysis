#!/bin/bash -e

hltGetConfiguration /dev/CMSSW_12_3_0/GRun \
 --full \
 --offline \
 --unprescale \
 --process HLTX \
 --globaltag auto:run3_mc_GRun \
 --input /store/mc/Run3Winter21DRMiniAOD/SinglePion_PT0to200/GEN-SIM-DIGI-RAW/NoPUFEVT_112X_mcRun3_2021_realistic_v16-v2/140000/53fc39b0-c12c-419f-ba73-78c4d032ff3e.root \
 --mc \
 --max-events 10 \
 > tmp.py

edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_12_3_0_GRun_configDump.py
rm -f tmp.py
