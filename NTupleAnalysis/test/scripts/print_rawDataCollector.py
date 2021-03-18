#!/usr/bin/env python
"""
Example call:
  ./print_rawDataCollector.py root://cmsxrootd.fnal.gov//store/data/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/10000/00006301-CAA8-E511-AD39-549F35AD8BC9.root
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
   argParser.add_argument('-l', '--label', default='rawDataCollector::DIGI2RAW', help='Label')
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
   fedRawDataCollectionHandle = FWLite.Handle('FEDRawDataCollection')

   triggerAcceptDict = {}
   for event in events:

#       # Skip to the desired event
#       if event.eventAuxiliary().run() != eventToSelect[0] or \
#          event.eventAuxiliary().luminosityBlock() != eventToSelect[1] or \
#          event.eventAuxiliary().event() != eventToSelect[2]:
#          continue

       # Read trigger results in the selected event
       event.getByLabel(args.label, fedRawDataCollectionHandle)
       fedRawDataCollection = fedRawDataCollectionHandle.product()

       for iii in range(700, 731+1) + range(1100, 1199+1):
           for jjj in range(fedRawDataCollection.FEDData(iii).size()):
               print '{:>9d} {:>9d} {:>9d}'.format(iii, jjj, fedRawDataCollection.FEDData(iii).data()[jjj])

#       for i in range(fedRawDataCollection.size()):
#           print i

       break
