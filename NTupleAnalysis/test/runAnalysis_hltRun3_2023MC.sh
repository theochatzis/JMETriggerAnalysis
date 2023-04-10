#!/bin/bash
source env.sh

# directory with input JMETriggerNTuple(s)
INPDIR=/eos/user/t/tchatzis/samples2023/test_ntuples/HLT_Run3TRK/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65

# directory with outputs of NTupleAnalysis
OUTDIR=QCD_2023MC
OUTPUTDIR=QCD_2023MC

mkdir -p ${OUTDIR}
[ -d ${OUTDIR}/ntuples ] || (ln -sf ${INPDIR} ${OUTDIR}/ntuples)

batch_driver.py -l 1 -n 5000 -p JMETriggerAnalysisDriverRun3 \
 -i ${OUTDIR}/ntuples/*.root -o ${OUTDIR}/jobs \
 -od ${OUTPUTDIR} \
 --JobFlavour espresso

batch_monitor.py -i ${OUTDIR}/jobs -r --repe -f 900

merge_batchOutputs.py -l 1 -i ${OUTPUTDIR}/*.root -o ${OUTPUTDIR}/outputs

NUM_PROC=$(nproc)
if [[ ${HOSTNAME} == lxplus* ]]; then NUM_PROC=2; fi;
for rootfile_i in ${OUTPUTDIR}/outputs/*/*.root; do
  while [ $(jobs -p | wc -l) -ge ${NUM_PROC} ]; do sleep 5; done
  echo ${rootfile_i}
  jmeAnalysisHarvester.py -l 1 -i ${rootfile_i} -o ${OUTPUTDIR}/harvesting || true &
done
unset rootfile_i

jobs
wait || true

#rm -rf ${OUTDIR}/outputs

