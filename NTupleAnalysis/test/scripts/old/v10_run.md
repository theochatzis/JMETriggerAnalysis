#!/bin/bash

#hadd_crab3.py -i ../output_v10_test50K/trkV2/* -o ntuples_prod_v10_test50K/trkV2
#hadd_crab3.py -i ../output_v10_test50K2/trkV2_skimmedTracks/* -o ntuples_prod_v10_test50K/trkV2_skimmedTracks
#hadd_crab3.py -i ../output_v10_test50K4/trkV2/* -o ntuples_prod_v10_test50K/trkV2_2
#hadd_crab3.py -i ../output_v10_test50K3/trkV2_skimmedTracks/* -o ntuples_prod_v10_test50K/trkV2_skimmedTracks_2

#batch_driver.py -s jmeAnalysis.py -i ntuples_prod_v10_test50K/trkV2/*root -o analysis_v10_test50K/trkV2/prod -n 5000
#batch_driver.py -s jmeAnalysis.py -i ntuples_prod_v10_test50K/trkV2_skimmedTracks/*root -o analysis_v10_test50K/trkV2_skimmedTracks/prod -n 5000

#merge_batchOutputs.py -i analysis_v10_test50K/trkV2/prod/*.root -o analysis_v10_test50K/trkV2/outputs
#merge_batchOutputs.py -i analysis_v10_test50K/trkV2_skimmedTracks/prod/*.root -o analysis_v10_test50K/trkV2_skimmedTracks/outputs

jmeAnalysisHarvester.py -i analysis_v10_test50K/trkV2/outputs/*.root -o analysis_v10_test50K/trkV2/outputs_postHarvesting
jmeAnalysisHarvester.py -i analysis_v10_test50K/trkV2_skimmedTracks/outputs/*.root -o analysis_v10_test50K/trkV2_skimmedTracks/outputs_postHarvesting
