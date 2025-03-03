#!/bin/bash

NREPS=100
INTSEC=1200

if [ $# -ge 2 ]; then
  NREPS=$1
  INTSEC=$2
elif [ $# -eq 1 ]; then
  NREPS=$1
fi

condor_release ${USER}

for tmp in {0..${NREPS}}; do
  sleep ${INTSEC}
  condor_release ${USER}
done
unset -v tmp

unset -v NREPS INTSEC
