#!/bin/bash
base_dir=/eos/user/${USER:0:1}/${USER}/JRA_NTuples/ 
# Define lists
bpix_categories=("BPix" "FPix" "noBPix")
samples_labels=("FlatPU0to80" "NoPU")

# Double loop over the lists
for bpix_category in "${bpix_categories[@]}"; do
    for sample_label in "${samples_labels[@]}"; do
        dir_name="JRA_${sample_label}${bpix_category}"
        echo "adding samples from $dir_name : "
        hadd "$base_dir/$dir_name.root" `ls -u $base_dir/$dir_name/QCD*/crab*/*/*/*.root`
    done
done
