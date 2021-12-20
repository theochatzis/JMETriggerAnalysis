#!/bin/bash

if [ $# -ne 1 ]; then
  exit 1
fi

set -e

if [ ! -f CF9E9002-A7D9-EB40-A182-AB1D7A508721.root ]; then
  xrdcp root://cms-xrd-global.cern.ch//store/relval/CMSSW_11_2_0_pre3/RelValQCD_FlatPt_15_3000HS_14/GEN-SIM-DIGI-RAW/PU_112X_mcRun3_2021_realistic_v5-v1/20000/CF9E9002-A7D9-EB40-A182-AB1D7A508721.root .
fi

cmsDriver.py step2 \
--filein file:CF9E9002-A7D9-EB40-A182-AB1D7A508721.root \
--mc \
--datatier AODSIM \
--conditions 112X_mcRun3_2021_realistic_v7 \
--step RAW2DIGI,RECO,RECOSIM \
--eventcontent AODSIM \
--nThreads 1 \
--geometry DB:Extended \
--era Run3 \
--python_filename testPuppiInRECO_mcRun3_cfg.py \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--customise JMETriggerAnalysis/NTuplizers/customise_reco.customise_addPuppiNTupleToRECO \
--customise HLTrigger/Timer/FastTimer.customise_timer_service_print \
--customise_commands "process.TFileService = cms.Service('TFileService', fileName = cms.string('$1'))" \
-n 10

#--customise_commands "process.schedule.remove(process.AODSIMoutput_step)\ndel process.AODSIMoutput\ndel process.AODSIMoutput_step\nprocess.TFileService = cms.Service('TFileService', fileName = cms.string('$1'))" \
