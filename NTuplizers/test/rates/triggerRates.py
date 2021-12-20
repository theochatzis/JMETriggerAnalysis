#!/usr/bin/env python
"""
Script to print trigger rates from a collection of .json files
"""
import os
import argparse
import json
import math
import fnmatch

if __name__ == '__main__':
   ### args
   parser = argparse.ArgumentParser(
    prog='./'+os.path.basename(__file__),
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__)

   parser.add_argument('-i', '--input-files', dest='input_files', nargs='+', default=[], required=True,
                       help='list of paths to EDM input files')

#   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
#                       help='path to output file (.json format)')

   parser.add_argument('-t', '--triggers-only', dest='triggers_only', nargs='+', default=[],
                       help='')

   parser.add_argument('-p', '--prescale-factor', dest='prescale_factor', action='store', type=int, default=1,
                       help='')

   parser.add_argument('-l', '--ls-time', dest='ls_time', action='store', type=float, default=23.31,
                       help='duration of a luminosity section in seconds')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')

   parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', type=int, default=0, const=1,
                       help='level of verbosity (default: 0)')

   opts, opts_unknown = parser.parse_known_args()
   ### ----

   log_prx = os.path.basename(__file__)+' -- '

   if len(opts_unknown) > 0:
     raise RuntimeError(log_prx+'unsupported command-line arguments: '+str(opts_unknown))

   ratesDict = {}
   trigList = []
   lsList = []

   for inputFile in opts.input_files:

     if opts.verbosity > 0:
       print 'File =', inputFile

     countsDict = json.load(open(inputFile, 'r'))
     for runStr in countsDict:
       for lsStr in countsDict[runStr]:
         lsList.append(runStr+':'+lsStr)

         countsPerTrigDict = countsDict[runStr][lsStr]['pathAcceptsRawAndPure']

         trigList_i = []
         for trig_i in countsPerTrigDict.keys():
           if opts.triggers_only:
             keepTrig = False
             for trigMatch_i in opts.triggers_only:
               if fnmatch.fnmatch(trig_i, trigMatch_i):
                 keepTrig = True
             if not keepTrig: continue
           trigList_i.append(trig_i)
         trigList_i = sorted(trigList_i)

         if len(trigList) == 0:
           trigList = trigList_i[:]
         elif trigList_i != trigList:
           raise RuntimeError('different list of triggers (not supported yet)')

         prescale_factor = countsDict[runStr][lsStr]['HLTPhysicsPrescale'] \
           if 'HLTPhysicsPrescale' in countsDict[runStr][lsStr] else opts.prescale_factor

         for trig_i in trigList:
           if trig_i not in ratesDict: ratesDict[trig_i] = [0, 0]
           ratesDict[trig_i][0] += countsPerTrigDict[trig_i][0] * prescale_factor
           ratesDict[trig_i][1] += countsPerTrigDict[trig_i][1] * prescale_factor

   lsList = list(set(lsList))
   totTime = opts.ls_time * len(lsList)
   if totTime <= 0.:
     raise RuntimeError('non-positive time')

   for trig_i in trigList:
     countRaw_i = ratesDict[trig_i][0]
     countRawErr_i = math.sqrt(countRaw_i)

     countPure_i = ratesDict[trig_i][1]
     countPureErr_i = math.sqrt(countPure_i)

     rateRaw_i = countRaw_i / totTime
     rateRawErr_i = countRawErr_i / totTime

     ratePure_i = countPure_i / totTime
     ratePureErr_i = countPureErr_i / totTime

     print '| {: <90} | {:>8.2f} +/- {:>8.2f} ({:>9d}) | {:>8.2f} +/- {:>8.2f} ({:>9d}) |'.format(trig_i, rateRaw_i, rateRawErr_i, countRaw_i, ratePure_i, ratePureErr_i, countPure_i)
