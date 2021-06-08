#!/bin/bash

# directory with input JMETriggerNTuple(s)
INPDIR=/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/JetMET_PhaseII/JMETriggerAnalysis_run3/ntuples/hltRun3_testTRK_210604/HLT_GRun/

# directory with outputs of NTupleAnalysis
OUTDIR=output_07June
OUTPUTDIR=/eos/cms/store/group/phys_jetmet/pdas/07June/

mkdir -p ${OUTDIR}
[ -d ${OUTDIR}/ntuples ] || (ln -sf ${INPDIR} ${OUTDIR}/ntuples)

python batch_driver.py -l 1 -n 50000 -p JMETriggerAnalysisDriverRun3 \
 -i ${OUTDIR}/ntuples/*.root -o ${OUTDIR}/jobs \
 -od ${OUTPUTDIR} \
 --JobFlavour longlunch

python batch_monitor.py -i ${OUTDIR}/jobs -r --repe -f 900

python merge_batchOutputs.py -l 1 -i ${OUTPUTDIR}/*.root -o ${OUTPUTDIR}/outputs
rm -rf ${OUTDIR}/jobs

NUM_PROC=$(nproc)
if [[ ${HOSTNAME} == lxplus* ]]; then NUM_PROC=3; fi;
for rootfile_i in ${OUTPUTDIR}/outputs/*/*.root; do
  while [ $(jobs -p | wc -l) -ge ${NUM_PROC} ]; do sleep 5; done
  python jmeAnalysisHarvester.py -l 1 -i ${rootfile_i} -o ${OUTPUTDIR}/harvesting || true &
done
unset rootfile_i

jobs
wait || true

rm -rf ${OUTDIR}/outputs
