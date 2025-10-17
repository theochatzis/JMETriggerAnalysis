#this is not meant to be run locally
#

input_list=$1
echo "Input file list: $input_list"
cat $input_list

# L1 Step
cmsRun jmeTriggerNTuple_L1Only_cfg.py inputFiles=$(cat $input_list | tr '\n' ',')

# HLT Step (makes custom JMETrigger NTuples)
cmsRun jmeTriggerNTuple_cfg.py inputFiles=file:L1_output.root

fi
