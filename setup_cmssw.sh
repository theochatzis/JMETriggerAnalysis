#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#

scram project CMSSW_12_2_0_pre2
cd CMSSW_12_2_0_pre2/src
eval `scram runtime -sh`

git cms-init --ssh
git cms-merge-topic silviodonato:customizeHLTforRun3_v2

git clone git@github.com:missirol/JMETriggerAnalysis.git -o missirol -b run3
git clone git@github.com:missirol/JetMETAnalysis.git -o missirol -b devel_hlt2

# external data
mkdir -p ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/data

# PFHC: preliminary HLT-PFHC for Run 3
scp missirol@lxplus.cern.ch:/afs/cern.ch/work/m/missirol/public/run3/PFHC/PFHC_Run3Winter20_HLT_v01.db \
  ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/data/PFHC_Run3Winter20_HLT_v01.db

# JESC: preliminary HLT-JESCs for Run 3
scp missirol@lxplus.cern.ch:/afs/cern.ch/work/m/missirol/public/run3/JESC/Run3Winter20_V2_MC/Run3Winter20_V2_MC.db \
  ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter20_V2_MC.db

scram b -j 8
