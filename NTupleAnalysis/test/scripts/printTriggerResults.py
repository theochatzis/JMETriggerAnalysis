#!/usr/bin/env python
"""Prints TriggerResults in the given event.
Example call:
  ./printTriggerResults.py root://cmsxrootd.fnal.gov//store/data/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/10000/00006301-CAA8-E511-AD39-549F35AD8BC9.root 259861:162358311
"""
import argparse
#import re
import ROOT
from DataFormats import FWLite

if __name__ == '__main__':
   # Parse input arguments
   argParser = argparse.ArgumentParser(description=__doc__)
   argParser.add_argument('inputFile', help='Input MiniAOD file')
#   argParser.add_argument('event', help='ID of event to be selected, run:lumi:event')
   argParser.add_argument('-l', '--label', default='TriggerResults::HLT', help='Label to access trigger results')
   args = argParser.parse_args()

#   # Parse ID of event to be selected
#   eventIDRegex = re.compile(r'^(\d+):(\d+):(\d+)$')
#   match = re.match(eventIDRegex, args.event)
#   if not match:
#       raise RuntimeError('Failed to parse event ID "{}".'.format(args.event))
#   else:
#       eventToSelect = (int(match.group(1)), int(match.group(2)), int(match.group(3)))

   # Allow loading CMSSW classes
   ROOT.gSystem.Load('libFWCoreFWLite.so')
   ROOT.FWLiteEnabler.enable()
   ROOT.gSystem.Load('libDataFormatsFWLite.so')

   # Open input file
   events = FWLite.Events(args.inputFile)

   # Read events
   triggerResultsHandle = FWLite.Handle('edm::TriggerResults')

   triggerAcceptDict = {}
   for event in events:

#       # Skip to the desired event
#       if event.eventAuxiliary().run() != eventToSelect[0] or \
#          event.eventAuxiliary().luminosityBlock() != eventToSelect[1] or \
#          event.eventAuxiliary().event() != eventToSelect[2]:
#          continue

       # Read trigger results in the selected event
       event.getByLabel(args.label, triggerResultsHandle)
       triggerResults = triggerResultsHandle.product()
       triggerNames = event.object().triggerNames(triggerResults)

       for i in range(triggerResults.size()):

           if triggerNames.triggerName(i) not in triggerAcceptDict:
              triggerAcceptDict[triggerNames.triggerName(i)] = 0

           if triggerResults.accept(i):
              triggerAcceptDict[triggerNames.triggerName(i)] += 1

   # print results
   for _tmp in sorted(triggerAcceptDict):
       print '{:<100} {:>5}'.format(_tmp, triggerAcceptDict[_tmp])
