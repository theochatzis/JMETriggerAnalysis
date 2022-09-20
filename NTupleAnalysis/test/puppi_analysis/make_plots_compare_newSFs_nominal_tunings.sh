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
#ODIR=./tuning_test_newSFs_nominal_tunings_withPUtracks/plots
ODIR=./tuning_test_newSFs_nominal_tunings/plots

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
      jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_noPUtracks \
      -i ./tuning_test_newSFs_nominal/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'nominal AB':600:1:24 \
      ./tuning_test_newSFs_nominal_tuned_withoutPUtracks/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'tuned AB':616:1:25 \
      ./tuning_test_newSFs_nominal_FixedBackupDist_PUfitNew/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'offline MedRMS':632:1:25 \
      ./tuning_test_newSFs_nominal_FixedBackupDist_PUfitNew_tuned_withPUtracks/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'offline MedRMS + tuned AB':800:1:25 \
      
      jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv_noPUtracks \
      -i ./tuning_test_newSFs_nominal/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'nominal AB':600:1:24 \
      ./tuning_test_newSFs_nominal_tuned_withoutPUtracks/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'tuned AB':616:1:25 \
      ./tuning_test_newSFs_nominal_FixedBackupDist_PUfitNew/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'offline MedRMS':632:1:25 \
      ./tuning_test_newSFs_nominal_FixedBackupDist_PUfitNew_tuned_withPUtracks/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'offline MedRMS + tuned AB':800:1:25 \
      
      jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_withPUtracks \
      -i ./tuning_test_newSFs_nominal/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'nominal AB':600:1:24 \
      ./tuning_test_newSFs_nominal_tuned_withPUtracks/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'tuned AB':616:1:25 \
      ./tuning_test_newSFs_nominal_FixedBackupDist_PUfitNew/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'offline MedRMS':632:1:25 \
      ./tuning_test_newSFs_nominal_FixedBackupDist_PUfitNew_tuned_withPUtracks/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'offline MedRMS + tuned AB':800:1:25 \
      
      jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv_withPUtracks \
      -i ./tuning_test_newSFs_nominal/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'nominal AB':600:1:24 \
      ./tuning_test_newSFs_nominal_tuned_withPUtracks/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'tuned AB':616:1:25 \
      ./tuning_test_newSFs_nominal_FixedBackupDist_PUfitNew/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'offline MedRMS':632:1:25 \
      ./tuning_test_newSFs_nominal_FixedBackupDist_PUfitNew_tuned_withPUtracks/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'offline MedRMS + tuned AB':800:1:25 \

      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_6.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'6 x B':820:1:25 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_7.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'7 x B':400:1:25 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_8.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'8 x B':800:1:25 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_10.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'10 x B':616:1:25 \
      #-l 'Run3Winter21_QCD_PtFlat15to7000_14TeV_PU'

      #jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_tune2 \
      #-i ./tuning_test_newSFs_nominal/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'nominal AB':600:1:24 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_1.5/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'5 x B':616:1:25 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_2.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'6 x B':632:1:25 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_3.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'7 x B':416:1:25 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_4.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'8 x B':800:1:25 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_1.0/MinNeutralPtSlope_4.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'10 x B':800:1:25 \
      
      #jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv \
      #-i ./tuning_test_newSFs_nominal/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'SFs + nominal A,B':600:1:24 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_2.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'hybrid method':632:1:25 \
      #./tuning_test_newSFs_nominal_increase_B/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_3.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'hybrid method, no offset':416:1:26 \
      #-l 'Run3Winter21_VBF_HToInvisible_14TeV_PU'
      
      # organise the plots
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_noPUtracks/NoSelection
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv_noPUtracks/NoSelection

      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_noPUtracks/noPUtracks
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv_noPUtracks/noPUtracks

      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_noPUtracks/withPUtracks
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv_noPUtracks/withPUtracks        
    
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_withPUtracks/NoSelection
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv_withPUtracks/NoSelection

      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_withPUtracks/noPUtracks
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv_withPUtracks/noPUtracks

      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD_withPUtracks/withPUtracks
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBF_HToInv_withPUtracks/withPUtracks       
    done
  done
done

unset recoKeys MinNeutralPt_factors MinNeutralPtSlope_factors 
unset IDIR ODIR
unset FOUND_ODIR



