#!/usr/bin/env python
"""
utilities related to the CMS Data Aggregation System (DAS)
"""
import json

from JMETriggerAnalysis.NTuplizers.utils.common import *

def load_dataset_data(das_name, max_files=-1, max_events=-1, parentFiles_levels=2, files_prefix='', verbose=False):

    if verbose:
       print(colored_text(das_name, ['1']))

    dataset_split = das_name.split('/')
    if len(dataset_split) != 4:
       KILL('load_dataset_data -- invalid data-set name (format is incorrect, check slashes): '+das_name)

    dset_data = {'DAS': str(das_name), 'files': []}

    dataset_files = command_output_lines('dasgoclient --query "file dataset='+str(das_name)+' | grep file.name,file.nevents"')
    dataset_files = [_tmp for _tmp in dataset_files if _tmp != '']
    dataset_files = sorted(list(set(dataset_files)))
    
   #  # removing files from list which do not have a T2 site (so only T0_CH_CERN_Tape i.e. not available to user)
   #  for iFile in range(len(dataset_files)):
   #      _fileName = dataset_files[iFile].split()[0]
   #      #print(_fileName)
   #      _dasSites = command_output_lines('dasgoclient --query "site file='+str(_fileName)+'"')
   #      #print(_dasSites)
   #      # loop over sites and check if there is a T2
   #      foundT2=False
   #      for _site in _dasSites:
   #         if 'T2' in _site:
   #           foundT2 = True
   #           break
   #      if not foundT2:
   #         del dataset_files[iFile]

    if len(dataset_files) == 0:
       KILL('load_dataset_data -- empty list of input files for dataset: '+str(das_name))

    if max_files > 0:
       dataset_files = dataset_files[:max_files]

    dataset_filesNevents = []
    for _tmp in dataset_files:
        _tmp_split = _tmp.split()
        if len(_tmp_split) != 2:
           KILL(das_name+' '+str(_tmp))
        if not is_int(_tmp_split[1]):
           KILL(das_name+' '+i_file+' '+str(_tmp_split[1]))
        dataset_filesNevents += [[_tmp_split[0], int(_tmp_split[1])]]

    totEvents, breakLoop = 0, False
    for i_file_idx, [i_file, i_file_nevents] in enumerate(dataset_filesNevents):
        totEvents += i_file_nevents
        if (max_events > 0) and (totEvents >= max_events):
           breakLoop = True

        if verbose:
           print('  [ file', i_file_idx+1, '/', len(dataset_filesNevents), '] [ # events =', i_file_nevents, ']', i_file)

        i_file_parents1 = []
        i_file_parents2 = []
        if parentFiles_levels > 0:
           i_file_parents1 = command_output_lines('dasgoclient --query "parent file='+str(i_file)+'"')
           i_file_parents1 = [files_prefix+_tmp for _tmp in i_file_parents1 if _tmp]
           i_file_parents1 = sorted(list(set(i_file_parents1)))
           if parentFiles_levels > 1:
              i_file_parents2 = []
              for i_file_aodf in i_file_parents1:
                  i_file_parents2_tmp = command_output_lines('dasgoclient --query "parent file='+str(i_file_aodf)+'"')
                  i_file_parents2_tmp = [_tmp.replace(' ', '') for _tmp in i_file_parents2_tmp]
                  i_file_parents2_tmp = [files_prefix+_tmp for _tmp in i_file_parents2_tmp if _tmp]
                  i_file_parents2_tmp = sorted(list(set(i_file_parents2_tmp)))
                  i_file_parents2 += i_file_parents2_tmp
              i_file_parents2 = sorted(list(set(i_file_parents2)))
        
        
        if verbose:
           for _tmp in i_file_parents2:
               print(' '*5, _tmp)

        dset_data['files'] += [{
          'file': files_prefix+i_file,
          'nevents': i_file_nevents,
          'parentFiles_1': i_file_parents1,
          'parentFiles_2': i_file_parents2,
        }]

        if breakLoop:
           break

    del totEvents, breakLoop

    # consistency checks on dataset data
    assert_dataset_data(dset_data=dset_data, verbose=verbose)

    return dset_data

def assert_dataset_data(dset_data, verbose=False):

    if not isinstance(dset_data, dict):
       KILL('assert_dataset_data -- invalid content of dataset .json file [-d]: '+str(file_path))

    if 'DAS' not in dset_data:
       KILL('assert_dataset_data -- 11')
    elif not isinstance(dset_data['DAS'], str):
       KILL('assert_dataset_data -- 12')

    if 'files' not in dset_data:
       KILL('assert_dataset_data -- 21')
    elif not isinstance(dset_data['files'], list):
       KILL('assert_dataset_data -- 22')

    for i_ent in dset_data['files']:

        if not isinstance(i_ent, dict):
           KILL('assert_dataset_data -- 31')

        if 'file' not in i_ent:
           KILL('assert_dataset_data -- 41 '+str(i_ent))
        elif not isinstance(i_ent['file'], str):
           KILL('assert_dataset_data -- 42 '+str(i_ent))

        if 'nevents' not in i_ent:
           KILL('assert_dataset_data -- 41 '+str(i_ent))
        elif not isinstance(i_ent['nevents'], int):
           KILL('assert_dataset_data -- 42 '+str(i_ent))
        elif i_ent['nevents'] < 0:
           KILL('assert_dataset_data -- 43 '+str(i_ent))

        for _tmp in ['parentFiles_1', 'parentFiles_2']:
            if _tmp not in i_ent:
               KILL('assert_dataset_data -- 51 '+str(i_ent))
            elif not isinstance(i_ent[_tmp], list):
               KILL('assert_dataset_data -- 52 '+str(i_ent))
            else:
               for _tmp2 in i_ent[_tmp]:
                   if not isinstance(_tmp2, str):
                      KILL('assert_dataset_data -- 53 '+str(i_ent))

def skim_das_jsondump(file_path, max_files=-1, max_events=-1, verbose=False):

    dset_data = json.load(open(file_path))

    # consistency checks on dataset data
    assert_dataset_data(dset_data, verbose=verbose)

    # skim input list based on max_files and max_events
    if max_files > 0:
       dset_data['files'] = dset_data['files'][:max_files]

    if max_events > 0:
       lastIndex, totEvents = 0, 0
       for _tmp in dset_data['files']:
           lastIndex += 1
           totEvents += _tmp['nevents']
           if totEvents >= max_events:
              break
       if lastIndex != len(dset_data['files']):
          dset_data['files'] = dset_data['files'][:lastIndex]
       del lastIndex, totEvents

    return dset_data
