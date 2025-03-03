#!/bin/bash
# source TTbarSR_driver.sh $FILEBOX/vXX/ntuples/ntuple . tmp

if [ $# -ne 3 ]; then
  echo ""
  echo " @@@ FATAL -- stopping execution: incorrect command-line arguments."
  echo "             [1] input file(s) prefix"
  echo "             [2] output directory"
  echo "             [3] output file(s) prefix"
  echo ""
  return
fi

IPREX=$1
OPATH=$2
OPREX=$3

for cha in muon elec; do

  mkdir -p "$OPATH"/$cha

  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.TTJets_mg5__phys14_pu20bx25.root

  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.WJets_HT100to200_mg5__phys14_pu20bx25.root
  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.WJets_HT200to400_mg5__phys14_pu20bx25.root
  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.WJets_HT400to600_mg5__phys14_pu20bx25.root
  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.WJets_HT600toINF_mg5__phys14_pu20bx25.root

  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.DYJets_HT100to200_mg5__phys14_pu20bx25.root
  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.DYJets_HT200to400_mg5__phys14_pu20bx25.root
  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.DYJets_HT400to600_mg5__phys14_pu20bx25.root
  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.DYJets_HT600toINF_mg5__phys14_pu20bx25.root

  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.Zp_M1000w01p__phys14_pu20bx25.root
  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.Zp_M2000w01p__phys14_pu20bx25.root
  ./bin/TTbarSR $cha "$IPREX" "$OPATH"/$cha/"$OPREX" .MC.Zp_M3000w01p__phys14_pu20bx25.root

done

unset -v IPREX OPATH OPREX
