#!/usr/bin/env python
"""
Script to create a copy of an ntuple with the TDirectories ak4puppiHLT and ak8puppiHLT
renamed to ak4puppi and ak8puppi preserving the TTree named 't' inside.
This allows the usage of tools in JetMETAnalysis.

This script takes an HLT JRA NTuple (see https://github.com/missirol/JMETriggerAnalysis/tree/phase2) 
as input, and it will output one file with renamed directories.

Example:

./renameJRADirs.py -i jra_input.root -o jra_output.root
"""
import argparse
import os
import ROOT

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('-i', '--input', dest='inputf', required=True, action='store', default='',
                      help='path to input file')
  parser.add_argument('-o', '--output', dest='outputf', required=True, action='store', default='',
                      help='path to output file')
  parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                      help='verbosity level')
  opts, opts_unknown = parser.parse_known_args()

  if len(opts_unknown) > 0:
    raise RuntimeError('unknown command-line arguments: '+str(opts_unknown))

  if os.path.exists(opts.outputf):
    raise RuntimeError('target output file already exists: '+opts.outputf)

  # input file
  infile = ROOT.TFile.Open(opts.inputf)
  if not infile:
    raise RuntimeError('input file is not valid: '+opts.inputf)

  # output file
  outfile = ROOT.TFile(opts.outputf, 'recreate')
  if not outfile:
    raise RuntimeError('failed to create target output file: '+opts.outputf)

  # clone of input TTrees to output file
  dirNameDict = {
    'ak4puppi': 'ak4puppiHLT',
    'ak8puppi': 'ak8puppiHLT',
  }

  if opts.verbosity > 0:
    print 'input  :', opts.inputf

  for _key in sorted(dirNameDict.keys()):
    _inpTree = infile.Get(dirNameDict[_key]+'/t')
    if not _inpTree:
      if opts.verbosity > -10:
        print '** TTree named "'+dirNameDict[_key]+'/t" not found in input file (will be skipped): '+opts.inputf
      continue
    outfile.cd()
    _tmpDir = outfile.mkdir(_key)
    _tmpDir.cd()
    _outTree = _inpTree.CloneTree()
    _outTree.Write()
    if opts.verbosity > 1:
      print '>> cloned TTree "'+dirNameDict[_key]+'/t" (input) to TTree "'+_key+'/'+_outTree.GetName()+'" (output)'

  # close input and output files
  outfile.Close()
  infile.Close()

  if opts.verbosity > 0:
    print 'output :', opts.outputf
