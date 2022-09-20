#/bin/bash

# define the samples you want to use
recoKeys=(
HLT_Run3TRK
)

RMSEtaSF_factors=(
1.00
)

MedEtaSF_factors=(
1.80
1.90
2.00
)


IDIR=tuning_$1/harvester_output 
ODIR=tuning_$1/plots

FOUND_ODIR=false


for recoKey in "${recoKeys[@]}"; do
  for RMSEtaSF_factor in  "${RMSEtaSF_factors[@]}"; do
    for MedEtaSF_factor in "${MedEtaSF_factors[@]}"; do
      if [ -d ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor} ]; then FOUND_ODIR=true; fi
      find ./${ODIR} -path ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}
    done
  done
done
if ${FOUND_ODIR}; then echo 'The above paths with the driver outputs will be overwritten...'; fi
read -p "Do you want to continue? [y/n]" yn
case $yn in
    [Yy]* ) echo "Continuing the process...";;
    [Nn]* ) echo "Exiting..."; exit 1;;
    * ) echo "Please answer with y/n.";;
esac

for recoKey in "${recoKeys[@]}"; do
  for RMSEtaSF_factor in  "${RMSEtaSF_factors[@]}"; do
    for MedEtaSF_factor in "${MedEtaSF_factors[@]}"; do
      # ouput dir: if already exists remove it
      if [ -d ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor} ]; then rm -rf ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}; fi
      
      # make the plotting
      ../../jmePlots.py -k run3_jme_compareTRK5_puppi -o ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/QCD \
      -i ./${IDIR}/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_1.0/Run3Winter20_QCD_PtFlat15to3000_14TeV_PU__0.root:'nominal settings':600:1:24 ./${IDIR}/HLT_Run3TRK/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/Run3Winter20_QCD_PtFlat15to3000_14TeV_PU__0.root:'modified settings':632:1:24 \
      -l 'Run3Winter20_QCD_PtFlat15to3000_14TeV_PU'
      
      ../../jmePlots.py -k run3_jme_compareTRK5_puppi -o ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/VBF_HToInv \
      -i ./${IDIR}/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_1.0/Run3Winter20_VBF_HToInvisible_14TeV_PU__0.root:'nominal settings':600:1:24 ./${IDIR}/HLT_Run3TRK/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/Run3Winter20_VBF_HToInvisible_14TeV_PU__0.root:'modified settings':632:1:24 \
      -l 'Run3Winter20_VBF_HToInvisible_14TeV_PU'
      
      # organise the plots
      ./organise_plots.sh ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/QCD/NoSelection
      ./organise_plots.sh ./${ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/VBF_HToInv/NoSelection       
    done
  done
done

unset recoKeys RMSEtaSF_factors MedEtaSF_factors 
unset IDIR ODIR
unset FOUND_ODIR



