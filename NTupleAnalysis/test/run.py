#!/usr/bin/env python3
from __future__ import print_function
import argparse
import os
import glob
import time
import ROOT

def colored_text(txt, keys=[]):
    _tmp_out = ''
    for _i_tmp in keys:
        _tmp_out += '\033['+_i_tmp+'m'
    _tmp_out += txt
    if len(keys) > 0: _tmp_out += '\033[0m'
    return _tmp_out

def EXE(cmd, suspend=True, verbose=False, dry_run=False):
    if verbose: print(colored_text('>', ['1']), cmd)
    if dry_run: return
    _exitcode = os.system(cmd)
    _exitcode = min(255, _exitcode)
    if _exitcode and suspend:
       raise SystemExit(_exitcode)
    return _exitcode

#### main
if __name__ == '__main__':
   time_start = time.time()

   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=None,
                       help='path to input files (can also include TTree key, as "FILE:KEY"; if not specified, TTree key is taken from --tree)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default=None,
                       help='path to output .root file')

   parser.add_argument('-t', '--tree', dest='tree', action='store', default='JMETriggerNTuple/Events',
                       help='key of TTree in input file(s)')

   parser.add_argument('--options', dest='options', nargs='+', default=[],
                       help='list of plugin options (format: "option1=value1 option2=value2 [..]")')

   parser.add_argument('-l', '--libs', dest='libs', nargs='+', default=[],
                       help='names of libraries to be loaded via ROOT::gSystem::Load')

   parser.add_argument('-p', '--plugin', dest='plugin', action='store', default=None, required=True,
                       help='name of analysis plugin')

   parser.add_argument('-e', '--every', dest='every', action='store', type=int, default=1e2,
                       help='show progress of processing every N events')

   parser.add_argument('-s', '--skipEvents', dest='skipEvents', action='store', type=int, default=0,
                       help='number of events to be skipped from start of input TTree')

   parser.add_argument('-m', '--maxEvents', dest='maxEvents', action='store', type=int, default=-1,
                       help='maximum number of events to be processed')

   parser.add_argument('-v', '--verbosity', dest='verbosity', action='store', type=int, default=-1,
                       help='level of verbosity of output')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   ROOT.gROOT.SetBatch()
   ROOT.gErrorIgnoreLevel = ROOT.kError #kWarning

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation ---

   ## unknown
   if len(opts_unknown) > 0:
      raise RuntimeError(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   ## output
   if os.path.exists(opts.output):
      raise RuntimeError(log_prx+'target path to output .root file already exists [-o]: '+opts.output)

   ## options
   optionsDict = {}
   for i_opt in opts.options:
       i_opt_split = i_opt.split('=')

       if len(i_opt_split) != 2:
          WARNING(log_prx+'plugin option with invalid format (will be ignored) [--options]: '+i_opt)
          continue

       if i_opt_split[0] in optionsDict:
          KILL(log_prx+'attempt to redefine plugin option [--options]: '+i_opt_split[0])

       optionsDict[i_opt_split[0]] = i_opt_split[1]

   ## libraries
   LIBS = sorted(list(set(opts.libs)))
   for _tmp in LIBS:
       if ROOT.gSystem.Load(_tmp):
          print(log_prx+'failed to load library via ROOT::gSystem::Load [-l]: '+_tmp)

   ## plugin
   if not hasattr(ROOT, opts.plugin):
      raise RuntimeError(log_prx+'analysis plugin unavailable [-p]: '+opts.plugin)

   ## inputs
   inputFileTreePairs = []

   for i_inpf in opts.inputs:

       i_inpf_fpath, i_inpf_treekey = None, None

       i_inpf_split = i_inpf.split(':')

       if len(i_inpf_split) == 1:
          i_inpf_fpath = i_inpf_split[0]
          i_inpf_treekey = opts.tree

       elif len(i_inpf_split) == 2:
          i_inpf_fpath = i_inpf_split[0]
          i_inpf_treekey = i_inpf_split[1]

       else:
          print(log_prx+'invalid format for input entry (will be skipped): '+i_inpf)
          continue

       i_inpf_ls = glob.glob(i_inpf_fpath)

       for i_inpf_2 in i_inpf_ls:
           if os.path.isfile(i_inpf_2):
              inputFileTreePairs += [(os.path.abspath(os.path.realpath(i_inpf_2)), i_inpf_treekey)]
           elif opts.verbosity > 0:
              print(log_prx+'invalid path to input file (input entry will be skipped) [-i]: '+i_inpf_2)

   inputFileTreePairs = sorted(list(set(inputFileTreePairs)))

   if len(inputFileTreePairs) == 0:
      raise RuntimeError(log_prx+'empty list of valid input entries [-i]')

   ## show-every flag
   SHOW_EVERY = opts.every
   if SHOW_EVERY <= 0:
      print(log_prx+'invalid (non-positive) value for option "-e/--every" ('+str(SHOW_EVERY)+'), value will be changed to 100')
      SHOW_EVERY = 1e2
   ### -------------------

   ## create output directory
   output_dirname = os.path.dirname(os.path.abspath(opts.output))
   if not os.path.isdir(output_dirname):
      EXE('mkdir -p '+output_dirname, verbose=options.verbosity > 0, dry_run=options.dry_run)
   del output_dirname

   skipEvents = opts.skipEvents
   if (skipEvents != 0) and (len(inputFileTreePairs) != 1):
      raise RuntimeError(log_prx+' -- invalid argument of --skipEvents option (non-zero value not supported for multiple input files)')

   if opts.verbosity > -99:
      print('-'*50)
      print(colored_text('[plugin]', ['1']), opts.plugin)

   analyzer = getattr(ROOT, opts.plugin)(opts.output, 'recreate')
   analyzer.setVerbosity(opts.verbosity)
   analyzer.addOption('showEvery', str(SHOW_EVERY))
   for i_opt in optionsDict: analyzer.addOption(i_opt, optionsDict[i_opt])
   analyzer.init()

   for [i_inpFile, i_inpTree] in inputFileTreePairs:

       i_maxEvents = -1 if (opts.maxEvents < 0) else (opts.maxEvents - analyzer.eventsProcessed())

       if opts.verbosity > -99:
          print(colored_text('[input]', ['1']), os.path.relpath(i_inpFile)+':'+i_inpTree)
          print('skipEvents =', skipEvents)
          print('maxEvents =', i_maxEvents)
          print('-'*50)

       analyzer.setInputTTree(i_inpFile, i_inpTree)
       analyzer.process(skipEvents, i_maxEvents)

   nEvtProcessed = analyzer.eventsProcessed()

   if opts.verbosity > -99:
      print('events processed: {:d}'.format(nEvtProcessed))

      time_finish = time.time()
      time_exe = time_finish - time_start
      timereport_str = 'execution time [sec]: {:.2f}'.format(time_exe)
      if time_exe > 0:
         timereport_str += ' ({:.5f} evts/sec)'.format(nEvtProcessed/time_exe)
      print(timereport_str)

      print('output:', os.path.relpath(opts.output))
      print('-'*50)
