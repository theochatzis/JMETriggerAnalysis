#!/bin/bash
source env.sh

OUT_EOS_DIR=/samples2023/DPNote2023/
OUTPUT_FILE_NAME=data


FIRST_USER_LETTER=${USER:0:1}

# directory with input JMETriggerNTuple(s)
INPUT_DIR="/eos/user/${FIRST_USER_LETTER}/${USER}${OUT_EOS_DIR}"

## Merge Jobs with hadd
echo "merging jobs outputs..."
hadd ${INPUT_DIR}/${OUTPUT_FILE_NAME}.root ${INPUT_DIR}/*.root

## Harvest i.e. create responses, matching efficiency etc
echo "harvesting..."
jmeAnalysisHarvester.py -l 0 -i ${INPUT_DIR}/${OUTPUT_FILE_NAME}.root -o ${INPUT_DIR}/harvesting
