#!/usr/bin/env python3
import os
import subprocess

def colored_text(txt, keys=[]):
    _tmp_out = ''
    for _i_tmp in keys:
        _tmp_out += '\033['+_i_tmp+'m'
    _tmp_out += txt
    if len(keys) > 0: _tmp_out += '\033[0m'

    return _tmp_out

def KILL(log):
    raise RuntimeError('\n '+colored_text('@@@ FATAL', ['1','91'])+' -- '+log+'\n')

def WARNING(log):
    print('\n '+colored_text('@@@ WARNING', ['1','93'])+' -- '+log+'\n')

def MKDIRP(dirpath, verbose=False, dry_run=False):
    if verbose: print('\033[1m'+'>'+'\033[0m'+' os.mkdirs("'+dirpath+'")')
    if dry_run: return
    try:
      os.makedirs(dirpath)
    except OSError:
      if not os.path.isdir(dirpath):
        raise
    return

def EXE(cmd, suspend=True, verbose=False, dry_run=False):
    if verbose: print('\033[1m'+'>'+'\033[0m'+' '+cmd)
    if dry_run: return

    _exitcode = os.system(cmd)
    _exitcode = min(255, _exitcode)

    if _exitcode and suspend:
       raise RuntimeError(_exitcode)

    return _exitcode

def get_output(cmd, permissive=False):
    prc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = prc.communicate()

    if (not permissive) and prc.returncode:
       KILL('get_output -- shell command failed (execute command to reproduce the error):\n'+' '*14+'> '+cmd)

    return (out, err)

def command_output_lines(cmd, stdout=True, stderr=False, permissive=False):
    _tmp_out_ls = []

    if not (stdout or stderr):
       WARNING('command_output_lines -- options "stdout" and "stderr" both set to FALSE, returning empty list')
       return _tmp_out_ls

    _tmp_out = get_output(cmd, permissive=permissive)
    
    #print(type(_tmp_out[0]))
    if stdout: _tmp_out_ls += _tmp_out[0].decode("utf-8").split('\n')
    if stderr: _tmp_out_ls += _tmp_out[1].decode("utf-8").split('\n')
    
    return _tmp_out_ls

def rreplace(str__, old__, new__, occurrence__):
    li_ = str__.rsplit(old__, occurrence__)
    return new__.join(li_)

def which(program, permissive=False, verbose=False):
    fpath, fname = os.path.split(program)

    _exe_ls = []

    if fpath:
       if os.path.isfile(program) and os.access(program, os.X_OK):
          _exe_ls += [program]

    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)

            if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
               _exe_ls += [exe_file]

    _exe_ls = list(set(_exe_ls))

    if len(_exe_ls) == 0:
       log_msg = 'which -- executable not found: '+program

       if permissive:
          if verbose: WARNING(log_msg)
          return None

       else:
          KILL(log_msg)

    if len(_exe_ls) >  1:
       if verbose:
          WARNING('which -- executable "'+program+'" has multiple matches: \n'+str(_exe_ls))

    return _exe_ls[0]

def is_int(value):
    try: int(value)
    except ValueError: return False

    return True

def is_float(value):
    try: float(value)
    except ValueError: return False

    return True

def HTCondor_jobIDs(username=None):
    if not username:
       if 'USER' in os.environ: username = os.environ['USER']

    if not username:
       KILL('HTCondor_jobIDs -- unspecified argument "username"')

    _condorq_jobIDs = []

    _condorq_lines = get_output('condor_q')[0].split('\n')

    for _i_condorq in _condorq_lines:
        _i_condorq_pieces = _i_condorq.split()

        if (len(_i_condorq_pieces) > 0) and (_i_condorq_pieces[0] == str(username)):
           _condorq_jobIDs += [_i_condorq_pieces[-1]]

    return _condorq_jobIDs

def HTCondor_jobExecutables_old(username=None):
    if not username:
       if 'USER' in os.environ: username = os.environ['USER']

    if not username:
       KILL('HTCondor_jobExecutables -- unspecified argument "username"')

    _condorq_jobExes = []

    _condorq_lines = get_output('condor_q -long '+username)[0].split('\n')

    for _i_condorq in _condorq_lines:

        if not _i_condorq.startswith('Cmd = '): continue

        _i_condorq_cmd_pieces = _i_condorq.split(' = ')

        if len(_i_condorq_cmd_pieces) != 2: continue

        _exe_path = _i_condorq_cmd_pieces[1]
        _exe_path = _exe_path.replace(' ', '')

        if len(_exe_path) == 0: continue

        if _exe_path.startswith('"'): _exe_path = _exe_path[+1:]
        if _exe_path.endswith  ('"'): _exe_path = _exe_path[:-1]

        _exe_path = os.path.abspath(os.path.realpath(_exe_path))

        _condorq_jobExes += [_exe_path]

    _condorq_jobExes = sorted(list(set(_condorq_jobExes)))

    return _condorq_jobExes

def HTCondor_jobExecutables(username=None):
    if not username:
       if 'USER' in os.environ: username = os.environ['USER']

    if not username:
       KILL('HTCondor_jobExecutables -- unspecified argument "username"')

    _condorq_jobExes_dict = {}

    _condorq_cmd = 'condor_q {:} -format "%d." ClusterId -format "%d " ProcId -format "%s\\n" Cmd'.format(username)
    
    _condorq_lines = get_output(_condorq_cmd, permissive=True)[0].decode("utf-8").split('\n')

    for _i_condorq_line in _condorq_lines:

        _i_condorq_cmd_pieces = _i_condorq_line.split()

        if len(_i_condorq_cmd_pieces) != 2: continue

        _exe_path = os.path.abspath(_i_condorq_cmd_pieces[1])

        _condorq_jobExes_dict[_exe_path] = _i_condorq_cmd_pieces[0]

    return _condorq_jobExes_dict

def HTCondor_executable_from_jobID(jobID):
    _condorq_cmd = get_output('condor_q '+jobID+' -long')[0].split('\n')
    _condorq_cmd = [_tmp for _tmp in _condorq_cmd if _tmp.startswith('Cmd = ')]

    if len(_condorq_cmd) != 1: return None

    _condorq_cmd_pieces = _condorq_cmd[0].split(' = ')
    if len(_condorq_cmd_pieces) != 2: return None

    _exe_path = _condorq_cmd_pieces[1]
    _exe_path = _exe_path.replace(' ', '')

    if _exe_path.startswith('"'): _exe_path = _exe_path[+1:]
    if _exe_path.endswith  ('"'): _exe_path = _exe_path[:-1]

    _exe_path = os.path.abspath(os.path.realpath(_exe_path))

    return _exe_path

def slurm_jobExecutables(username=None, executable=None):
    if not username:
      if 'USER' in os.environ:
        username = os.environ['USER']

    if not username:
      KILL('slurm_jobExecutables -- unspecified argument "username"')

    _squeue_jobExes_dict = {}
    _squeue_cmd = 'squeue -u {:} --format "%i %o"'.format(username)
    _squeue_lines = get_output(_squeue_cmd, permissive=True)[0].split('\n')

    _startJobParsing = False
    for _i_squeue_line in _squeue_lines:
      if not _i_squeue_line: continue
      if _i_squeue_line == 'JOBID COMMAND':
        _startJobParsing = True
        continue
      if not _startJobParsing: continue

      _i_squeue_cmd_pieces = _i_squeue_line.split()
      if executable is not None and _i_squeue_cmd_pieces[1] != executable: continue

      _jobids = []
      if _i_squeue_cmd_pieces[0].endswith(']'):
        _jobid_blks = _i_squeue_cmd_pieces[0].split('[')
        _jobid = _jobid_blks[0]
        _taskids_str = _jobid_blks[1][:-1]
        _taskids_strblks = _taskids_str.split(',')
        for _taskids_strblk in _taskids_strblks:
          _taskidsInBlk = []
          if '-' in _taskids_strblk:
            _taskidsInBlkMinMax = _taskids_strblk.split('-')
            _taskidsInBlk += range(int(_taskidsInBlkMinMax[0]), int(_taskidsInBlkMinMax[1])+1)
          else:
            _taskidsInBlk.append(int(_taskids_strblk))
          _jobids += [_jobid+str(_taskid) for _taskid in _taskidsInBlk]
      else:
        _jobids.append(_i_squeue_cmd_pieces[0])

      for _jobid in _jobids:
        _squeue_jobExes_dict[_jobid] = ' '.join(_i_squeue_cmd_pieces[1:])

    return _squeue_jobExes_dict

def hadd_rootfiles(output, inputs):
    if os.path.exists(output):
       KILL('hadd_rootfiles -- path to target output file already exists: '+output)

    if len(inputs) == 0:
       KILL('hadd_rootfiles -- empty list of inputs')

    valid_inputs = []
    for i_inp in inputs:

        valid_inputs += [i_inp]

    _merger = ROOT.TFileMerger(False, False)
    _merger.OutputFile(output_file)

    for i_inp in inputs:

        if not os.path.isfile(i_inp):
           KILL('hadd_rootfiles -- invalid path to input file: '+i_inp)

        _tmp_tfile = ROOT.TFile.Open(i_inp)

        if not _tmp_tfile:
           KILL('hadd_rootfiles -- failed conversion from input file path to TFile: '+i_inp)

        elif _tmp_tfile.IsZombie():
           KILL('hadd_rootfiles -- input TFile in Zombie state: '+i_inp)

        _tmp_tfile.Close()

        _merger.AddFile(i_inp)

    _ret = _merger.Merge(False)

    if not _ret:
       KILL('hadd_rootfiles -- call to TFileMerger::Merge() failed: output='+output)

    print(colored_text('[output='+output_file+']', ['93']), 'merging completed {0}, {1:.2f} MB'.format(output_file, os.path.getsize(output_file)/1024.0/1024.0))
