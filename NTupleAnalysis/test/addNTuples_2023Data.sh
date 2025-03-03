#!/bin/bash
source env.sh

# directory with input(s) 
INPDIR=/eos/user/t/tchatzis/samples2023/test_trk25
POSTFIX=_qcd
recoKeys=(
    default
    ca_mkfit
    ca_mkfit_bpixl1
)

for recoKey in "${recoKeys[@]}"; do
    mkdir -p ${INPDIR}/${recoKey}/samples_merged${POSTFIX}

    hadd_ntuples.py -i ${INPDIR}/${recoKey}/QCD_Bin-Pt-15to7000_TuneCP5_13p6TeV_pythia8/out_*0* \
    -o ${INPDIR}/${recoKey}/samples_merged${POSTFIX} -l 0
done



