#!/bin/bash

# directory with input JMETriggerNTuple(s)
INPDIR=/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/JetMET_PhaseII/JMETriggerAnalysis_run3/ntuples/hltRun3_testTRK_210331

# directory with outputs of NTupleAnalysis
OUTDIR=output_hltRun3_testTRK_210331_v03

mkdir -p ${OUTDIR}
[ -d ${OUTDIR}/ntuples ] || (ln -sf ${INPDIR} ${OUTDIR}/ntuples)

batch_driver.py -l 1 -n 50000 -p JMETriggerAnalysisDriverRun3 \
 -i ${OUTDIR}/ntuples/*/*.root -o ${OUTDIR}/jobs \
 --AccountingGroup group_u_CMS.CAF.PHYS --JobFlavour longlunch

batch_monitor.py -i ${OUTDIR}/jobs -r --repe -f 900

merge_batchOutputs.py -l 1 -i ${OUTDIR}/jobs/*/*.root -o ${OUTDIR}/outputs
rm -rf ${OUTDIR}/jobs

NUM_PROC=$(nproc)
if [[ ${HOSTNAME} == lxplus* ]]; then NUM_PROC=3; fi;
for rootfile_i in ${OUTDIR}/outputs/*/*.root; do
  while [ $(jobs -p | wc -l) -ge ${NUM_PROC} ]; do sleep 5; done
  jmeAnalysisHarvester.py -l 1 -i ${rootfile_i} -o ${OUTDIR}/harvesting || true &
done
unset rootfile_i

jobs
wait || true

rm -rf ${OUTDIR}/outputs
