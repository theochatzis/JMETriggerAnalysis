#!/bin/bash
source env.sh

# directory with input(s) 
INPDIR=/eos/user/a/aakpinar/nanopost/hlt_run3_JECs

mkdir -p ${INPDIR}/samples_merged/QCD_FlatPUGTv6HCAL_126X_withForwardPFHCs
mkdir -p ${INPDIR}/samples_merged/QCD_EpsPUGTv6HCAL_126X_withForwardPFHCs

# QCD flat PU sample
hadd_ntuples.py -i ${INPDIR}/QCD_FlatPUGTv6HCAL_126X_withForwardPFHCs/QCD_PT-15to7000_TuneCP5_Flat2022_13p6TeV_pythia8/crab_jmeTriggerNTuple_QCD_FlatPUGTv6HCAL_126X_withForwardPFHCs/230802_122038/0000 \
-o ${INPDIR}/samples_merged/QCD_FlatPUGTv6HCAL_126X_withForwardPFHCs -l 0

# QCD epsilon PU sample
hadd_ntuples.py -i ${INPDIR}/QCD_EpsPUGTv6HCAL_126X_withForwardPFHCs/QCD_PT-15to7000_TuneCP5_Flat2022_13p6TeV_pythia8/crab_jmeTriggerNTuple_QCD_EpsPUGTv6HCAL_126X_withForwardPFHCs/230802_121934/0000 \
-o ${INPDIR}/samples_merged/QCD_EpsPUGTv6HCAL_126X_withForwardPFHCs -l 0



