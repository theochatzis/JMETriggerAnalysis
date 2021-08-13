#!/bin/bash -e

[ $# -eq 1 ] || exit 1

INPDIR="${1}"
OUTDIR=$(basename "${INPDIR}")

hadd_ntuples.py -l 1 -i "${INPDIR}"/*/* -o "${INPDIR}"

batch_driver.py -i "${INPDIR}"/*/*.root -o "${OUTDIR}"/jobs -l 1 -n 50000 -p JMETriggerAnalysisDriverPhase2

NUM_PROC=$(nproc)
for exefile_i in "${OUTDIR}"/jobs/*/*.sh; do
  while [ $(jobs -p | wc -l) -ge "${NUM_PROC}" ]; do sleep 5; done
  ${exefile_i} || true &
done
unset exefile_i
jobs
wait || true

merge_batchOutputs.py -l 1 -i "${OUTDIR}"/jobs/*/*.root -o "${OUTDIR}"/outputs
rm -rf "${OUTDIR}"/jobs

NUM_PROC=$(nproc)
for rootfile_i in "${OUTDIR}"/outputs/*/*.root; do
  while [ $(jobs -p | wc -l) -ge "${NUM_PROC}" ]; do sleep 5; done
  jmeAnalysisHarvester.py -l 1 -i "${rootfile_i}" -o "${OUTDIR}"/harvesting || true &
done
unset rootfile_i
jobs
wait || true
rm -rf "${OUTDIR}"/outputs
