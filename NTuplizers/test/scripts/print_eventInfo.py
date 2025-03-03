#!/usr/bin/env python
import argparse
import os
import glob
import array
import copy
import math
import ROOT
import uproot

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=None,
                       help='path to input .root file(s)')

   parser.add_argument('-t', '--tree', dest='tree', action='store', default='JMETriggerNTuple/Events',
                       help='key of TTree in input file(s)')

   parser.add_argument('-n', '--nevents', dest='nevents', action='store', type=int, default=-1,
                       help='number of events')

   parser.add_argument('-e', '--every', dest='every', action='store', type=int, default=1e2,
                       help='show progress of processing every N events')

   parser.add_argument('-r', '--response', dest='response', action='store', default='',
                       help='response')

#   parser.add_argument('-f', '--firstEvent', dest='firstEvent', action='store', type=int, default=0,
#                       help='index of first event to be processed (inclusive)')
#
#   parser.add_argument('-l', '--lastEvent', dest='lastEvent', action='store', type=int, default=-1,
#                       help='index of last event to be processed (inclusive)')
#
#   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
#                       help='enable verbose mode')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   ROOT.gROOT.SetBatch()
   ROOT.gErrorIgnoreLevel = ROOT.kError #kWarning

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation ---
   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   INPUT_FILES = []
   for i_inpf in opts.inputs:
       i_inpf_ls = glob.glob(i_inpf)
       for i_inpf_2 in i_inpf_ls:
           if os.path.isfile(i_inpf_2):
              INPUT_FILES += [os.path.abspath(os.path.realpath(i_inpf_2))]
   INPUT_FILES = sorted(list(set(INPUT_FILES)))

   if len(INPUT_FILES) == 0:
      KILL(log_prx+'empty list of input files [-i]')

   SHOW_EVERY = opts.every
   if SHOW_EVERY <= 0:
      WARNING(log_prx+'invalid (non-positive) value for option "-e/--every" ('+str(SHOW_EVERY)+'), value will be changed to 100')
      SHOW_EVERY = 1e2
   ### -------------------

   collections = [
     'hltPFMET_pt',
     'hltPFCHSv1MET_pt',
     'hltPFCHSv2MET_pt',
     'hltPFSoftKillerMET_pt',
     'hltPuppiV1MET_pt',
     'hltPuppiV2MET_pt',
     'hltPuppiV3MET_pt',
     'hltPuppiV4MET_pt',
     'offlinePFMET_Raw_pt',
     'offlinePFMET_Type1_pt',
     'offlinePuppiMET_Raw_pt',
     'offlinePuppiMET_Type1_pt',
   ]

   values = {}
   for _tmp in collections:
       values[_tmp] = []

   nEvtProcessed = 0

   for i_inpf in INPUT_FILES:

       if (opts.nevents >= 0) and (nEvtProcessed >= opts.nevents): break

#       if opts.verbose:
#          print colored_text('[input]', ['1','92']), os.path.relpath(i_inpf)

       i_tfile = ROOT.TFile.Open(i_inpf)
       if not i_tfile: continue

       i_ttree = i_tfile.Get(opts.tree)
       if not i_ttree: continue

       i_ttree.SetBranchStatus('*', False)
       for _tmp in collections:
           i_ttree.SetBranchStatus('*', True)

       for i_evt in i_ttree:

           for _tmp in collections:
               if hasattr(i_evt, _tmp):
                  if hasattr(i_evt, opts.response):
                     values[_tmp] += [getattr(i_evt, _tmp)[0] / getattr(i_evt, opts.response)[0]]
                  else:
                     values[_tmp] += [getattr(i_evt, _tmp)[0]]

           nEvtProcessed += 1
           if (opts.nevents >= 0) and (nEvtProcessed >= opts.nevents): break

#           if not (evt_idx % SHOW_EVERY) and (evt_idx > 0):
#              print colored_text('['+str(os.path.relpath(opts.output))+']', ['1','93']), 'events processed:', evt_idx

       i_tfile.Close()

   print '-'*100
   print 'events processed:', nEvtProcessed
   print '-'*100

   def mean(values):
       if len(values) < 1: return -1.
       return sum(values)/len(values)

   def rms(values):
       if len(values) < 2: return -1.
       _mean = mean(values)
       _ret = 0.
       for _tmp in values:
          _ret += (_tmp - _mean)*(_tmp- _mean)
       _ret /= len(values)-1
       return math.sqrt(_ret)

   for _tmp in collections:
       mean_val = mean(values[_tmp])
       rms_val = rms(values[_tmp])
       print '{:<30} {:>10.3f} {:>10.3f}'.format(_tmp, mean_val, rms_val/mean_val)
