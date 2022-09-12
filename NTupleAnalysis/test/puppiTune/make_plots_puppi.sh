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
if ${FOUND_ODIR}; then echo 'The above paths with the plots outputs will be overwritten...'; fi
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

  # jmePlots.py -k phase2_jme_puppi_new -o ./${ODIR}/${key}/QCD -e png \
  # -i ./${IDIR}/${key}/value_0.1/value_0.1__0.root:'dz=0.1':1:1:24 \
  # ./${IDIR}/${key}/value_0.2/value_0.2__0.root:'dz=0.2':861:1:24 \
  # ./${IDIR}/${key}/value_0.3/value_0.3__0.root:'dz=0.3':874:1:24 \
  # ./${IDIR}/${key}/value_0.5/value_0.5__0.root:'dz=0.5':904:1:24 \
  # ./${IDIR}/${key}/value_100.0/value_100.0__0.root:'dz=100.0':807:1:24 \
  # -l 'Phase2HLT_QCD_Flat_Pt-15to3000_14TeV_PU200'

  # jmePlots.py -k phase2_jme_puppi_new -o ./${ODIR}/${key}/QCD -e png \
  # -i ./${IDIR}/${key}/value_1.00/value_1.00__0.root:'offset x 1.00':1:1:24 \
  # ./${IDIR}/${key}/value_0.75/value_0.75__0.root:'offset x 0.75':861:1:24 \
  # ./${IDIR}/${key}/value_0.50/value_0.50__0.root:'offset x 0.50':874:1:24 \
  # ./${IDIR}/${key}/value_0.25/value_0.25__0.root:'offset x 0.25':904:1:24 \
  # ./${IDIR}/${key}/value_0.00/value_0.00__0.root:'offset x 0.00':807:1:24 \
  # -l 'Phase2HLT_QCD_Flat_Pt-15to3000_14TeV_PU200'

  # jmePlots.py -k phase2_jme_puppi_new -o ./${ODIR}/${key}/QCD -e png \
  # -i ./${IDIR}/${key}/value_0/value_0__0.root:'no. vtxs = 0':1:1:24 \
  # ./${IDIR}/${key}/value_2/value_2__0.root:'no. vtxs = 2':874:1:24 \
  # ./${IDIR}/${key}/value_3/value_3__0.root:'no. vtxs = 3':807:1:24 \
  # -l 'Phase2HLT_QCD_Flat_Pt-15to3000_14TeV_PU200'

   jmePlots.py -k phase2_jme_puppi_new -o ./${ODIR}/${key}/QCD -e png \
   -i ./${IDIR}/${key}/value_0.6/value_0.6__0.root:'dz=0.6':1:1:24 \
   ./${IDIR}/${key}/value_0.7/value_0.7__0.root:'dz=0.7':861:1:24 \
   ./${IDIR}/${key}/value_0.8/value_0.8__0.root:'dz=0.8':874:1:24 \
   ./${IDIR}/${key}/value_1.0/value_1.0__0.root:'dz=1.0':904:1:24 \
   ./${IDIR}/${key}/value_10.0/value_10.0__0.root:'dz=10.0':807:1:24 \
   -l 'Phase2HLT_QCD_Flat_Pt-15to3000_14TeV_PU200'
  
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



