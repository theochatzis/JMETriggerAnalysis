#!/bin/bash

if [ $# -ne 2 ]; then
  printf "%s\n" "specify [1] if igprof shall be used (0,1), and [2] the name of the output file"
#  printf "%s\n" "specify if igprof shall be used [1/0] and the number of threads/streams [int]"
  exit 1
fi

IGPROF=${1}
OUTFILE=${2}
NTHREADS=1 #4 #${2}

#EXE="cmsRun jmeTriggerNTuple_cfg.py inputFiles=file:1E007C6B-0236-774C-AE76-16FF40129ED8.root secondaryInputFiles=None printSummaries=1 maxEvents=2 numThreads=${NTHREADS} numStreams=0 wantSummary=1 output=${OUTFILE}"
#EXE="cmsRun testPuppiOnRECO_cfg.py inputFiles=file:972E4466-10B8-1345-A0F9-8ECBF8D1D772.root printSummaries=1 maxEvents=1 numThreads=${NTHREADS} numStreams=0 wantSummary=0 output=${OUTFILE}"

EXE="./testPuppiInRECO_mcRun3_cmsDriver.sh ${OUTFILE}"
#EXE="./testPuppiInRECO_mcRun4_cmsDriver.sh ${OUTFILE}"

if [ ${IGPROF} -ne 0 ]; then
  igprof -t cmsRun -pp -z -o igprof.pp.gz ${EXE}
  igprof-analyse -d -v -g igprof.pp.gz &> igprof.pp.txt
# igprof-analyse --sqlite -d -v -g igprof.pp.gz | sqlite3 igprof_analyse.pp.sql3
  rm igprof.pp.gz
else
  ${EXE}
#  taskset -c 0-3 ${EXE}
fi
