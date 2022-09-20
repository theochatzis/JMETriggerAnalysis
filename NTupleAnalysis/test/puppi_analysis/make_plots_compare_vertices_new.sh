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
ODIR=./tuning_compare_vertices_new/plots

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
      ./tuning_old_vertex/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'PF vertices':416:1:24 \
      ./tuning_new_vertex_old_proxy_v6_dzCut/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'Pixel vertices with dz<0.3':904:1:24 \
      -l 'Run3Winter21_QCD_PtFlat15to7000_14TeV_PU'
      
      jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv \
      -i ./${NOMINAL_IDIR}/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_1.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'nominal settings':600:1:24 \
      ./tuning_old_vertex/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'PF vertices':416:1:24 \
      ./tuning_new_vertex_old_proxy_v6_dzCut/harvester_output/HLT_Run3TRK/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'Pixel vertices with dz<0.3':904:1:24 \
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



