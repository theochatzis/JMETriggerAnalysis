#!/bin/bash
source env.sh

# directory with input(s) 
INPDIR=/eos/user/t/tchatzis/samples2023/


OUTDIR=./plots_testPFHConly_Corrected


# jmePlots.py -k version_check  \
# -o ${OUTDIR} \
# -i /eos/user/t/tchatzis/samples2023/test_noCustom/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'default':1:1:26 \
#    /eos/user/t/tchatzis/samples2023/test_correctJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'HCAL update':632:1:26 \
# #   /eos/user/t/tchatzis/samples2023/test_wrongJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'HCAL update+condDB JECs':632:1:26 \
# #   /eos/user/t/tchatzis/samples2023/test_correctJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'HCAL update+fixed JECs':600:1:26 \
# #-l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD PU 65'

rm -rf ${OUTDIR}

# jmePlots.py -k version_check_data  \
# -o ${OUTDIR} \
# -i /eos/user/t/tchatzis/samples2023/test_dataG_compare/default/harvesting/data.root:'default':1:1:26 \
#    /eos/user/t/tchatzis/samples2023/test_dataG_compare/hcal_jecs2022/harvesting/data.root:'HCAL update+jec/pfhc2022':632:1:26 \
#    /eos/user/t/tchatzis/samples2023/test_dataG_new2023/hcal_jecs2023/harvesting/data.root:'HCAL update+jec/pfhc2023':600:1:26 \
#    /eos/user/t/tchatzis/samples2023/test_pfhc2023/hcal_jecs2022/harvesting/data.root:'HCAL update+jec2022/pfhc2023':416:1:26 \
# -l '#font[61]{CMS} #font[52]{Run-3 Data} JetMET 2022 RunG'

# jmePlots.py -k version_check_data  \
# -o ${OUTDIR} \
# -i /eos/user/t/tchatzis/samples2023/test_dataG_new2023/hcal_jecs2023/harvesting/data.root:'HCAL update+jec/pfhc2023':600:1:26 \
# -l '#font[61]{CMS} #font[52]{Run-3 Data} JetMET 2022 RunG'

# jmePlots.py -k compare_PFCalo_PFHC_withOffline  \
# -o ${OUTDIR} \
# -i ${INPDIR}/pfhc_test_offline/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'HLT PFHC':1:1:26 
# -l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD Winter23 FlatPt'

jmePlots.py -k compare_PFCalo_PFHC  \
-o ./plots_testPFHConly \
-i ${INPDIR}/test_defaultJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'HLT_default':1:1:26 \
   ${INPDIR}/test_offlineJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Offline':632:1:26 \
   ${INPDIR}/test_offlineSkipFwdJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Offline_SkipFwd':800:1:26 \
-l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD Winter23 FlatPt'

jmePlots.py -k compare_PFCalo_PFHC_Corrected  \
-o ./plots_testPFHConly_Corrected \
-i ${INPDIR}/test_defaultJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'HLT_default':1:1:26 \
   ${INPDIR}/test_offlineJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Offline':632:1:26 \
   ${INPDIR}/test_offlineSkipFwdJECs/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Offline_SkipFwd':800:1:26 \
-l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD Winter23 FlatPt'

# jmePlots.py -k compare_PFCalo_PFHC  \
# -o ${OUTDIR} \
# -i ${INPDIR}/test_hlt_pfhc/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'HLT PFHC':1:1:26 \
#    ${INPDIR}/test_offline_pfhc/HLT_Run3TRK/harvesting/Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65.root:'Offline PFHC':632:1:26 \
# -l '#font[61]{CMS} #font[52]{Run-3 Simulation} QCD Winter23 FlatPt'

# organize plots into folders

Regions=(
EtaIncl
HB
HE1
HE2
HF
#MET
)

for region_name in "${Regions[@]}"; do
  mkdir -p plots_testPFHConly/NoSelection/${region_name}
  mv plots_testPFHConly/NoSelection/*${region_name}*.png plots_testPFHConly/NoSelection/${region_name}
  mkdir -p plots_testPFHConly_Corrected/NoSelection/${region_name}
  mv plots_testPFHConly_Corrected/NoSelection/*${region_name}*.png plots_testPFHConly_Corrected/NoSelection/${region_name}
done


# for region_name in "${Regions[@]}"; do
#   mkdir -p ${OUTDIR}/NoSelection/${region_name}
#   mv ${OUTDIR}/NoSelection/*${region_name}*.png ${OUTDIR}/NoSelection/${region_name}
# done

unset INPDIR region_name Regions OUTDIR pt_region_number