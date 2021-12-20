#!/bin/bash

EXE='root -l -b -q'

ODIR=$1

mkdir -p "$ODIR"/muon "$ODIR"/elec

cp dumperLI.C dumperLI.h "$ODIR"

$EXE 'dumperLI_exe.C("muon", "../../../filebox/nak/leptonISO/ntuples/ntupleLI", "'"$ODIR"'/muon/dump_LI")'
$EXE 'dumperLI_exe.C("elec", "../../../filebox/nak/leptonISO/ntuples/ntupleLI", "'"$ODIR"'/elec/dump_LI")'

rm *.d *.so

unset -v EXE ODIR
