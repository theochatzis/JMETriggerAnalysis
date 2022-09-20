#/bin/bash

# define the samples you want to use
recoKeys=(
HLT_Run3TRK
)

MinNeutralPt_factors=(
0.0
)

MinNeutralPtSlope_factors=(
0.0
)

NOMINAL_IDIR=./tuning_nominal/harvester_output
ODIR=./tuning_dz_old_vertex/plots

FOUND_ODIR=false


for recoKey in "${recoKeys[@]}"; do
  for MinNeutralPt_factor in  "${MinNeutralPt_factors[@]}"; do
    for MinNeutralPtSlope_factor in "${MinNeutralPtSlope_factors[@]}"; do
      if [ -d ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor} ]; then FOUND_ODIR=true; fi
      find ${ODIR} -path ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}
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
  for MinNeutralPt_factor in  "${MinNeutralPt_factors[@]}"; do
    for MinNeutralPtSlope_factor in "${MinNeutralPtSlope_factors[@]}"; do
      # ouput dir: if already exists remove it
      if [ -d ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor} ]; then rm -rf ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}; fi
      
      # make the plotting
      jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      -i ./${NOMINAL_IDIR}/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_1.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'nominal settings':600:1:24 \
      ./tuning_old_vertex_dz_0p20/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'dz<0.20':861:1:24 \
      ./tuning_old_vertex_dz_0p15/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'dz<0.15':874:1:24 \
      ./tuning_old_vertex_dz_0p10/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'dz<0.10':904:1:24 \
      ./tuning_old_vertex_dz_0p05/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'dz<0.05':807:1:24 \
      ./tuning_old_vertex_dz_0p025/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'dz<0.025':814:1:24 \
      -l 'Run3Winter21_QCD_PtFlat15to7000_14TeV_PU'
      
      jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv \
      -i ./${NOMINAL_IDIR}/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_1.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'nominal settings':600:1:24 \
      ./tuning_old_vertex_dz_0p20/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'dz<0.20':861:1:24 \
      ./tuning_old_vertex_dz_0p15/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'dz<0.15':874:1:24 \
      ./tuning_old_vertex_dz_0p10/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'dz<0.10':904:1:24 \
      ./tuning_old_vertex_dz_0p05/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'dz<0.05':807:1:24 \
      ./tuning_old_vertex_dz_0p025/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'dz<0.025':814:1:24 \
      -l 'Run3Winter21_VBF_HToInvisible_14TeV_PU'
      
      # organise the plots
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD/NoSelection
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv/NoSelection       
    done
  done
done

unset recoKeys MinNeutralPt_factors MinNeutralPtSlope_factors 
unset IDIR ODIR
unset FOUND_ODIR



