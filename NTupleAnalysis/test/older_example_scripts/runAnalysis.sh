#!/bin/bash

NTUPLES_DIR=/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/JetMET_PhaseII/JMETriggerAnalysis_phase2/ntuples/output_hltPhase2_201209

OUTDIR=output_hltPhase2_201209_tdrDraft2_deltaR02_v2

mkdir -p ${OUTDIR}

ln -sf ${NTUPLES_DIR} ${OUTDIR}/ntuples
unset NTUPLES_DIR

batch_driver.py -l 1 -n 100000 -p JMETriggerAnalysisDriverPhase2 \
 -i ${OUTDIR}/ntuples/*/*.root -o ${OUTDIR}/jobs \
 --AccountingGroup group_u_CMS.CAF.PHYS --JobFlavour longlunch

batch_monitor.py -i ${OUTDIR}/jobs -r --repe -f 900

./mergeAndHarvest_hltPhase2.sh ${OUTDIR}

./plotTDR.py -i ${OUTDIR}/harvesting -o ${OUTDIR}_plots;

unset OUTDIR
