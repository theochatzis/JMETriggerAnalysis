#!/bin/bash
source env.sh

# directory with input(s) 
#INPDIR=/eos/user/t/tchatzis/CoffteaNTuples/muon2023C_CoffteaNTuple
INPDIR=/eos/user/t/tchatzis/samples2023/test_Zmu_default/HLT_Run3TRK

recoKeys=(
    HLT_Run3TRK
    #default
    #option5
    #option3
)

for recoKey in "${recoKeys[@]}"; do
    mkdir -p ${INPDIR}/samples_merged

    hadd_ntuples.py -i ${INPDIR}/data \
    -o ${INPDIR}/samples_merged -l 0
done



