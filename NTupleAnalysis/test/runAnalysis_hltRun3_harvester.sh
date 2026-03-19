#!/bin/bash
source env.sh
# ______                       _   _____                  _   
# | ___ \                     | | |_   _|                | |  
# | |_/ /_ _ _ __ ___  ___  __| |   | | _ __  _ __  _   _| |_ 
# |  __/ _` | '__/ __|/ _ \/ _` |   | || '_ \| '_ \| | | | __|
# | | | (_| | |  \__ \  __/ (_| |  _| || | | | |_) | |_| | |_ 
# \_|  \__,_|_|  |___/\___|\__,_|  \___/_| |_| .__/ \__,_|\__|
#                                            | |              
#                                            |_|              
# Default values
OUT_EOS_DIR=/HFscaleDec01/HFscale26Nov2025evaluation_2025Dec01_Muon0_HFscaleNov2025/ #"/DPNoteSubmitter/"
OUTPUT_FILE_NAME="data"
SKIP_HARVEST=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-harvest) # Skip the harvesting step. This step is needed only if you want to make Graphs of efficiency, response etc. If histos is all you need can skip it.
            SKIP_HARVEST=true
            shift
            ;;
        --out-dir) # This is the directory that you will use as base for your output.
            OUT_EOS_DIR="$2"
            shift 2
            ;;
        --output-file) # This is the ouput file name 
            OUTPUT_FILE_NAME="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--skip-harvest] [--out-dir DIR] [--output-file NAME]"
            exit 1
            ;;
    esac
done

FIRST_USER_LETTER=${USER:0:1}

# Directory with input files from submitter step
INPUT_DIR="/eos/user/${FIRST_USER_LETTER}/${USER}${OUT_EOS_DIR}"

#   ___      _     _   _   _ _   _   _                           _   
#  / _ \    | |   | | | \ | ( ) | | | |                         | |  
# / /_\ \ __| | __| | |  \| |/  | |_| | __ _ _ ____   _____  ___| |_ 
# |  _  |/ _` |/ _` | | . ` |   |  _  |/ _` | '__\ \ / / _ \/ __| __|
# | | | | (_| | (_| | | |\  |   | | | | (_| | |   \ V /  __/\__ \ |_ 
# \_| |_/\__,_|\__,_| \_| \_/   \_| |_/\__,_|_|    \_/ \___||___/\__|

echo "Searching for ROOT files in: ${INPUT_DIR} ..."

# Find all .root files recursively
ROOT_FILES=$(find "${INPUT_DIR}" -type f -name "*.root")

if [ -z "${ROOT_FILES}" ]; then
    echo "Error: No .root files found inside ${INPUT_DIR}"
    exit 1
fi

## Merge Jobs with hadd
echo "Merging all ROOT files into: ${INPUT_DIR}/${OUTPUT_FILE_NAME}.root"
hadd -j 8 "${INPUT_DIR}/${OUTPUT_FILE_NAME}.root" $ROOT_FILES

## Harvest i.e. create responses, matching efficiency etc
if [ "$SKIP_HARVEST" = true ]; then
    echo "Skipping harvesting step."
else
    echo "Harvesting..."
    jmeAnalysisHarvester.py -l 0 -i "${INPUT_DIR}/${OUTPUT_FILE_NAME}.root" -o "${INPUT_DIR}/harvesting"
fi
