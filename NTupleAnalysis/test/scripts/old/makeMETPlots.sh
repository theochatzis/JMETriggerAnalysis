#!/bin/bash

BKG_NoPU="${METANA_BASE}"/ntuples/191030_inclAging1000Fix/jmeTriggerNTuple_QCD_Pt_0_1000_14TeV_NoPU.root
BKG_PU200="${METANA_BASE}"/ntuples/191030_inclAging1000Fix/jmeTriggerNTuple_QCD_Pt_0_1000_14TeV_PU200_temp.root

SIG_NoPU="${METANA_BASE}"/ntuples/191030_inclAging1000Fix/jmeTriggerNTuple_VBF_HToInvisible_M125_14TeV_NoPU_temp.root
SIG_PU140="${METANA_BASE}"/ntuples/191030_inclAging1000Fix/jmeTriggerNTuple_VBF_HToInvisible_M125_14TeV_PU140.root
SIG_PU200="${METANA_BASE}"/ntuples/191030_inclAging1000Fix/jmeTriggerNTuple_VBF_HToInvisible_M125_14TeV_PU200.root

ODIR=output_191104

NEVT=100001

### ----------

#if [ -d ${ODIR} ]; then
#
#  printf "\n%s\n\n" " >> execution stopped --> target output directory already exists: ${ODIR}"
#  exit 1
#fi

"${METANA_BASE}"/metAnalysis.py -n ${NEVT} -i ${BKG_NoPU}  -o ${ODIR}/histos/Bkg/NoPU.root
"${METANA_BASE}"/metAnalysis.py -n ${NEVT} -i ${BKG_PU200} -o ${ODIR}/histos/Bkg/PU200.root

"${METANA_BASE}"/metAnalysis.py -n ${NEVT} -i ${SIG_NoPU}  -o ${ODIR}/histos/Sig/NoPU.root
"${METANA_BASE}"/metAnalysis.py -n ${NEVT} -i ${SIG_PU140} -o ${ODIR}/histos/Sig/PU140.root
"${METANA_BASE}"/metAnalysis.py -n ${NEVT} -i ${SIG_PU200} -o ${ODIR}/histos/Sig/PU200.root

if [ -d ${ODIR}/plots ]; then rm -rf ${ODIR}/plots; fi;

"${METANA_BASE}"/metPlots.py -l QCD_Pt_0_1000_14TeV --skip-GEN \
 --NoPU  ${ODIR}/histos/Bkg/NoPU.root \
 --PU200 ${ODIR}/histos/Bkg/PU200.root \
 -o ${ODIR}/plots/Bkg \
 -e png pdf root

"${METANA_BASE}"/metPlots.py -l VBF_H125ToInv_14TeV \
 --NoPU  ${ODIR}/histos/Sig/NoPU.root \
 --PU140 ${ODIR}/histos/Sig/PU140.root \
 --PU200 ${ODIR}/histos/Sig/PU200.root \
 -o ${ODIR}/plots/Sig \
 -e png pdf root

unset -v BKG_NoPU BKG_PU200
unset -v SIG_NoPU SIG_PU140 SIG_PU200
unset -v ODIR NEVT
