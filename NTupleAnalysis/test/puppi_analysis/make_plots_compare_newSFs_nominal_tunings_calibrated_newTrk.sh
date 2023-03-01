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
#ODIR=./tuning_test_newSFs_nominal_tunings_calibrated/plots
#ODIR=./tuning_test_puppiTune/plots
ODIR=./tuning_test_puppiJets_tuneV0/plots


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
     

      # jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline_puTracks_new -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_vtxfit_dz/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'dz':600:1:24 \
      # ./tuning_test_vtxfit_dzPU/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'dz PU':632:1:25 \
      # ./tuning_test_vtxfit_pixelPU/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'pixel PU':800:1:26 \
      # -l 'Run3Summer21_QCD_PtFlat15to7000_14TeV_PU'

      # jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline_puTracks_new -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_puppiTune/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_1.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'nominal AB':600:1:24 \
      # ./tuning_test_puppiTune/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_1.5/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'1.5 x B':616:1:25 \
      # ./tuning_test_puppiTune/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_2.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'2.0 x B':432:1:25 \
      # ./tuning_test_puppiTune/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_3.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'3.0 x B':632:1:25 \
      # ./tuning_test_puppiTune/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_4.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'4.0 x B':416:1:25 \
      # ./tuning_test_puppiTune/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_5.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'5.0 x B':800:1:25 \
      

      # jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_puppiJets_newVerticesPF/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'full pf vertices ':600:1:24 \
      # ./tuning_test_puppiJets_pixelVertices/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'pixel vertices':616:1:25 \
      
      
      
      # jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_puppiJets_ptcut6GEV/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'tuneV1':600:1:24 \
      # ./tuning_test_puppiJets_Azero/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'A=0':616:1:25 \
      # ./tuning_test_puppiJets_ABzero/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'A=B=0':632:1:26 \

      #jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      #-i ./tuning_test_puppiJets_ptcut6GEV/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'loose':600:1:24 \
      #./tuning_test_puppiJets_ptcut6GEV_tight/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'tight':616:1:25 \
      #./tuning_test_puppiJets_ptcut6GEV_highPurity/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'high purity':632:1:26 \
      # #./tuning_test_puppiJets_pixelRemove/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'no pixel':616:1:25 \

      
      # jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_puppiJets_nocut/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'mixed Trk':600:1:24 \
      # ./tuning_test_puppiJets_ptcut6GEV/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'pt<6GeV':616:1:25 \
      # ./tuning_test_puppiJets_ptcut4GEV/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'pt<4GeV':632:1:26 \
      # #./tuning_test_puppiJets_pixelRemove/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'no pixel':616:1:25 \
     

      # jmePlots.py -k run3_jme_compareTRK5_puppi_noOffline_puTracks_new -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_tuneV1/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'fully tuned':600:1:24 \
      # -l 'Run3Summer21_QCD_PtFlat15to7000_14TeV_PU'
      
      # jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_puppiJets_newVerticesPF/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'Run3Summer21':600:1:24 \
      # ./tuning_test_puppiJets_noAB/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'Run3Summer22':632:1:25 \


      # jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks_new_comparePF -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_puppiJets_postEEtag_nominalTrk/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'nominal Trk':1:1:24 \
      # ./tuning_test_puppiJets_tuneV1/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'mixed Trk':632:1:25 \

      
      jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks_new_comparePF -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      -i ./tuning_test_puppiJets_postEEtag_nominalTrk/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'nominal Trk':1:1:24 \
      ./tuning_test_puppiJets_tuneV1/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'mixed Trk (tight PUPPI)':632:1:25 \
      ./tuning_test_puppiJets_tuneV0/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'mixed Trk (loose PUPPI)':600:1:25 \

      # jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks_new_comparePF -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD \
      # -i ./tuning_test_puppiJets_postEEtag_nominalTrk/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'nominal Trk':1:1:24 \
      # ./tuning_test_puppiJets_tuneV1/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'mixed Trk':632:1:25 \
      # ./tuning_test_puppiJets_ptstart10/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'mixed ptStart=10':800:1:25 \
      # ./tuning_test_puppiJets_ptstart5/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'mixed ptStart=5':616:1:25 \
      # ./tuning_test_puppiJets_ptstart0/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_QCD_Pt15to7000_14TeV_PU__0.root:'mixed ptStart=0':600:1:25 \

      
      
      # organise the plots
      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD/NoSelection
    

      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD/noPUtracks
      

      ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/QCD/withPUtracks


      # jmePlots.py -k run3_jme_compareTRK5_puppiCorr_noOffline_puTracks_new_comparePF -o ./${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBFHtoInv \
      # -i ./tuning_test_pfJets_new/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'nominal Trk':1:1:24 \
      # ./tuning_test_puppiJets_new/harvester_output/HLT_Run3TRK/MinNeutralPt_0.0/MinNeutralPtSlope_0.0/Run3Winter21_VBF_HToInvisible_14TeV_PU__0.root:'mixed Trk':600:1:25 \
      # -l 'Run3Summer21_QCD_PtFlat15to7000_14TeV_PU'
      
      # # organise the plots
      # ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBFHtoInv/NoSelection
    

      # ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBFHtoInv/noPUtracks
      

      # ./organise_plots.sh ${ODIR}/${recoKey}/MinNeutralPt_${MinNeutralPt_factor}/MinNeutralPtSlope_${MinNeutralPtSlope_factor}/VBFHtoInv/withPUtracks
        
    
    done
  done
done

unset recoKeys MinNeutralPt_factors MinNeutralPtSlope_factors 
unset IDIR ODIR
unset FOUND_ODIR



