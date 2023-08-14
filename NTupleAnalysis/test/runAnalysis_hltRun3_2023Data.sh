#!/bin/bash
source env.sh

# directory with input JMETriggerNTuple(s)
NAME=data_BPixIssue_eraC
RECO=default
INPDIR=/eos/user/t/tchatzis/samples2023/${NAME}/${RECO}/samples_merged/

#directory with outputs of NTupleAnalysis
OUTDIR=${NAME}_${RECO}
OUTPUTDIR=/eos/user/t/tchatzis/samples2023/${NAME}/${RECO}/

# mkdir -p ${OUTDIR}
# [ -d ${OUTDIR}/ntuples ] || (ln -sf ${INPDIR} ${OUTDIR}/ntuples)

# batch_driver.py -l 1 -n 50000 -p JMETriggerAnalysisDriverRun3 \
#  -i ${OUTDIR}/ntuples/*.root -o ${OUTDIR}/jobs \
#  -od ${OUTPUTDIR} \
#  --JobFlavour espresso

# batch_monitor.py -i ${OUTDIR}/jobs -r #--repe -f 900

echo "merging jobs outputs..."

merge_batchOutputs.py -l 0 -i ${OUTPUTDIR}/*.root -o ${OUTPUTDIR}/outputs

NUM_PROC=$(nproc)
if [[ ${HOSTNAME} == lxplus* ]]; then NUM_PROC=2; fi; #process NUM_PROC files each time
for rootfile_i in ${OUTPUTDIR}/outputs/*.root; do
  while [ $(jobs -p | wc -l) -ge ${NUM_PROC} ]; do sleep 5; done
  echo ${rootfile_i}
  jmeAnalysisHarvester.py -l 0 -i ${rootfile_i} -o ${OUTPUTDIR}/harvesting || true &
done
unset rootfile_i

jobs
wait || true



#rm -rf ${OUTDIR}/outputs

