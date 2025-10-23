#!/bin/bash
set -e

echo "Extracting input files from PSet.py..."
input_files=$(python3 - <<'EOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("PSet", "PSet.py")
PSet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PSet)
try:
    print(','.join(PSet.process.source.fileNames))
except Exception as e:
    print(f"ERROR: could not read input files: {e}", file=sys.stderr)
    sys.exit(1)
EOF
)

out_file=$(python3 - <<'EOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("PSet", "PSet.py")
PSet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PSet)
try:
    print(PSet.process.output.fileName.value())
except Exception as e:
    print(f"ERROR: could not find output fileName: {e}", file=sys.stderr)
    sys.exit(1)
EOF
)

echo "Input files: $input_files"
echo "Output file from PSet: $out_file"

events_per_chunk=5 # 10 events correspond to roughly 110 MB with the skimming of L1 Output (CRAB has max at 120MB disk)

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
            skipEvents=$skip maxEvents=$events_per_chunk output=L1_output.root monitorMemory=True
    )

    (
        cmsRun jmeTriggerNTuple_cfg.py inputFiles=file:L1_output.root output=HLT_chunk_${chunk_index}.root  monitorMemory=True
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
hadd -f $out_file HLT_chunk_*.root
rm -f HLT_chunk_*.root
