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


NTUPLES_IDIR=${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/scripts/tuning_puppi_$1
NTUPLES_ODIR=tuning_$1/added_ntuples 

FOUND_NTUPLES_ODIR=false


for recoKey in "${recoKeys[@]}"; do
  for RMSEtaSF_factor in  "${RMSEtaSF_factors[@]}"; do
    for MedEtaSF_factor in "${MedEtaSF_factors[@]}"; do
      if [ -d ./${NTUPLES_ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor} ]; then FOUND_NTUPLES_ODIR=true; fi
      find ./${NTUPLES_ODIR} -path ./${NTUPLES_ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}
    done
  done
done

if ${FOUND_NTUPLES_ODIR}; then echo 'The above paths will be overwritten...'; fi
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
      if [ -d ./${NTUPLES_ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor} ]; then rm -rf ./${NTUPLES_ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}; fi
      # add the ntuples jobs from input dir
      ../../hadd_ntuples.py -i ${NTUPLES_IDIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/Run3Winter20_QCD_PtFlat15to3000_14TeV_PU -o ./${NTUPLES_ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor} -l 0
      ../../hadd_ntuples.py -i ${NTUPLES_IDIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor}/Run3Winter20_VBF_HToInvisible_14TeV_PU -o ./${NTUPLES_ODIR}/${recoKey}/RMSEtaSF_${RMSEtaSF_factor}/MedEtaSF_${MedEtaSF_factor} -l 0
      
      # remove the multiple jobs files
      # rm -rf ${NTUPLES_IDIR}
    done
  done
done



unset recoKeys RMSEtaSF_factors MedEtaSF_factors 
unset NTUPLES_IDIR NTUPLES_ODIR
unset FOUND_NTUPLE_ODIR


