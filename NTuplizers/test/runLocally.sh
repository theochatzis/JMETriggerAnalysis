#!/bin/bash -e

# Run first the L1 step (note : very very big file output... ~100MB/Evt )
cmsRun jmeTriggerNTuple_L1Only_cfg.py maxEvents=5 skipEvents=5 output=L1_output.root

# HLT step with analyser that producer JMETrigger NTuple tree structure.
cmsRun jmeTriggerNTuple_cfg.py inputFiles=file:L1_output.root

# Remove the large FEVTDEBUGHLT outputs
# rm Phase2*HLT.root
# rm L1_output.root

