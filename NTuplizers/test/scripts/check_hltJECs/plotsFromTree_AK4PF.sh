#!/bin/bash

set -e

python -B histosFromTree_AK4PF.py output_run3_checkJECs_v0 10
python -B histosFromTree_AK4PF.py output_run3_checkJECs_v1 10

rm -rf tmpout

../../../NTupleAnalysis/JMETrigger/test/test/compareHistos.py \
  -i output_run3_checkJECs_v0.root:'Before Fix (2016 HLT-JECs)':1 \
     output_run3_checkJECs_v1.root:'After Fix (2017 HLT-JECs)':2 \
  -o tmpout \
  -l '[Run3Winter20] QCD_Pt15-3000_Flat' \
  -e pdf root \
  -k None
