#!/bin/bash -e

# directory with input JMETriggerNTuple(s)
INPDIR=/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/JetMET_PhaseII/JMETriggerAnalysis_phase2/ntuples/output_hltPhase2_201209

# directory with outputs of NTupleAnalysis
OUTDIR=output_hltPhase2_201209_HLTTDR

mkdir -p ${OUTDIR}

ln -sf ${INPDIR} ${OUTDIR}/ntuples

batch_driver.py -l 1 -n 100000 -p JMETriggerAnalysisDriverPhase2 \
 -i ${OUTDIR}/ntuples/*/*.root -o ${OUTDIR}/jobs \
 --AccountingGroup group_u_CMS.CAF.PHYS --JobFlavour longlunch

batch_monitor.py -i ${OUTDIR}/jobs -r --repe -f 900

merge_batchOutputs.py -l 1 -i ${OUTDIR}/jobs/*/*.root -o ${OUTDIR}/outputs
rm -rf ${OUTDIR}/jobs

NUM_PROC=$(nproc)
if [[ ${HOSTNAME} == lxplus* ]]; then NUM_PROC=3; fi;

for rootfile_i in ${OUTDIR}/outputs/*/*.root; do
  while [ $(jobs -p | wc -l) -ge ${NUM_PROC} ]; do sleep 5; done
  jmeAnalysisHarvester.py -l 1 -i ${rootfile_i} -o ${OUTDIR}/harvesting2 || true &
done
unset rootfile_i

jobs
wait || true

rm -rf ${OUTDIR}/outputs

./plot_hltPhase2TDR.py -i ${OUTDIR}/harvesting -o ${OUTDIR}_plots
