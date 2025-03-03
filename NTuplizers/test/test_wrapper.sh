#!/bin/bash

set -e

cd ${CMSSW_BASE}/src
git checkout from-${CMSSW_VERSION}
scram b &> /dev/null
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test
printf "%s\n" "--- REFE ---"
for nnn in {0..0}; do
  printf "%s\n" "old_${nnn}"
  ./test.sh 0 old_${nnn}.root &> old_${nnn}.txt
  grep -inr pfPuppi old_${nnn}.txt | grep FastReport
  rm -f old_${nnn}.root.txt
  printTTree -i old_${nnn}.root -o old_${nnn}.root.txt -t puppiNTuple/Events
done; unset nnn;

cd ${CMSSW_BASE}/src
git checkout devel_112X_puppi_speedup2
scram b &> /dev/null
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test
printf "%s\n" "--- TARG ---"
for nnn in {0..0}; do
  printf "%s\n" "new_${nnn}"
  ./test.sh 0 new_${nnn}.root &> new_${nnn}.txt
  grep -inr pfPuppi new_${nnn}.txt | grep FastReport
  rm -f new_${nnn}.root.txt
  printTTree -i new_${nnn}.root -o new_${nnn}.root.txt -t puppiNTuple/Events
done; unset nnn;
