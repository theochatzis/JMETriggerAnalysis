#!/usr/bin/env python3
"""Description:
 script to monitor batch jobs
  * finds all batch scripts, e.g. "XXX.htc" for HTCondor and "XXX.sh" for SGE, in the input directory (including sub-directories)
  * if a file called "XXX.completed" exists, the job is considered finished
  * otherwise, the job is resubmitted if option "-r" is specified
"""
import argparse
import os
import math
import glob
import ROOT

from common.utils import *

def monitor(options, log='', local=False):

    if options.check_root:
       ROOT.gROOT.SetBatch()

    # input directories
    INPUT_DIRS = []

    for i_opt in options.inputs:

        if not os.path.isdir(i_opt):
           WARNING(log_prx+'input argument is not a valid directory: '+i_opt)
           continue

        INPUT_DIRS += [i_opt]

    INPUT_DIRS = list(set(INPUT_DIRS))

    if len(INPUT_DIRS) == 0:
       return True

    # batch system
    BATCH_HTC = bool(options.batch == 'htc')

    BATCH_RESUB_EXE = 'condor_submit' if BATCH_HTC else 'qsub'

    if which(BATCH_RESUB_EXE, permissive=True) is None:
       return False

    ADD_OPTIONS = []
    if options.job_maxtime is not None:
       if BATCH_HTC: ADD_OPTIONS += ['-append "+RequestRuntime = '+str(options.job_maxtime)+'"']

    if options.jobflavour is not None:
       ADD_OPTIONS += ['-append \'+JobFlavour = "'+str(options.jobflavour)+'"\'']

    if len(ADD_OPTIONS) > 0:
       print (' > additional options to "'+BATCH_RESUB_EXE+'":', str(ADD_OPTIONS))

    EXT_INP = 'htc' if BATCH_HTC else 'sh'
    EXT_OUT = 'completed'

    if EXT_INP == EXT_OUT:
       KILL(log_prx+'logic error: extensions of input and output files are identical')

    counter_input = 0
    counter_resubmitted = 0
    counter_toResubmit = 0
    counter_running = 0
    counter_completed = 0

    FILES_INPUT = []

    _all_completed = True

    for input_dir in INPUT_DIRS:

        for path, subdirs, files in os.walk(input_dir):

            for name in files:

                if name.endswith(EXT_INP):

                   i_finp = os.path.join(path, name)

                   FILES_INPUT += [os.path.abspath(i_finp)]

                   if _all_completed:
                      i_fout = os.path.splitext(i_finp)[0]+'.'+EXT_OUT
                      if not os.path.isfile(i_fout): _all_completed = False

    counter_input = len(FILES_INPUT)

    if _all_completed:
       counter_completed = counter_input

    if not _all_completed or options.check_err or options.check_log or options.check_root:

       #
       # find script(s) running (or stuck) on batch system
       #
       # * current implementation:
       #   - if stuck, do not resubmit automatically
       #
       RUNNG_FILES = []

       if not _all_completed:

          if BATCH_HTC:

             if options.skip:
   
                running_jobIDs = HTCondor_jobIDs(os.environ['USER'])
   
                nJobs_submitted = len(running_jobIDs)
   
                for i_runn_jobID in running_jobIDs:
   
                    if i_runn_jobID in options.skip: continue
   
                    i_runn_exepath = HTCondor_executable_from_jobID(i_runn_jobID)
   
                    if i_runn_exepath != None:
   
                       i_runn_htcpath = os.path.splitext(i_runn_exepath)[0]+'.'+EXT_INP

                       if i_runn_htcpath in FILES_INPUT:
                          RUNNG_FILES += [os.path.abspath(i_runn_htcpath)]

             else:

                running_jobExes = HTCondor_jobExecutables_2(os.environ['USER'])

                for i_runn_exepath in running_jobExes:

                    i_runn_htcpath = os.path.splitext(i_runn_exepath)[0]+'.'+EXT_INP

                    if i_runn_htcpath in FILES_INPUT:
                       RUNNG_FILES += [os.path.abspath(i_runn_htcpath)]

          else:

             qstat_lines = get_output('qstat')[0].split('\n')
             qstat_lines = [_tmp for _tmp in qstat_lines if _tmp != '']

             if len(qstat_lines) > 2: qstat_lines = qstat_lines[2:]
   
             for qstat_l in qstat_lines:
   
                 qstat_jobN = qstat_l.split()[0]
   
                 if qstat_jobN in options.skip: continue
   
                 qstat_j = get_output('qstat -j '+qstat_jobN+' | grep script_file', permissive=True)[0].split('\n')
                 qstat_j = [_tmp for _tmp in qstat_j if _tmp != '']
    
                 if len(qstat_j) != 1: continue
   
                 qstat_j_pieces = qstat_j[0].split()
                 if len(qstat_j_pieces) != 2: continue
   
                 qstat_script = os.path.abspath(os.path.realpath(qstat_j_pieces[1]))

                 RUNNG_FILES += [qstat_script]

       FILES_RESUB = []

       counter_completed = 0
   
       for input_file in FILES_INPUT:

           input_file_woEXT = os.path.splitext(input_file)[0]

           output_file = input_file_woEXT+'.'+EXT_OUT

           if os.path.exists(output_file):

#              if options.verbose: print output_file

              # check stderr stream (if non-empty, resubmit)
              if options.check_err:

                 err_files_wildcard = None
                 if '/' in input_file_woEXT:
                    err_files_wildcard = input_file_woEXT[:input_file_woEXT.rfind('/')]+'/'+options.batch+input_file_woEXT[input_file_woEXT.rfind('/'):]
                 else:
                    err_files_wildcard = options.batch+'/'+input_file_woEXT

                 err_files_wildcard += '.err.*'

                 err_files = sorted(glob.glob(err_files_wildcard))

                 if (len(err_files) > 0) and (os.stat(err_files[-1]).st_size > 0):

                    EXE('rm -f '+output_file, verbose=options.verbose, dry_run=options.dry_run)

                    RESUB_FILES += [input_file]

                    continue

              # check condor-log (if contains the word "abort", resubmit)
              if options.check_log:

                 log_files_wildcard = None
                 if '/' in input_file_woEXT:
                    log_files_wildcard = input_file_woEXT[:input_file_woEXT.rfind('/')]+'/'+options.batch+input_file_woEXT[input_file_woEXT.rfind('/'):]
                 else:
                    log_files_wildcard = options.batch+'/'+input_file_woEXT

                 log_files_wildcard += '.log.*'

                 log_files = sorted(glob.glob(log_files_wildcard))

                 if (len(log_files) > 0) and (os.stat(log_files[-1]).st_size > 0):

                    if 'abort' in open(log_files[-1]).read():

                       EXE('rm -f '+output_file, verbose=options.verbose, dry_run=options.dry_run)

                       RESUB_FILES += [input_file]

                       continue

              if options.check_root:

                 output_file_root = input_file_woEXT+'.root'

                 if os.path.isfile(output_file_root):

                    output_tfile_root = ROOT.TFile.Open(output_file_root)

                    if (not output_tfile_root) or output_tfile_root.IsZombie() or output_tfile_root.TestBit(ROOT.TFile.kRecovered):

                       FILES_RESUB += [input_file]

                       output_tfile_root.Close()

                       continue

                    if options.verbose: print ('output ROOT file is valid:', os.path.relpath(output_file_root))

                    output_tfile_root.Close()

              counter_completed += 1

           elif input_file in RUNNG_FILES:
              counter_running += 1
              continue

           else:
              FILES_RESUB += [input_file]

       FILES_RESUB = sorted(list(set(FILES_RESUB)))

       nJobs_submitted = 0
       if len(FILES_RESUB) > 0:
          running_jobExes = HTCondor_jobExecutables_2(os.environ['USER'])
          nJobs_submitted = len(running_jobExes.keys())

       for resub_file in FILES_RESUB:

           if os.path.isfile(os.path.splitext(resub_file)[0]+'.'+EXT_OUT):
              counter_resubmitted -= 1
              counter_completed += 1
              continue

           resubmit_job = options.resubmit and (nJobs_submitted < options.jobs_max)

           if resubmit_job or local:

              try:
                 resub_file_abspath = os.path.abspath(os.path.realpath(resub_file))

                 if local:
                    resub_exe = os.path.splitext(resub_file_abspath)[0]+'.sh'
                    if os.path.isfile(resub_exe):
                       print (colored_text('> executing', ['93']), colored_text(os.path.relpath(resub_exe), ['1', '93']))
                       EXE(resub_exe, verbose=options.verbose, dry_run=options.dry_run)
                       counter_completed += 1
                 else:
                    print (colored_text('> resubmitting', ['93']), colored_text(os.path.relpath(resub_file), ['1', '93']))

                    resub_addopt = (' '+(' '.join(ADD_OPTIONS)) if (len(ADD_OPTIONS) > 0) else '')
                    EXE(BATCH_RESUB_EXE+' '+resub_file_abspath+resub_addopt, verbose=options.verbose, dry_run=options.dry_run)

                    counter_resubmitted += 1
                    nJobs_submitted += 1

              except:
                 counter_toResubmit += 1

           else:
              print (colored_text('> job to be resubmitted', ['93']), colored_text(os.path.relpath(resub_file), ['1', '93']))
              counter_toResubmit += 1

    counter_format = '{:>'+str(1+int(math.log10(counter_input)))+'}' if counter_input > 0 else '{:>1}'

    print ('')
    print ('-'*51)
    print ('')
    print (' Number of input  files found : '+colored_text(counter_format.format(counter_input), ['1']))
    print (' Number of output files found : '+colored_text(counter_format.format(counter_completed), ['1', '92']))
    print (' Number of resubmitted jobs   : '+colored_text(counter_format.format(counter_resubmitted), ['1', '93']))
    print (' Number of jobs to resubmit   : '+colored_text(counter_format.format(counter_toResubmit), ['1', '93']))
    print ('')
    print (' Number of jobs still running : '+counter_format.format(counter_running))
    print ('')
    print ('-'*51)
    print ('')

    return bool(counter_input == counter_completed)

#### main
if __name__ == '__main__':
   ### args
   parser = argparse.ArgumentParser(description=__doc__)

   parser.add_argument('-i', '--inputs', dest='inputs', nargs='+', default=[], required=True,
                       help='list of paths to input directories')

   parser.add_argument('--batch', dest='batch', choices=['htc', 'sge'], action='store', default='htc',
                       help='type of batch system for job submission (default: HTCondor)')

   parser.add_argument('--skip', dest='skip', nargs='+', default=[],
                       help='list of job-ID numbers to be ignored')

   parser.add_argument('-r', '--resubmit', dest='resubmit', action='store_true', default=False,
                       help='enable resubmission of batch jobs')

   parser.add_argument('--jobflavour', dest='jobflavour', action='store', type=str, default=None, required=False,
                       help='argument of HTCondor parameter "+JobFlavour"')

   parser.add_argument('-t', '--job-maxtime', dest='job_maxtime', action='store', default=None,
                       help='max-time assigned to batch job in seconds (only applies when running with --resubmit; only works for HTCondor)')

   parser.add_argument('-j', '--jobs-max', dest='jobs_max', action='store', type=int, default=5000,
                       help='maximum number of jobs that can submitted to the batch system')

   parser.add_argument('--repeat', dest='repeat', nargs='?', type=int, const=-1, default=None,
                       help='number of times the monitoring is repeated (enables continuous monitoring; see -f for monitoring frequency); if value is not specified or negative, monitoring stops only when all jobs are completed')

   parser.add_argument('-f', '--frequency', dest='frequency', action='store', type=int, default=3600,
                       help='interval of time in seconds between executions of the monitor (has no effect if --repeat is not specified)')

   parser.add_argument('--check-err', dest='check_err', action='store_true', default=False,
                       help='check job err file (resubmit if err file is not empty)')

   parser.add_argument('--check-log', dest='check_log', action='store_true', default=False,
                       help='check job log file (resubmit if log file contains word "abort")')

   parser.add_argument('--check-root', dest='check_root', action='store_true', default=False,
                       help='check integrity of ROOT output before marking job as completed')

   parser.add_argument('-l', '--local', dest='local', action='store_true', default=False,
                       help='execute jobs locally')

   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                       help='enable verbose mode')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')

   opts, opts_unknown = parser.parse_known_args()
   ### ----

   log_prx = os.path.basename(__file__)+' -- '

   if len(opts_unknown) > 0:
      KILL(log_prx+'unsupported command-line arguments: '+str(opts_unknown))

   if opts.repeat != 0:

      if opts.repeat is not None:

         n_reps = 0

         SLEEP_CMD = 'sleep '+str(opts.frequency)

      while not monitor(options=opts, log=log_prx, local=opts.local):

         if opts.repeat is None: break

         n_reps += 1

         if (opts.repeat >= 0) and (n_reps == opts.repeat): break

         EXE(SLEEP_CMD, verbose=opts.verbose, dry_run=opts.dry_run)
