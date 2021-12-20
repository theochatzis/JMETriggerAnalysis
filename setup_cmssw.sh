#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#

scram project CMSSW_12_0_0_pre4
cd CMSSW_12_0_0_pre4/src
eval `scram runtime -sh`
git cms-merge-topic missirol:devel_hltRun3TRK_1200pre4
