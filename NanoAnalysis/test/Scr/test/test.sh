#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh
export X509_USER_PROXY=/afs/cern.ch/user/y/yeo/tmp/x509up
voms-proxy-info -all
voms-proxy-info -all --file $1
cd /afs/cern.ch/user/y/yeo/rdf/24.09.30/JMETriggerAnalysis/NanoAnalysis/test
mkdir -p ./output/test
python3 Rdataframe.py -f ./input/test -i $1 -o output/test