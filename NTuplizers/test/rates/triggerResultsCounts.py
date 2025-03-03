#!/usr/bin/env python
"""
Script to write to a .json file the raw and pure counts of HLT accepts
from the edm::TriggerResults of one or more EDM files

This script is a simplified version of
https://github.com/cms-steam/SteamRatesEdmWorkflow/blob/2c197201a810ed8ff95aaa55a17722c3722dfc3e/Rates/triggerCountsFromTriggerResults.py
"""
import os
import argparse
import json
import ROOT

from DataFormats.FWLite import Handle, Events

if __name__ == '__main__':
   ### args
   parser = argparse.ArgumentParser(
    prog='./'+os.path.basename(__file__),
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__)

   parser.add_argument('-i', '--input-files', dest='input_files', nargs='+', default=[], required=True,
                       help='list of paths to EDM input files')

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                       help='path to output file (.json format)')

   parser.add_argument('-l', '--lumi-json', dest='lumi_json', action='store', default=None,
                       help='path to file with dictionary of valid run:luminosityBlock values (.json format)')

   parser.add_argument('-t', '--triggers-json', dest='triggers_json', action='store', default=None,
                       help='path to file with list of HLT paths to be used for pure counts (.json format)')

   parser.add_argument('-p', '--processName', dest='processName', action='store', default='HLTX',
                       help='process name of edm::TriggerResults in EDM input file(s)')

   parser.add_argument('-m', '--maxEvents', dest='maxEvents', action='store', type=int, default=-1,
                       help='maximum number of events to be processed')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')

   parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', type=int, default=0, const=1,
                       help='level of verbosity (default: 0)')

   opts, opts_unknown = parser.parse_known_args()
   ### ----

   log_prx = os.path.basename(__file__)+' -- '

   if len(opts_unknown) > 0:
     raise RuntimeError(log_prx+'unsupported command-line arguments: '+str(opts_unknown))

   if 'CMSSW_BASE' not in os.environ:
     raise RuntimeError(log_prx+'environment variable CMSSW_BASE is not defined (set up CMSSW environment with "cmsenv"')

   if os.path.exists(opts.output):
     raise RuntimeError(log_prx+'target path to output file already exists [-o]: '+str(opts.output))

   triggerBits = Handle('edm::TriggerResults')
   triggerBitLabel = 'TriggerResults::'+opts.processName

   goodLSDict = None
   if opts.lumi_json is not None:
     goodLSDict = json.load(open(opts.lumi_json, 'r'))

   triggersForPureCounts = None
   if opts.triggers_json is not None:
     triggersForPureCounts = json.load(open(opts.triggers_json, 'r'))

   rateDict = {}
   nEvents = 0

   for inputFile in opts.input_files:

     if opts.verbosity > 0:
       print 'File =', inputFile

     events = Events(inputFile)
     for event in events:

       if opts.maxEvents >= 0 and nEvents >= opts.maxEvents: 
         break

       runnbr = event.object().id().run()
       runls = event.object().id().luminosityBlock()

       if goodLSDict is not None:
         goodLS = False
         if str(runnbr) in goodLSDict:
           for part_LS in goodLSDict[str(runnbr)]:
             if runls >= part_LS[0] and runls <= part_LS[1]:
               goodLS = True
               break
         if not goodLS: continue

       nEvents += 1
       if opts.verbosity > 0 and nEvents%1000 == 0:
         print 'Processing entry ', nEvents
   
       if runnbr not in rateDict:
         rateDict[runnbr] = {}
   
       event.getByLabel(triggerBitLabel, triggerBits)
       names = event.object().triggerNames(triggerBits.product())
   
       if runls not in rateDict[runnbr]:
         rateDict[runnbr][runls] = {'numberOfEvents': 0, 'pathAcceptsRawAndPure': {}}
         for name in names.triggerNames():
           name = str(name)
           if 'HLTriggerFirstPath' in name or 'HLTriggerFinalPath' in name: continue
           rateDict[runnbr][runls]['pathAcceptsRawAndPure'][name] = [0, 0]

       triggersFired = []
       triggerCounts = 0
       for triggerName in rateDict[runnbr][runls]['pathAcceptsRawAndPure']:
         index = names.triggerIndex(triggerName)
         if index >= names.triggerNames().size(): raise RuntimeError(name)

         if triggerBits.product().accept(index):
           triggersFired.append(triggerName)
           if triggerName.startswith('HLT_'):
             if triggersForPureCounts is None or triggerName in triggersForPureCounts:
               triggerCounts += 1

       for triggerName in rateDict[runnbr][runls]['pathAcceptsRawAndPure']:
         if triggerName not in triggersFired: continue
         rateDict[runnbr][runls]['pathAcceptsRawAndPure'][triggerName][0] += 1

         if triggerName.startswith('HLT_IsoMu24_v'): print triggersFired, triggerCounts

         if triggerCounts != 1 or not triggerName.startswith('HLT_'): continue
         rateDict[runnbr][runls]['pathAcceptsRawAndPure'][triggerName][1] += 1

       rateDict[runnbr][runls]['numberOfEvents'] += 1

   if not opts.dry_run:
     json.dump(rateDict, open(opts.output, 'w'), sort_keys=True, indent=2)
