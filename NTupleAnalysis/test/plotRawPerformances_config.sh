#!/bin/bash
source env.sh

# directory with input(s) 
INPDIR=/eos/user/t/tchatzis/samples2023/


#OUTDIR=./plots_test_winter24
OUTDIR=/eos/user/t/tchatzis/raw_jets_pfhc_vbf/



rm -rf ${OUTDIR}


# jmePlots.py -k version_check_mc_raw  \
# -o ${OUTDIR} \
# -i /eos/user/t/tchatzis/samples2023/test_24_winter23pfhc_met/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'2023 PFHC':1:1:20 \
#    /eos/user/t/tchatzis/samples2023/test_24_winter24pfhc_met/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'2024 PFHC':632:1:20 \
# -l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD FlatPt Winter24'

jmePlots.py -k version_check_mc_raw  \
-o ${OUTDIR} \
-i /eos/user/t/tchatzis/samples2023/test_24_winter23pfhc_met/HLT_Run3TRK/harvesting/Run3Winter23_VBF_HToInvisible_13p6TeV_PU65.root:'2023 PFHC':1:1:20 \
   /eos/user/t/tchatzis/samples2023/test_24_winter24pfhc_met/HLT_Run3TRK/harvesting/Run3Winter23_VBF_HToInvisible_13p6TeV_PU65.root:'2024 PFHC':632:1:20 \
-l '#font[61]{CMS} #font[52]{Run-3 Simulation} VBF H #rightarrow Invisible Winter24'

# jmePlots.py -k version_check_data  \
# -o ${OUTDIR} \
# -i /eos/user/t/tchatzis/samples2023/test_dataG_compare/default/harvesting/data.root:'default':1:1:26 \
#    /eos/user/t/tchatzis/samples2023/test_dataG_compare/hcal_jecs2022/harvesting/data.root:'HCAL update+jec/pfhc2022':632:1:26 \
#    /eos/user/t/tchatzis/samples2023/test_dataG_new2023/hcal_jecs2023/harvesting/data.root:'HCAL update+jec/pfhc2023':600:1:26 \
#    /eos/user/t/tchatzis/samples2023/test_pfhc2023/hcal_jecs2022/harvesting/data.root:'HCAL update+jec2022/pfhc2023':416:1:26 \
# -l '#font[61]{CMS} #font[52]{Run-3 Data} JetMET 2022 RunG'

#jmePlots.py -k run3_jme_pfperformance  \
#-m "*NoSelection*" \
#-o ${OUTDIR} \
#-i ${INPDIR}/test_24_summer23/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'L2s noBPix':632:1:26 \
#   ${INPDIR}/test_24_summer23bpix/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Offline L2s BPix':600:1:26 \
#-l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD Winter24'a

# jmePlots.py -k run3_jme_pfperformance  \
# -m "*NoSelection*" \
# -o ${OUTDIR} \
# -i ${INPDIR}/test_summer23new_noBPix/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Summer23 preBPix':1:1:26 \
#    ${INPDIR}/test_24_winter23jecs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Winter23 JECs':632:1:26 \
#    ${INPDIR}/test_24_winter24jecs_recipe/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Winter24 JECs':600:1:26
# -l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD Winter24'
#   ${INPDIR}/test_24_winter24jecs_NoBPix/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Winter24 JECs (NoBPix)':600:1:26 \
#   ${INPDIR}/test_24_winter24jecs_bpix_L1/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Winter24 JECs (BPix)':616:1:26 \
#-l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD Winter24'
#   ${INPDIR}/test_summer23new_noBPix/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Summer23':600:1:26 \
#   ${INPDIR}/test_summer23new_BPix_noRecovery/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Summer23BPix':616:1:26 \
#-l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD'

#jmePlots.py -k run3_jme_pfperformance  \
#-m "*NoSelection*" \
#-o ${OUTDIR} \
#-i ${INPDIR}/test_Winter23JECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Winter23 JECs':1:1:26 \
#-l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD Winter24'

rm ${OUTDIR}/NoSelection/*mass*.png
rm ${OUTDIR}/NoSelection/*MatchedToGEN_pt_overGEN.png

# organize plots into folders

Regions=(
EtaIncl_
HB_
HE1_
HE2_
HF_
BPix_
BPixVeto_
MET
)

for region_name in "${Regions[@]}"; do
  mkdir -p ${OUTDIR}/NoSelection/${region_name}
  mv ${OUTDIR}/NoSelection/*${region_name}*.png ${OUTDIR}/NoSelection/${region_name}

  mkdir -p ${OUTDIR}/NoSelection/${region_name}/efficiency
  mkdir -p ${OUTDIR}/NoSelection/${region_name}/response
  mkdir -p ${OUTDIR}/NoSelection/${region_name}/resolution
  mkdir -p ${OUTDIR}/NoSelection/${region_name}/jet_content
  mkdir -p ${OUTDIR}/NoSelection/${region_name}/kinematics
  
  mv ${OUTDIR}/NoSelection/${region_name}/*eff.png ${OUTDIR}/NoSelection/${region_name}/efficiency
  mv ${OUTDIR}/NoSelection/${region_name}/*Mean*.png ${OUTDIR}/NoSelection/${region_name}/response
  mv ${OUTDIR}/NoSelection/${region_name}/*RMS*.png ${OUTDIR}/NoSelection/${region_name}/resolution
  mv ${OUTDIR}/NoSelection/${region_name}/*Multiplicity*.png ${OUTDIR}/NoSelection/${region_name}/jet_content
  mv ${OUTDIR}/NoSelection/${region_name}/*Fraction*.png ${OUTDIR}/NoSelection/${region_name}/jet_content
  mv ${OUTDIR}/NoSelection/${region_name}/*.png ${OUTDIR}/NoSelection/${region_name}/kinematics
done

rm ${OUTDIR}/NoSelection/*.png

unset INPDIR region_name Regions OUTDIR pt_region_number
