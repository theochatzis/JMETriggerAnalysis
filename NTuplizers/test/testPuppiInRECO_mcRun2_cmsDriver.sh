#!/bin/bash

if [ $# -ne 1 ]; then
  exit 1
fi

set -e

if [ ! -f EF03FD1C-C1C3-C84E-ADEF-5067054B19EC.root ]; then
  xrdcp root://cms-xrd-global.cern.ch//store/relval/CMSSW_10_6_14_Pyt8240BugFix/RelValQCD_FlatPt_15_3000HS_13/GEN-SIM-RECO/PU25ns_106X_mc2017_realistic_v7_HS-v1/10000/EF03FD1C-C1C3-C84E-ADEF-5067054B19EC.root .
fi

cmsDriver.py step2 \
--filein file:EF03FD1C-C1C3-C84E-ADEF-5067054B19EC.root \
--mc \
--datatier MINIAODSIM \
--conditions 106X_mc2017_realistic_v7 \
--step PAT \
--runUnscheduled \
--eventcontent MINIAODSIM \
--nThreads 1 \
--geometry DB:Extended \
--era Run2_2017 \
--python_filename testPuppiInRECO_mcRun2_cfg.py \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--customise JMETriggerAnalysis/NTuplizers/customise_reco.customise_addPuppiNTupleToRECO \
--customise HLTrigger/Timer/FastTimer.customise_timer_service_print \
--customise_commands "process.TFileService = cms.Service('TFileService', fileName = cms.string('$1'))" \
-n 500

#--customise_commands "process.schedule.remove(process.AODSIMoutput_step)\ndel process.AODSIMoutput\ndel process.AODSIMoutput_step\nprocess.TFileService = cms.Service('TFileService', fileName = cms.string('$1'))" \
