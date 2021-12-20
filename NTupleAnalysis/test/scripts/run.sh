#!/bin/bash

#for nnn in 0 1 2; do
#  batch_driver.py \
#   -n 50000 -l 1 -p JMETriggerAnalysisDriverPhase2 \
#   -i output_hltPhase2_200717_PuppiMod${nnn}_v01/ntuples/*/*.root \
#   -o output_hltPhase2_200717_PuppiMod${nnn}_v01/jobs
#done
#unset nnn

#for nnn in 0 1 2; do
#  merge_batchOutputs.py  -l 1 \
#    -i output_hltPhase2_200717_PuppiMod${nnn}_v01/jobs/*/*.root \
#    -o output_hltPhase2_200717_PuppiMod${nnn}_v01/outputs
#done
#unset nnn

for nnn in 0 1 2; do
  jmeAnalysisHarvester.py -l 1 \
    -i output_hltPhase2_200717_PuppiMod${nnn}_v01/outputs/*/*.root \
    -o output_hltPhase2_200717_PuppiMod${nnn}_v01/harvesting
done
unset nnn
