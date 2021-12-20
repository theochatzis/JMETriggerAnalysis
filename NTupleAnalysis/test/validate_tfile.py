#!/usr/bin/env python
import os
import argparse
import glob
import array
import re
import ROOT

from common.utils import *

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser(description=__doc__)

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=[],
                       help='paths to output directories of crab3-task (Tier-2)')

   parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                       help='verbosity level')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   log_prx = os.path.basename(__file__)+' -- '

   ROOT.gROOT.SetBatch()

   ### args validation ---

   # inputs
   INPUT_DIRS = []
   for i_inp in opts.inputs:
       i_inp_ls = glob.glob(i_inp)
       for i_inp_2 in i_inp_ls:
           if os.path.isfile(i_inp_2):
              INPUT_DIRS += [os.path.abspath(os.path.realpath(i_inp_2))]
           elif opts.verbosity > 0:
              WARNING(log_prx+'target input path is not a directory (will be skipped): '+i_inp_2)

   INPUT_DIRS = sorted(list(set(INPUT_DIRS)))

   if len(INPUT_DIRS) == 0:
     KILL(log_prx+'empty list of input directories')

   testFailed = 0
   for fi in INPUT_DIRS:
     _tf = ROOT.TFile.Open(fi)
     if (not _tf) or _tf.IsZombie() or _tf.TestBit(ROOT.TFile.kRecovered):
       testFailed = 1
       ffi = fi.replace('/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/JetMET_PhaseII/JMETriggerAnalysis_phase2/ntuples/output_hltPhase2_201209/HLT_TRKv06p1_TICL', '/afs/cern.ch/work/m/missirol/private/jmeTrigger/phase2/CMSSW_11_1_3_Patatrack/src/JMETriggerAnalysis/NTuplizers/test/output_hltPhase2_201209/HLT_TRKv06p1_TICL').replace('/out_', '/job_').replace('.root', '/flag.done')
       print ffi
       continue
#     _tf.Close()
