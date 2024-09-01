#/bin/bash

# define the samples you want to use
keys=(
  #RelValQCD_Pt15To7000_Flat_14TeV_PU200
  Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200
  #Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
  #RelValQCD_Pt15To7000_Flat_14TeV_noPU
  #Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
)


IDIR=/eos/user/t/tchatzis/MTDtiming_samples/$1
ODIR=./$1/driver_output

FOUND_ODIR=false


for key in "${keys[@]}"; do
  if [ -d ${ODIR}/${key}/ ]; then FOUND_ODIR=true; fi
  find ${ODIR} -path ${ODIR}/${key}
done
if ${FOUND_ODIR}; then echo 'The above paths with the driver outputs will be overwritten...'; fi
read -p "Do you want to continue? [y/n]" yn
case $yn in
    [Yy]* ) echo "Continuing the process...";;
    [Nn]* ) echo "Exiting..."; exit 1;;
    * ) echo "Please answer with y/n.";;
esac

for key in "${keys[@]}"; do
  # ouput dir: if already exists remove it
  if [ -d ./${ODIR}/${key} ]; then rm -rf ./${ODIR}/${key}; fi
  # run the batch driver to prepare the HTC jobs
  ../batch_driver.py -l 0 -n 100000 -p JMETriggerAnalysisDriverPhase2 \
  -i ${IDIR}/${key}/${key}.root \
  -od ./${ODIR}/${key} \
  -o ./${ODIR}/${key} \
  --time 2400
done

# run the batch monitor to submit the jobs
../batch_monitor.py -i ${ODIR} -r


unset keys
unset IDIR ODIR
unset FOUND_ODIR



