#!/bin/bash
source env.sh

# directory with input JMETriggerNTuple(s)
INPDIR=/eos/cms/store/group/phys_jetmet/pdas/test_2018data/ntuple/

# directory with outputs of NTupleAnalysis
OUTDIR=test_2018data
OUTPUTDIR=/eos/cms/store/group/phys_jetmet/pdas/test_2018data/test_outputs/

mkdir -p ${OUTDIR}
[ -d ${OUTDIR}/ntuples ] || (ln -sf ${INPDIR} ${OUTDIR}/ntuples)

batch_driver.py -l 1 -n 5000 -p JMETriggerAnalysisDriverRun3 \
 -i ${OUTDIR}/ntuples/*.root -o ${OUTDIR}/jobs \
 -od ${OUTPUTDIR} \
 --JobFlavour longlunch

batch_monitor.py -i ${OUTDIR}/jobs -r --repe -f 900

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

rm -rf ${OUTDIR}/outputs
