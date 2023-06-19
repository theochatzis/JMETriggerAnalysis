#!/bin/bash
source env.sh

# directory with input(s) 
INPDIR=/eos/user/t/tchatzis/samples2023/test_dataG_2023eta2p4


OUTDIR=./versionCheckPlots_2023Data_fix_150GeV


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


jmePlots.py -k version_check_data  \
-o ${OUTDIR} \
-i /eos/user/t/tchatzis/samples2023/test_dataG_new2023/hcal_jecs2023/harvesting/data.root:'PFHC |#eta|<2.75':1:1:26 \
   /eos/user/t/tchatzis/samples2023/test_dataG_2023eta2p4/hcal_jecs2023/harvesting/data.root:'PFHC |#eta|<2.4':632:1:26 \
-l '#font[61]{CMS} #font[52]{Run-3 Data} JetMET 2022 RunG'

# organize plots into folders

Regions=(
EtaIncl
HB
HE1
HE2
HF
MET
)



for region_name in "${Regions[@]}"; do
  mkdir -p ${OUTDIR}/NoSelection/${region_name}
  mv ${OUTDIR}/NoSelection/*${region_name}*.png ${OUTDIR}/NoSelection/${region_name}
done

unset INPDIR region_name Regions OUTDIR pt_region_number