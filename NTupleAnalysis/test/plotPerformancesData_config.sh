#!/bin/bash
source env.sh

# directory with input(s) 
INPDIR=/eos/user/t/tchatzis/samples2023/


#OUTDIR=./plots_test_winter24
OUTDIR=/eos/user/t/tchatzis/plots_calo_thresholds/



rm -rf ${OUTDIR}


jmePlots.py -k version_check_data_new \
-o ${OUTDIR} \
-i /eos/user/t/tchatzis/samples2023/test_calojet_default/harvesting/data.root:'Default CaloTower':1:1:20 \
   /eos/user/t/tchatzis/samples2023/test_calojet_ecal_thresh/harvesting/data.root:'PF RecHit Threshold':632:1:20 \
-l '#font[61]{CMS} #font[52]{Run-3 Data} Muon Dataset (Era G)'

# jmePlots.py -k version_check_data_new \
# -o ${OUTDIR} \
# -i /eos/user/t/tchatzis/samples2023/before_fpix_default/harvesting/data.root:'No FPix issue':632:1:20 \
#    /eos/user/t/tchatzis/samples2023/after_fpix_default/harvesting/data.root:'FPix issue (w/o doublets)':800:1:20 \
#    /eos/user/t/tchatzis/samples2023/after_fpix_doublet/harvesting/data.root:'FPix issue (w/ doublets)':1:1:20 \
# -l '#font[61]{CMS} #font[52]{Run-3 Data} EphemeralHLTPhysics Era F'


rm ${OUTDIR}/NoSelection/*mass*.png
#rm ${OUTDIR}/NoSelection/*MatchedTo*_pt_over*.png

# organize plots into folders

Regions=(
EtaIncl_
HB_
HBPt0_
HBPt1_
HBPt2_
HBPt3_
HEPt0_
HEPt1_
HEPt2_
HEPt3_
HE1_
HE2_
HF_
# BPix_plus4_
# BPix_minus4_
# BPix_plus8_
# BPix_minus8_
BPix_
BPixVeto_
FPix_
FPixVeto_
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

#rm ${OUTDIR}/NoSelection/*.png

unset INPDIR region_name Regions OUTDIR pt_region_number
