#!/usr/bin/env python
"""merge outputs of batch jobs"""
import os
import argparse
import glob
import array
import re
import ROOT

from common.utils import *

def all_file_paths(input_directory):
  _all_fpaths = []
  _paths = glob.glob(input_directory+'/*')

  for _tmp in _paths:
    if os.path.isfile(_tmp):
      _all_fpaths += [_tmp]
    elif os.path.isdir(_tmp):
      _all_fpaths += all_file_paths(_tmp)

  return _all_fpaths

def merge_rootfiles(input_directories, output_file, input_skipKeywords=[], compressionLevel=None, verbosity=0, dry_run=False):
    if os.path.exists(output_file):
       KILL('merge_rootfiles -- target path to output file already exists: '+output_file)

    _valid_files = []

    _compressionLevel = compressionLevel

    for i_dir in input_directories:

       _input_files = all_file_paths(i_dir)
       _input_files = [os.path.abspath(os.path.realpath(_tmp)) for _tmp in _input_files]

       _good_files = []
       for _tmp in _input_files:
         if not _tmp.endswith('.root'):
           continue
         _skipFile = False
         for _tmp2 in input_skipKeywords:
           if _tmp2 in _tmp:
             _skipFile = True
             break
         if not _skipFile:
           _good_files.append(_tmp)
         else:
           if verbosity > 10:
             print 'merge_rootfiles --', colored_text('[input will be skipped]', ['1','94']), os.path.relpath(_tmp)

       for fi in _good_files:
         _tf = ROOT.TFile.Open(fi)
         if (not _tf) or _tf.IsZombie() or _tf.TestBit(ROOT.TFile.kRecovered):
           continue

         if _compressionLevel is None:
           _compressionLevel = _tf.GetCompressionLevel()

         _valid_files += [fi]

         _tf.Close()
#         ROOT.gROOT.GetListOfFiles().Remove(_tf)

    print colored_text('[output = '+output_file+']', ['1']), 'merging {0} files'.format(len(_valid_files))

    _ret = 0

    if not dry_run:

       if len(_valid_files) == 0:
         print colored_text('[output = '+output_file+']', ['1', '93']), 'no valid input files found, output will not be created'

       elif len(_valid_files) == 1:
         if verbosity > 10: print '  '+colored_text('[input]', ['1']), _valid_files[0]

         EXE('cp '+_valid_files[0]+' '+output_file, verbose=(verbosity > 0), dry_run=dry_run)

         print colored_text('[output = '+output_file+']', ['1', '92']), 'merging completed ({:.2f} MB)'.format(os.path.getsize(output_file)/1024.0/1024.0)

       else:
         if _compressionLevel is None:
           KILL('merge_rootfiles -- logic error: could not determine CompressionLevel parameter from input files')

         _merger = ROOT.TFileMerger(False, True)
         _merger.OutputFile(output_file, False, _compressionLevel)

         for _tmp in _valid_files:
           if verbosity > 10: print '  '+colored_text('[input]', ['1']), os.path.relpath(_tmp)
           _merger.AddFile(_tmp)

         if _merger.HasCompressionChange():
           print colored_text('[output = '+output_file+']', ['1']), 'compression-level of output file differs from that of input files, merging will be slower'

         _ret = _merger.Merge()
         if not _ret:
           KILL('merge_rootfiles -- runtime error: call to TFileMerger::Merge() failed [output = '+output_file+']')

#         _merger.Reset()
#         del _merger

         print colored_text('[output = '+output_file+']', ['1', '92']), 'merging completed ({:.2f} MB)'.format(os.path.getsize(output_file)/1024.0/1024.0)

    else:
      if verbosity > 10:
        for _tmp in _valid_files:
          print '  '+colored_text('[input]', ['1']), os.path.relpath(_tmp)

      print colored_text('[output = '+output_file+']', ['1', '92'])

    return _ret

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser(description=__doc__)

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=[],
                       help='paths to output directories of crab3-task (Tier-2)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default='',
                       help='path to output directory')

   parser.add_argument('-s', '--skip', dest='skip', nargs='+', default=['/failed/'], # crab3
                       help='keywords to skip input files (if any of the specified strings is contained in the abs-path of an input file, the latter will be skipped)')

   parser.add_argument('-p', '--postfix', dest='postfix', action='store', default='',
                       help='postfix for name of ROOT output file(s)')

   parser.add_argument('-l', '--level', dest='level', action='store', type=int, default=0,
                       help='level of directory depth in output directory')

   parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                       help='verbosity level')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   log_prx = os.path.basename(__file__)+' -- '

   ROOT.gROOT.SetBatch()

   ROOT.gErrorIgnoreLevel = ROOT.kWarning

   ### args validation ---
#  if os.path.exists(opts.output):
#     KILL(log_prx+'target path to output directory already exists [-o]: '+opts.output)

   if opts.level < 0:
      KILL(log_prx+'negative level of directory depth in output directory (must be >=0) [-l]: '+str(opts.level))

   # keywords to skip input files
   input_skipkeywords = list(set(opts.skip))

   # inputs
   INPUT_DIRS = []
   for i_inp in opts.inputs:
       i_inp_ls = glob.glob(i_inp)
       for i_inp_2 in i_inp_ls:
           if os.path.isdir(i_inp_2):
              INPUT_DIRS += [os.path.abspath(os.path.realpath(i_inp_2))]
           elif opts.verbosity > 0:
              WARNING(log_prx+'target input path is not a directory (will be skipped): '+i_inp_2)

   INPUT_DIRS = sorted(list(set(INPUT_DIRS)))

   if len(INPUT_DIRS) == 0:
     KILL(log_prx+'empty list of input directories')

   # outputs
   sample_inputs_dict = {}

   for i_task in INPUT_DIRS:
       task_abspath = os.path.abspath(os.path.realpath(i_task))
       if not os.path.isdir(task_abspath):
          if opts.verbosity > 0:
             WARNING(log_prx+'skipping task "'+i_task+'", directory not found: '+task_abspath)
          continue

       task_samplename_pieces = [os.path.basename(task_abspath)]
       task_dirname = os.path.dirname(task_abspath)
       while opts.level >= len(task_samplename_pieces):
          task_samplename_pieces.insert(0, os.path.basename(task_dirname))
          task_dirname = os.path.dirname(task_dirname)
       del task_dirname

       task_samplename = '/'.join(task_samplename_pieces)
       if task_samplename in sample_inputs_dict:
         KILL(log_prx+'output with label "'+task_samplename+'" already exists (please adjust inputs):\n\n'+str(sample_inputs_dict))

       sample_inputs_dict[task_samplename] = [task_abspath]

   for i_sample in sorted(sample_inputs_dict.keys()):
       i_output = opts.output+'/'+i_sample+opts.postfix+'.root'

       i_output_dir = os.path.dirname(opts.output+'/'+i_sample)
       EXE('mkdir -p '+i_output_dir, verbose=(opts.verbosity > 0), dry_run=opts.dry_run)

       if os.path.exists(i_output):
         WARNING(log_prx+'target path to output file already exists (will be skipped): '+os.path.relpath(i_output))
         continue

       merge_rootfiles(
         input_directories = sample_inputs_dict[i_sample],
         output_file = i_output,
         input_skipKeywords = input_skipkeywords,
         compressionLevel = None,
         verbosity = opts.verbosity,
         dry_run = opts.dry_run,
       )
