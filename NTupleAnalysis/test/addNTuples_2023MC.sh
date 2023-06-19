#!/bin/bash
source env.sh

# directory with input(s) 
INPDIR=/eos/user/t/tchatzis/samples2023/test_noCustom

mkdir -p ${INPDIR}/HLT_Run3TRK/samples_merged

# QCD
hadd_ntuples.py -i ${INPDIR}/HLT_Run3TRK/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65 \
-o ${INPDIR}/HLT_Run3TRK/samples_merged -l 0

# VBF HToInvisible
hadd_ntuples.py -i ${INPDIR}/HLT_Run3TRK/Run3Winter23_VBF_HToInvisible_13p6TeV_PU65 \
-o ${INPDIR}/HLT_Run3TRK/samples_merged -l 0



