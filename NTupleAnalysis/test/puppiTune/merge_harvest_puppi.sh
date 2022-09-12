#/bin/bash

TUNE_VALUES=(
  0.1
  0.2
  0.3
  0.4
  0.5
  0.6
  0.7
  0.8
  0.9
  1.0
  10.0
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


IDIR=./$1/driver_output 
ODIR=./$1/harvester_output

FOUND_ODIR=false


for VALUE in ${TUNE_VALUES[@]}; do
  for key in "${keys[@]}"; do
    if [ -d ${ODIR}/${key}/value_${VALUE} ]; then FOUND_ODIR=true; fi
    find ${ODIR} -path ${ODIR}/${key}/value_${VALUE}
  done
done

if ${FOUND_ODIR}; then echo 'The above paths with the harvester outputs will be overwritten...'; fi
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
    # run the harvester to make profiles, efficiencies etc.
    jmeAnalysisHarvester.py -l 0 \
      -i ./${IDIR}/${key}/value_${VALUE}/*.root \
      -o ./${ODIR}/${key}/value_${VALUE}      
    
  done
done

unset keys
unset IDIR ODIR
unset FOUND_ODIR



