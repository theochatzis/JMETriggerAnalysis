#!/bin/bash
base_dir=/eos/user/t/tchatzis/JRA_NTuples_Winter24/ 
# Define lists
bpix_categories=("BPix" "BPixPlus" "BPixMinus" "noBPix")
samples_labels=("FlatPU0to80" "NoPU")

# Double loop over the lists
for bpix_category in "${bpix_categories[@]}"; do
    for sample_label in "${samples_labels[@]}"; do
        dir_name="JRA_${sample_label}${bpix_category}"
        echo "adding samples from $dir_name : "
        hadd "$base_dir/$dir_name.root" `ls -u $base_dir/$dir_name/QCD*/crab*/*/*/*.root`
    done
done
