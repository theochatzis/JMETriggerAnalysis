#!/usr/bin/env python3
"""
 driver to set up batch jobs
"""
import argparse
import os
import math
import glob
import ROOT

from common.utils import *

if __name__ == '__main__':
   ### args -----------
   parser = argparse.ArgumentParser(description=__doc__)

   parser.add_argument('-s', '--script', dest='script', action='store', default=os.path.dirname(__file__)+'/run.py',
                       help='path to python script executed in each batch job')

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=[],
                       help='path to file(s) containing input TTree(s)')

   parser.add_argument('-t', '--tree-name', dest='tree_name', action='store', default='JMETriggerNTuple/Events',
                       help='TTree key in input file(s)')

   parser.add_argument('-p', '--plugin', dest='plugin', action='store', default='JMETriggerAnalysisDriverPhase2', #default=None, required=True,
                       help='name of analysis plugin')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default=None,
                       help='path to output directory')
   
   parser.add_argument('-od', '--outputdir', dest='outputdir', required=True, action='store', default=None,
                       help='path to output directory in eos')

   parser.add_argument('-n', '--nperjob', dest='nperjob', type=int, action='store', default=5000, #default=None, required=True,
                       help='number of events per job')

   parser.add_argument('--time', '--RequestRuntime', dest='RequestRuntime', action='store', default='10800',
                       help='HTCondor: value of parameter "MaxRuntime"')

   parser.add_argument('--JobFlavour', dest='JobFlavour', action='store', default=None,
                       help='argument of HTCondor parameter "+JobFlavour" (by default, the parameter is not specified)')

   parser.add_argument('--AccountingGroup', dest='AccountingGroup', action='store', default=None,
                       help='argument of HTCondor parameter "+AccountingGroup" (by default, the parameter is not specified)')

   parser.add_argument('--batch', dest='batch', action='store', choices=['htc', 'sge'], default='htc',
                       help='type of batch system for job submission [default: HTCondor]')

   parser.add_argument('--submit', dest='submit', action='store_true', default=False,
                       help='submit job(s) to the batch system')

   parser.add_argument('-l', '--level', dest='level', action='store', type=int, default=0,
                       help='level of directory depth in output directory')

   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                       help='enable verbose mode')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')

   opts, opts_unknown = parser.parse_known_args()
   ### ----------------

   ROOT.gROOT.SetBatch()

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation
   if opts.level < 0:
      KILL(log_prx+'negative level of directory depth in output directory (must be >=0) [-l]: '+str(opts.level))

   PYSCRIPT_PATH = opts.script

   if not os.path.isfile(PYSCRIPT_PATH):
      KILL(log_prx+'target executable not found: '+PYSCRIPT_PATH)

   PYSCRIPT_ABSPATH = os.path.abspath(os.path.realpath(PYSCRIPT_PATH))

   INPUT_FILES = []
   for i_inpf in opts.inputs:
     i_inpf_ls = glob.glob(i_inpf)
     for i_inpf_2 in i_inpf_ls:
       if os.path.isfile(i_inpf_2):
         INPUT_FILES += [os.path.abspath(i_inpf_2)]
   INPUT_FILES = sorted(list(set(INPUT_FILES)))

   if len(INPUT_FILES) == 0:
      KILL(log_prx+'empty list of input files [-i]')

   if os.path.isdir(opts.output):
      WARNING(log_prx+'output directory already exists, new files will be added to it [-o]: '+opts.output)
   elif os.path.exists(opts.output):
      KILL(log_prx+'target path to output directory already exists and it is not a directory [-o]: '+opts.output)

   OUT_DIR = os.path.abspath(opts.output)
   OUTPUT_DIR = os.path.abspath(opts.outputdir)

   BATCH_HTC = bool(opts.batch == 'htc')

   if (not opts.dry_run) and opts.submit:
      which('condor_submit' if BATCH_HTC else 'qsub')

   which('python')

   if 'SCRAM_ARCH' not in os.environ:
      KILL(log_prx+'environment variable "SCRAM_ARCH" not defined (please set up CMSSW area)')

   is_slc7_arch = False
   if os.environ['SCRAM_ARCH'].startswith('slc7'): is_slc7_arch = True
   elif os.environ['SCRAM_ARCH'].startswith('slc6'): pass
   else:
      KILL(log_prx+'could not infer architecture from environment variable "SCRAM_ARCH" (script needs to be updated): '+str(os.environ['SCRAM_ARCH']))
   ### ----------------

   ### output ---------
   for i_inpf in INPUT_FILES:

       if not os.path.isfile(i_inpf):
          WARNING(log_prx+'invalid target path to input file [-i]: '+i_inpf)
          continue

       i_inptfile = ROOT.TFile.Open(i_inpf)
       if not i_inptfile or i_inptfile.IsZombie():
          WARNING(log_prx+'failed to access TFile (will be skipped): path='+i_inpf)
          continue

       i_tree = i_inptfile.Get(opts.tree_name)
       if not i_tree:
          WARNING(log_prx+'TFile does not contain TObject with key "'+opts.tree_name+'": path='+i_inpf)
          continue

       i_evtN = i_tree.GetEntries()

       i_inptfile.Close()

       if i_evtN == 0:
          minmax_evts = [ [0,0] ]
       else:
          minmax_evts = [ [int(_tmp * opts.nperjob), min(int(i_evtN-1), int(((_tmp+1) * opts.nperjob)-1))] for _tmp in range(int(math.ceil(float(i_evtN)/opts.nperjob)))]

       input_subdirs = []
       input_dirname = os.path.dirname(i_inpf)
       while opts.level > len(input_subdirs):
          input_subdirs.insert(0, os.path.basename(input_dirname))
          input_dirname = os.path.dirname(input_dirname)
       del input_dirname

       OUTDIR_PATH = OUT_DIR+'/'+('/'.join(input_subdirs)) if len(input_subdirs) else OUT_DIR
       OUTPUTDIR_PATH = OUTPUT_DIR

       for j_minmax_evt in range(len(minmax_evts)):

           OUTEXE_NAME = os.path.splitext(os.path.basename(i_inpf))[0]+'__'+str(j_minmax_evt)

           OUTEXE_PATH     = OUTDIR_PATH+'/'+OUTEXE_NAME+'.sh'
           OUTPUT_PATH_TMP = OUTPUTDIR_PATH+'/'+OUTEXE_NAME+'.root.tmp'
           OUTPUT_PATH     = OUTPUTDIR_PATH+'/'+OUTEXE_NAME+'.root'

           OUTEXE_ABSPATH     = os.path.abspath(os.path.realpath(OUTEXE_PATH))
           OUTPUT_ABSPATH_TMP = os.path.abspath(os.path.realpath(OUTPUT_PATH_TMP))
           OUTPUT_ABSPATH     = os.path.abspath(os.path.realpath(OUTPUT_PATH))

           if os.path.exists(OUTEXE_ABSPATH):
              KILL(log_prx+'path to target output script already exists: '+OUTEXE_ABSPATH)

           if os.path.exists(OUTPUT_ABSPATH_TMP):
              KILL(log_prx+'path to target (temporary) output file already exists: '+OUTPUT_ABSPATH_TMP)

           if os.path.exists(OUTPUT_ABSPATH):
              KILL(log_prx+'path to target output file already exists: '+OUTPUT_ABSPATH)

           if len(minmax_evts[j_minmax_evt]) != 2:
              KILL(log_prx+'list of [first-event, last-event] pairs: element has size different from 2: '+minmax_evts[j_minmax_evt])

           EVT_FIRST = minmax_evts[j_minmax_evt][0]
           EVT_LAST  = minmax_evts[j_minmax_evt][1]

           if EVT_FIRST > EVT_LAST:
              KILL(log_prx+'list of [first-event, last-event] pairs: last-event ('+str(EVT_LAST)+') is smaller than first-event ('+str(EVT_FIRST)+')')

           CMDS_0 = [
             'if [ -f '+OUTPUT_ABSPATH+' ]; then',
              ' rm -f '+OUTPUT_ABSPATH+'; fi;',
           ]

           CMDS_1 = [
             PYSCRIPT_ABSPATH,
             '-i '+i_inpf,
             '-o '+OUTPUT_ABSPATH,
             '-p '+opts.plugin,
             '--skipEvents '+str(EVT_FIRST),
             '--maxEvents '+str(1+EVT_LAST-EVT_FIRST),
           ]
           if opts_unknown:
              CMDS_1 += [' '.join(opts_unknown)]

           CMDS_2 = [
             'touch '+OUTDIR_PATH+'/'+OUTEXE_NAME+'.completed',
           ]

           EXECS = [
             ['set -e'],
             CMDS_0,
             CMDS_1,
             CMDS_2,
           ]
           # ----------------

           ### submission script
           BATCH_DIR = opts.batch

           if not os.path.isdir(OUTDIR_PATH+'/'+BATCH_DIR):
              EXE('mkdir -p '+OUTDIR_PATH+'/'+BATCH_DIR, verbose=opts.verbose, dry_run=opts.dry_run)

           # HTCondor ----------
           if BATCH_HTC:

              OPTS = [
                'batch_name = '+OUTEXE_NAME,

                'executable = '+OUTEXE_ABSPATH,

                'output = '+OUTDIR_PATH+'/'+BATCH_DIR+'/'+OUTEXE_NAME+'.out.$(Cluster).$(Process)',
                'error  = '+OUTDIR_PATH+'/'+BATCH_DIR+'/'+OUTEXE_NAME+'.err.$(Cluster).$(Process)',
                'log    = '+OUTDIR_PATH+'/'+BATCH_DIR+'/'+OUTEXE_NAME+'.log.$(Cluster).$(Process)',

                '#arguments = ',

                'transfer_executable = True',

                'universe = vanilla',

                'getenv = True',

                'should_transfer_files   = IF_NEEDED',
                'when_to_transfer_output = ON_EXIT',

                'requirements = (OpSysAndVer =?= "'+('CentOS7' if is_slc7_arch else 'SL6')+'")',

                ' RequestMemory  =  2000',
                '+MaxRuntime = '+str(opts.RequestRuntime),
              ]

              if opts.JobFlavour is not None:
                 JobFlavour = opts.JobFlavour
                 while JobFlavour.startswith("'") or JobFlavour.startswith('"'):
                   JobFlavour = JobFlavour[1:]
                 while JobFlavour.endswith("'") or JobFlavour.endswith('"'):
                   JobFlavour = JobFlavour[:-1]
                 OPTS += [
                   '+JobFlavour = "{:}"'.format(JobFlavour)
                 ]

              if opts.AccountingGroup is not None:
                 AccountingGroup = opts.AccountingGroup
                 while AccountingGroup.startswith("'") or AccountingGroup.startswith('"'):
                   AccountingGroup = AccountingGroup[1:]
                 while AccountingGroup.endswith("'") or AccountingGroup.endswith('"'):
                   AccountingGroup = AccountingGroup[:-1]
                 OPTS += [
                   '+AccountingGroup = "{:}"'.format(AccountingGroup)
                 ]

              OPTS += ['queue']

              if not opts.dry_run:
                 o_file = open(OUTEXE_ABSPATH, 'w')

                 o_shebang = '#!/bin/bash'
                 o_file.write(o_shebang+'\n')

#                 # HTCondor getenv=True does not export LD_LIBRARY_PATH
#                 # --> added by hand to the script itself
#                 if 'LD_LIBRARY_PATH' in os.environ:
#                    o_file.write('\n'+'export LD_LIBRARY_PATH='+os.environ['LD_LIBRARY_PATH']+'\n')

                 o_file.write('\n'+'cd '+os.environ['CMSSW_BASE']+'/src')
                 o_file.write('\n'+'eval `scramv1 runtime -sh`')
                 o_file.write('\n'+'cd - &> /dev/null'+'\n')

                 EXE_LINE = '\n\n'.join([' \\\n '.join(_cmds) for _cmds in EXECS])
                 o_file.write('\n'+EXE_LINE+'\n')

                 o_file.close()

              print('\033[1m'+'\033[94m'+'output:'+'\033[0m', os.path.relpath(OUTEXE_PATH))

              EXE('chmod u+x '+OUTEXE_ABSPATH, verbose=opts.verbose, dry_run=opts.dry_run)

              OFCFG_ABSPATH = os.path.splitext(OUTEXE_ABSPATH)[0]+'.htc'

              if not opts.dry_run:
                 o_fcfg = open(OFCFG_ABSPATH, 'w')
                 for _opt in OPTS: o_fcfg.write(_opt+'\n')
                 o_fcfg.close()

              if opts.submit:
                 EXE('condor_submit '+OFCFG_ABSPATH, verbose=opts.verbose, dry_run=opts.dry_run)
           # -------------------

           # SGE ---------------
           else:

              # batch configuration options
              OPTS = [
                '-N '+OUTEXE_NAME,
                '-o '+OUTDIR_PATH+'/'+BATCH_DIR,
                '-e '+OUTDIR_PATH+'/'+BATCH_DIR,
              ]

              OPTS = ['#$ '+_opt for _opt in OPTS]

              if not opts.dry_run:
                 o_file = open(OUTEXE_ABSPATH, 'w')

                 o_shebang = '#!/bin/bash'
                 o_file.write(o_shebang+'\n')

                 EXE_LINE = '\n\n'.join([' \\\n '.join(_cmds) for _cmds in EXECS])
                 o_file.write('\n'+EXE_LINE+'\n')

                 o_file.close()

              EXE('chmod u+x '+OUTEXE_ABSPATH, verbose=opts.verbose, dry_run=opts.dry_run)

              print('\033[1m'+'\033[94m'+'output:'+'\033[0m', os.path.relpath(OUTEXE_PATH))

              if opts.submit:
                 EXE('qsub '+OUTEXE_ABSPATH, verbose=opts.verbose, dry_run=opts.dry_run)
           # -------------------

   ### ----------------
