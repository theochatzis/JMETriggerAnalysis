#!/bin/bash
set -e

# Extract file list from PSet.py
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

echo "Input files: $input_files"

# L1 step
cmsRun jmeTriggerNTuple_L1Only_cfg.py inputFiles=${input_files} output=L1_output.root

# HLT Step (makes custom JMETrigger NTuples)
cmsRun jmeTriggerNTuple_cfg.py inputFiles=file:L1_output.root

fi
