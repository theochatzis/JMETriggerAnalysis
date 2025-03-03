#!/bin/bash

if [ ! -d "${t3out}" ]; then
  exit 1
fi

./triggersForPureRate.py

for inpd in $(ls -d "${t3out}"/*); do
  outf=rates_$(basename "${inpd}")
  [ -f "${outf}".json ] || ./triggerResultsCounts.py \
    -i "${inpd}"/*/job_*/out_*.root \
    -t triggersForPureRate.json \
    -l json_323775.txt \
    -o "${outf}".json \
    -p HLTX \
    -v 1

  ./triggerRates.py \
    -p 1100 -t 'HLT_PFJet*' 'HLT_PFHT*' 'HLT_PFMET*' \
    -i "${outf}".json > "${outf}".txt
done

#python mergeOutputs.py -l 1. -t 1. -p 1100
#23.31
