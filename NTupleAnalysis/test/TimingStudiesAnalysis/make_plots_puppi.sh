#/bin/bash

# define the samples you want to use
keys=(
  Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200
)

NOMINAL_IDIR=./tuning_nominal/harvester_output
IDIR=./$1/harvester_output 
ODIR=./$1/plots

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
  
  # make the plotting

  jmePlots.py -k phase2_jme_puppi -o ./${ODIR}/${key}/QCD \
  -i ./${IDIR}/${key}/Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200__0.root:'simplified menu':600:1:24 \
  -l 'Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200'
  
  #jmePlots.py -k phase2_jme_puppi -o ./${ODIR}/${key}/VBF_HToInv \
  #-i ./${IDIR}/${key}/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'nominal':600:1:24 \
  #-l 'Run3Winter21_VBF_HToInvisible_14TeV_PU'
  
  # organise the plots
  ./organise_plots.sh ${ODIR}/${key}/QCD/NoSelection
  #./organise_plots.sh ${ODIR}/${key}/VBF_HToInv/NoSelection       
  
done

unset keys
unset IDIR ODIR
unset FOUND_ODIR



