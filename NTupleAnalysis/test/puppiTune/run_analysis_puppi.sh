#/bin/bash

TUNE_VALUES=(
  0.1
  0.2
  0.3
  1000.0
)
# TUNE_VALUES=(
#   0.1
#   0.2
#   0.3
#   0.5
#   100.0
# )

# define the samples you want to use
keys=(
  #RelValQCD_Pt15To7000_Flat_14TeV_PU200
  Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200
  #Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
  #RelValQCD_Pt15To7000_Flat_14TeV_noPU
)


IDIR=/eos/user/t/tchatzis/MTDtiming_samples/$1
ODIR=./$1/driver_output



  
FOUND_ODIR=false

for VALUE in ${TUNE_VALUES[@]}; do
  for key in "${keys[@]}"; do
    if [ -d ${ODIR}/${key}/value_${VALUE} ]; then FOUND_ODIR=true; fi
    find ${ODIR} -path ${ODIR}/${key}/value_${VALUE}
  done
done

if ${FOUND_ODIR}; then echo 'The above paths with the driver outputs will be overwritten...'; fi
read -p "Do you want to continue? [y/n]" yn
case $yn in
    [Yy]* ) echo "Continuing the process...";;
    [Nn]* ) echo "Exiting..."; exit 1;;
    * ) echo "Please answer with y/n.";;
esac

for VALUE in ${TUNE_VALUES[@]}; do
  for key in "${keys[@]}"; do
    # ouput dir: if already exists remove it
    if [ -d ./${ODIR}/${key}/value_${VALUE} ]; then rm -rf ./${ODIR}/${key}/value_${VALUE}; fi
    # run the batch driver to prepare the HTC jobs
    batch_driver.py -l 0 -n 100000 -p JMETriggerAnalysisDriverPhase2 \
    -i ${IDIR}/${key}/value_${VALUE}/value_${VALUE}.root \
    -od ./${ODIR}/${key}/value_${VALUE} \
    -o ./${ODIR}/${key}/value_${VALUE} \
    --time 2400
  done  
done

# run the batch monitor to submit the jobs
batch_monitor.py -i ${ODIR} -r

unset keys
unset IDIR ODIR
unset FOUND_ODIR



