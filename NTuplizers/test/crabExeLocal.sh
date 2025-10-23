#!/bin/bash
set -e

input_files=/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_AllTP_140X_mcRun4_realistic_v4-v1/2560000/086c6a16-9e7c-455e-83e4-96a0fee12bfb.root

events_per_chunk=5 # 10 events correspond to roughly 110 MB with the skimming of L1 Output (CRAB has max at 120MB disk)
out_file="out.root"

# Make sure input_files is readable remotely
input_files=$(echo "$input_files" | sed 's#^/store/#root://xrootd-cms.infn.it//store/#')

echo "Input files after adding XROOTD: $input_files"

# Determine total number of events from ROOT file
echo "Counting total events using edmEventSize..."
total_events=$(edmEventSize -v ${input_files%%,*} 2>/dev/null | awk '/Events / {print $NF; exit}')

echo "Total Events: $total_events"

skip=0
chunk_index=0

while [ $skip -lt $total_events ]; do
    echo ">>> Processing chunk: skipEvents=$skip  maxEvents=$events_per_chunk"
    (
        cmsRun jmeTriggerNTuple_L1Only_cfg.py inputFiles=${input_files} \
            skipEvents=$skip maxEvents=$events_per_chunk output=L1_output.root
    )

    (
        cmsRun jmeTriggerNTuple_cfg.py inputFiles=file:L1_output.root output=HLT_chunk_${chunk_index}.root
    )

    rm -f L1_output.root  # free disk space quickly

    echo "Chunk $chunk_index completed. Checking memory usage..."
    grep VmRSS /proc/$$/status || true

    # Give the OS a moment
    #sleep 10
    skip=$((skip + events_per_chunk))
    chunk_index=$((chunk_index + 1))
done

echo "Merging all chunks..."
hadd -f out.root HLT_chunk_*.root
rm -f HLT_chunk_*.root
