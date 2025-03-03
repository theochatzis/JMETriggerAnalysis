#!/bin/bash
source env.sh

# directory with input JMETriggerNTuple(s)
NAME=test_leadJetCand
RECO=HLT_Run3TRK
INPDIR=/eos/user/t/tchatzis/samples2023/${NAME}/${RECO}/samples_merged/
#INPDIR=/eos/user/t/tchatzis/samples2023/validation_2024JECS/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/crab_validation_2024JECS/samples_merged/
#INPDIR=/eos/user/t/tchatzis/samples2023/validation_2024JECS/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/crab_validation_defaultJECS/samples_merged/
#INPDIR=/eos/user/t/tchatzis/samples2023/validation_2024JECS/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/crab_validation_2024JECS_extraPhi/samples_merged/

#directory with outputs of NTupleAnalysis
OUTDIR=${NAME}_${RECO}_test
OUTPUTDIR=/eos/user/t/tchatzis/samples2023/${NAME}/${RECO}/
#OUTPUTDIR=/eos/user/t/tchatzis/samples2023/validation_2024JECS/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/crab_validation_2024JECS/
#OUTPUTDIR=/eos/user/t/tchatzis/samples2023/validation_2024JECS/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/crab_validation_defaultJECS/
#OUTPUTDIR=/eos/user/t/tchatzis/samples2023/validation_2024JECS/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/crab_validation_2024JECS_extraPhi/

mkdir -p ${OUTDIR}
[ -d ${OUTDIR}/ntuples ] || (ln -sf ${INPDIR} ${OUTDIR}/ntuples)


batch_driver.py -l 1 -n 50000 -p JMETriggerAnalysisDriverRun3 \
 -i ${INPDIR}/*.root -o ${OUTDIR}/jobs \
 -od ${OUTPUTDIR} \
 --JobFlavour espresso
 
# batch_driver.py -l 1 -n 50000 -p JMETriggerAnalysisDriverRun3 \
#  -i ${OUTDIR}/ntuples/*.root -o ${OUTDIR}/jobs \
#  -od ${OUTPUTDIR} \
#  --JobFlavour espresso

batch_monitor.py -i ${OUTDIR}/jobs -r #--repe -f 1200

# echo "merging jobs outputs..."
# merge_batchOutputs.py -l 0 -i ${OUTPUTDIR}/*.root -o ${OUTPUTDIR}/outputs

# NUM_PROC=$(nproc)
# if [[ ${HOSTNAME} == lxplus* ]]; then NUM_PROC=2; fi; #process NUM_PROC files each time
# for rootfile_i in ${OUTPUTDIR}/outputs/*.root; do
#   while [ $(jobs -p | wc -l) -ge ${NUM_PROC} ]; do sleep 5; done
#   echo ${rootfile_i}
#   jmeAnalysisHarvester_experimental2.py -pc gausfit -l 0 -i ${rootfile_i} -o ${OUTPUTDIR}/harvesting || true &
# done
# unset rootfile_i

# jobs
# wait || true


#rm -rf ${OUTDIR}/outputs

