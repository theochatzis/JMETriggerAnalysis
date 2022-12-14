#/bin/bash


# define the samples you want to use
Regions=(
EtaIncl
HB
HE1
HE2
HF
#MET
)

IDIR=$1

for region_name in "${Regions[@]}"; do
  mkdir ${IDIR}/${region_name}
  mv ${IDIR}/*${region_name}*.png ${IDIR}/${region_name}
  #if [ ${region_name} != "MET" ]; then
  #  for pt_region_number in {0..4}; do
  #    mkdir ${IDIR}/${region_name}/${region_name}Pt${pt_region_number}
  #    mv ${IDIR}/${region_name}/*${region_name}Pt${pt_region_number}*.png ${IDIR}/${region_name}/${region_name}Pt${pt_region_number}
  #  done
  #fi
done

unset region_name Regions IDIR pt_region_number

