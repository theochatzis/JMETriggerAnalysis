#!/bin/bash
source env.sh

# directory with input(s) 
INPDIR=/eos/user/t/tchatzis/samples2023/test_dataG_2023eta2p4
recoKeys=(
    #default
    hcal_jecs2023
    #hcal_jecs2023
)

for recoKey in "${recoKeys[@]}"; do
    mkdir -p ${INPDIR}/${recoKey}/samples_merged

    hadd_ntuples.py -i ${INPDIR}/${recoKey}/data \
    -o ${INPDIR}/${recoKey}/samples_merged -l 0
done



