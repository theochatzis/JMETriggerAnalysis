#!/bin/bash

#
# recipe to set up local CMSSW area
#
# Notes:
#  - do not use aliases (e.g. cmsrel, cmsenv),
#    so that the recipe can also work in non-interactive shells
#  - do not compile with scram inside this script
#
scramv1 project CMSSW CMSSW_11_1_8
cd CMSSW_11_1_8/src
eval `scramv1 runtime -sh`

git cms-merge-topic cms-sw:32903

# [optional; required only for PF-Hadron calibrations]
# workaround for PFSimParticle::trackerSurfaceMomentum
# ref: hatakeyamak:FBaseSimEvent_ProtectAgainstMissingTrackerSurfaceMomentum
git cms-addpkg FastSimulation/Event
git remote add hatakeyamak https://github.com/hatakeyamak/cmssw.git
git fetch hatakeyamak
git diff 0cf67551731c80dc85130e4b8ec73c8f44d53cb0^ 0cf67551731c80dc85130e4b8ec73c8f44d53cb0 | git apply

# [optional; required only for JME-Trigger NTuple]
mkdir -p HLTrigger
git clone https://github.com/veelken/mcStitching.git HLTrigger/mcStitching

# [optional; required only for JME-Trigger NTuple workflow with 'pvdqm > 1']
# analyzer for primary vertices (courtesy of W. Erdmann)
git clone https://github.com/missirol/PVAnalysis.git usercode -o missirol -b phase2
