#!/bin/bash

if [ $# -ne 1 ]; then
  exit 1
fi

set -e

if [ ! -f AD9E7150-CC61-EF45-A9D6-463BA4273E44.root ]; then
  xrdcp root://cms-xrd-global.cern.ch//store/relval/CMSSW_11_2_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU25ns_110X_mcRun4_realistic_v3_2026D49PU200_rsb-v1/20000/AD9E7150-CC61-EF45-A9D6-463BA4273E44.root .
fi

cmsDriver.py step2 \
--filein file:AD9E7150-CC61-EF45-A9D6-463BA4273E44.root \
--mc \
--datatier AODSIM \
--conditions auto:phase2_realistic_T15 \
--step RAW2DIGI,RECO,RECOSIM \
--eventcontent AODSIM \
--nThreads 1 \
--geometry Extended2026D49 \
--era Phase2C9 \
--python_filename testPuppiInRECO_mcRun4_cfg.py \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000 \
--customise JMETriggerAnalysis/NTuplizers/customise_reco.customise_addPuppiNTupleToRECO \
--customise HLTrigger/Timer/FastTimer.customise_timer_service_print \
--customise_commands "process.TFileService = cms.Service('TFileService', fileName = cms.string('$1'))" \
-n 10

#--customise_commands "process.schedule.remove(process.AODSIMoutput_step)\ndel process.AODSIMoutput\ndel process.AODSIMoutput_step\nprocess.TFileService = cms.Service('TFileService', fileName = cms.string('$1'))" \
