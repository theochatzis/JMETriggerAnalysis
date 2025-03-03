#!/bin/bash
source env.sh

# directory with input JMETriggerNTuple(s)
INPDIR=/eos/cms/store/user/chuh/jec/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8
INPFILE=QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8

# directory with outputs of NTupleAnalysis
OUTDIR=Run3_QCD
OUTPUTDIR=/afs/cern.ch/user/c/chuh/work/PFHadCalibration/CMSSW_13_0_0/src/JMETriggerAnalysis/NTupleAnalysis/test/

merge_batchOutputs.py -l 1 -i ${OUTPUTDIR}/*.root -o ${OUTPUTDIR}/outputs
rm -rf ${OUTDIR}/jobs

NUM_PROC=$(nproc)
if [[ ${HOSTNAME} == lxplus* ]]; then NUM_PROC=3; fi;
for rootfile_i in ${OUTPUTDIR}/outputs/*/*.root; do
  while [ $(jobs -p | wc -l) -ge ${NUM_PROC} ]; do sleep 5; done
  jmeAnalysisHarvester.py -l 1 -i ${rootfile_i} -o ${OUTPUTDIR}/harvesting || true &
done
unset rootfile_i

jobs
wait || true

jmePlots.py -i ${OUTPUTDIR}/harvesting/test/${INPFILE}.root:'[JESCs Apr23]':600:1:24 -o ${OUTPUTDIR}/${INPFILE} -k trig_review_2023

rm -rf outputs *root
