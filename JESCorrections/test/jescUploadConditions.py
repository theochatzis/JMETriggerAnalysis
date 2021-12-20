#!/usr/bin/env python
"""
Script which reads in a .db file and uploads all the tags to the production, or development (prep), database

Original implementation by Sam Harper, see
https://github.com/cms-egamma/EgammaDBTools/blob/b61bd13f1f393e539961aa797e71bbb667f2d435/test/egRegUpload.py
"""
import os
import argparse
import subprocess
import json
import shutil
import time

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('dbfile')
  parser.add_argument('-r', '--record-types', dest='record_types', nargs='+', default=['JetCorrectorParametersCollection'], help='list of record types to be uploaded')
  parser.add_argument('-d', '--db', default='prep', choices=['prep', 'prod'], help='keyword for the target database -- must be "prep" (default) or "prod"')
  parser.add_argument('-c', '--cache-dir', dest='cache_dir', default='/tmp/'+os.environ['USER'], help='path to directory where files are cached prior to upload')
  parser.add_argument('-t', '--txt', required=True, help='description of payloads')
  parser.add_argument('--dry-run', dest='dry_run', action='store_true', help='execute in dry-run mode (no upload to db)')
  args, unknown_args = parser.parse_known_args()

  if len(unknown_args) > 0:
    raise RuntimeError('unknown command-line arguments: '+str(unknown_args))

  if not os.path.isfile(args.dbfile):
    raise RuntimeError('invalid path to .db file: '+str(args.dbfile))

  if args.dbfile[-3:] != '.db':
    raise RuntimeError('db file does not end in .db: {}'.format(args.dbfile))

  try:
    cmd = 'conddb --db {filename} listTags'.format(filename=args.dbfile)
    out, err = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
  except:
    raise RuntimeError('call to conddb failed (first enable a CMSSW area with cmsenv): '+cmd)

  tags = []
  for line in out.split('\n'):
    try:
      if line.split()[2] in args.record_types:
        tags.append(line.split()[0])
    except IndexError:
      pass

  if args.db == 'prod':
    database = 'oracle://cms_orcon_prod/CMS_CONDITIONS'
    print '-'*100+'\n'+'>>> '+('would upload' if args.dry_run else 'uploading')+' to production database: '+database+'\n'+'-'*100
  elif args.db == 'prep':
    database = 'oracle://cms_orcoff_prep/CMS_CONDITIONS'
    print '-'*100+'\n'+'>>> '+('would upload' if args.dry_run else 'uploading')+' to development database (prep): '+database+'\n'+'-'*100

  if not args.dry_run:
    try:
      os.makedirs(args.cache_dir)
    except:
      if not os.path.isdir(args.cache_dir):
        raise RuntimeError('target cache directory does not exist: '+args.cache_dir)

  upload_cmd = 'uploadConditions.py'

  tag_file_txt_format = args.cache_dir+'/'+os.path.splitext(os.path.basename(__file__))[0]+'_{tagnr}_{tag}.txt'

  for tagnr, tag in enumerate(tags):
    tag_file_txt = tag_file_txt_format.format(tagnr=tagnr, tag=tag)
    tag_file_db = tag_file_txt[:-3]+'db'

    if not args.dry_run:
      shutil.copy2(args.dbfile, tag_file_db)

    upload_cmd += ' '+tag_file_db

    metadata = {
      'destinationDatabase': database,
      'destinationTags': {tag : {}}, 
      'inputTag': tag,
      'since': 1, 
      'userText': args.txt,
    }

    print '\n'+'*'*100
    print '.db  :', tag_file_db
    print '.txt :', tag_file_txt
    print json.dumps(metadata, sort_keys=True, indent=4)
    print '*'*100

    if not args.dry_run:
      json.dump(metadata, open(tag_file_txt, 'w'))

  print '\n'+'-'*100
  print '>', upload_cmd
  print '-'*100

  if not args.dry_run:
    print '\n>>> will upload in 10 sec'
    time.sleep(10)
    subprocess.Popen(upload_cmd.split()).communicate()
