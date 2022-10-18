#/bin/bash

# define the samples you want to use
keys=(
  #RelValQCD_Pt15To7000_Flat_14TeV_PU200
  Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200
  #Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
  #RelValQCD_Pt15To7000_Flat_14TeV_noPU
  Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200
)


IDIR=./$1/driver_output 
ODIR=./$1/harvester_output

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
  # run the harvester to make profiles, efficiencies etc.
  jmeAnalysisHarvester.py -l 0 \
    -i ./${IDIR}/${key}/*.root \
    -o ./${ODIR}/${key}      
  
done

unset keys
unset IDIR ODIR
unset FOUND_ODIR



