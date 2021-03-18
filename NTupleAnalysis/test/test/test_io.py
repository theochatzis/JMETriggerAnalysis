#!/usr/bin/env python
from __future__ import print_function

UPROOT = 1

import time
start = time.time()

import ROOT
import glob

if __name__ == '__main__':

   VERBOSE = False

   num_maxEvents = 100000

   NUM_EVENTS_PROCESSED = 0

   INPUT_FILES = glob.glob('/pnfs/desy.de/cms/tier2/store/user/missirol/jme_trigger/jmeTriggerNtuples/pfMET/v02/191103/Data_Run2018B_EGamma/*/*/*/*/*.root')

   output = 'test'

   for i_inpf in INPUT_FILES:

       if VERBOSE: print('\033[1m'+'\033[92m'+'[input]'+'\033[0m', i_inpf)

       stop_exe = False
   
       if UPROOT:
          import uproot

          i_ttree = uproot.open(i_inpf)['JMETriggerNTuple/Events']

          i_firstEvent = 0
          i_lastEvent = min(num_maxEvents - NUM_EVENTS_PROCESSED, i_ttree.numentries) if (num_maxEvents >= 0) else i_ttree.numentries

          hltPuppiMET_pt = i_ttree.arrays('*', entrystart=i_firstEvent, entrystop=i_lastEvent)

          for i_ent in range(i_firstEvent, i_lastEvent):

              a = hltPuppiMET_pt['hltPuppiMET_pt'][i_ent]

              if (num_maxEvents >= 0) and (NUM_EVENTS_PROCESSED >= num_maxEvents):
                 stop_exe = True
                 break

#              analyze_event(event=i_evt, th1s=th1s, th2s=th2s)

              NUM_EVENTS_PROCESSED += 1

              if not (NUM_EVENTS_PROCESSED % 1e5):
                 print('\033[1m'+'\033[93m'+'['+str(output)+']'+'\033[0m', 'processed events:', NUM_EVENTS_PROCESSED)

       else:
          i_inptfile = ROOT.TFile.Open(i_inpf)
          if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
             WARNING(log_prx+'path to input file is not valid, or TFile is corrupted (file will be ignored) [-i]: '+i_inpf)
             continue
   
          i_ttree = i_inptfile.Get('JMETriggerNTuple/Events')
          if not i_ttree:
             WARNING(log_prx+'target TFile does not contain a TTree named "'+tree+'" (file will be ignored) [-t]: '+i_inpf)
             continue
   
          for i_evt in i_ttree:
   
              a = i_evt.hltPuppiMET_pt

              if (num_maxEvents >= 0) and (NUM_EVENTS_PROCESSED >= num_maxEvents):
                 stop_exe = True
                 break

#              analyze_event(event=i_evt, th1s=th1s, th2s=th2s)

              NUM_EVENTS_PROCESSED += 1

              if not (NUM_EVENTS_PROCESSED % 1e5):
                 print('\033[1m'+'\033[93m'+'['+str(output)+']'+'\033[0m', 'processed events:', NUM_EVENTS_PROCESSED)

#       ROOT.gROOT.GetListOfFiles().Remove(i_inptfile)
#       i_inptfile.Close()

       if stop_exe: break

   time_sec = (time.time() - start)
   print(time_sec)
