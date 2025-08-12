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
OUT_EOS_DIR="/DPNoteSubmitter/"
OUTPUT_FILE_NAME="data_batch"
SKIP_HARVEST=false
BATCH_SIZE=500   # Number of files to merge per batch

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
        --batch-size) # This is the ouput file name 
            BATCH_SIZE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--skip-harvest] [--out-dir DIR] [--output-file NAME] [--batch-size NUMBER OF FILES PER BATCH FOR HADD]"
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

# Find all .root files recursively and store in array
mapfile -t ROOT_FILES < <(find "${INPUT_DIR}" -type f -name "*.root")

if [ ${#ROOT_FILES[@]} -eq 0 ]; then
    echo "Error: No .root files found inside ${INPUT_DIR}"
    exit 1
fi

CORES=$(nproc)
echo "Using $CORES cores for hadd."

# Create temporary directory for batches
TMP_DIR="${INPUT_DIR}/tmp_batches"
mkdir -p "$TMP_DIR"

batch_files=()
batch_num=0

# Function to merge a batch of files
merge_batch() {
    local batch_file="$1"
    shift
    local files=("$@")
    echo "Merging batch ${batch_num} with ${#files[@]} files..."
    # hadd -j "$CORES" "$batch_file" "${files[@]}"
     hadd "$batch_file" "${files[@]}"
}

# Split input files into batches and merge each batch
for ((i=0; i<${#ROOT_FILES[@]}; i+=BATCH_SIZE)); do
    batch_file="${TMP_DIR}/batch_${batch_num}.root"
    batch_slice=("${ROOT_FILES[@]:i:BATCH_SIZE}")
    merge_batch "$batch_file" "${batch_slice[@]}"
    batch_files+=("$batch_file")
    ((batch_num++))
done

# Merge all batch files into the final output file
echo "Merging ${#batch_files[@]} batch files into final output: ${INPUT_DIR}/${OUTPUT_FILE_NAME}.root"
#hadd -j "$CORES" "${INPUT_DIR}/${OUTPUT_FILE_NAME}.root" "${batch_files[@]}"
hadd "${INPUT_DIR}/${OUTPUT_FILE_NAME}.root" "${batch_files[@]}"

# Clean up batch files
rm -rf "$TMP_DIR"

# Harvest step
if [ "$SKIP_HARVEST" = true ]; then
    echo "Skipping harvesting step."
else
    echo "Harvesting..."
    jmeAnalysisHarvester.py -l 0 -i "${INPUT_DIR}/${OUTPUT_FILE_NAME}.root" -o "${INPUT_DIR}/harvesting"
fi
