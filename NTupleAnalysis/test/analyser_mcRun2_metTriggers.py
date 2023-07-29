#!/usr/bin/env python
"""simple analyser to fill MET histograms via TTree::Draw"""
import os
import argparse
import ROOT

from common.utils import *
from common.efficiency import *

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser(description=__doc__)

#   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=[],
#                       help='path to input file(s)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default='',
                       help='path to output file (1 input) or directory (multiple inputs')

   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                       help='enable verbose mode')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   log_prx = os.path.basename(__file__)+' -- '

   ROOT.gROOT.SetBatch()

   ROOT.gErrorIgnoreLevel = ROOT.kError

   ### args validation ---
   f0 = ROOT.TFile('/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/JetMET_PhaseII/JMETriggerAnalysis_phase2/ntuples/output_mc2018_forHLTTDR/RunIIAutumn18MiniAOD_VBF_HToInvisible_13TeV.root')
   t0 = f0.Get('JMETriggerNTuple/Events')

   bins_met = array.array('d', [_tmp*5. for _tmp in range(161)])

   histograms = {}
   for _tmpDir, _tmpVar, _tmpCut in [
     ['NoSelection', 'genMETTrue_pt', ''],
     ['HLT_PFMET110_PFMHT110_IDTight', 'genMETTrue_pt', 'HLT_PFMET110_PFMHT110_IDTight == 1'],
     ['HLT_PFMET120_PFMHT120_IDTight', 'genMETTrue_pt', 'HLT_PFMET120_PFMHT120_IDTight == 1'],
     ['HLT_PFMET130_PFMHT130_IDTight', 'genMETTrue_pt', 'HLT_PFMET130_PFMHT130_IDTight == 1'],
     ['HLT_PFMET140_PFMHT140_IDTight', 'genMETTrue_pt', 'HLT_PFMET140_PFMHT140_IDTight == 1'],
     #['HLT_PFMETTypeOne110_PFMHT110_IDTight', 'genMETTrue_pt', 'HLT_PFMETTypeOne110_PFMHT110_IDTight == 1'],
     #['HLT_PFMETTypeOne120_PFMHT120_IDTight', 'genMETTrue_pt', 'HLT_PFMETTypeOne120_PFMHT120_IDTight == 1'],
     #['HLT_PFMETTypeOne130_PFMHT130_IDTight', 'genMETTrue_pt', 'HLT_PFMETTypeOne130_PFMHT130_IDTight == 1'],
     #['HLT_PFMETTypeOne140_PFMHT140_IDTight', 'genMETTrue_pt', 'HLT_PFMETTypeOne140_PFMHT140_IDTight == 1'],
   ]:
     hname = 'h'+str(len(histograms.keys()))
     h0 = ROOT.TH1D(hname, hname, len(bins_met)-1, bins_met)
     h0.Sumw2()
     t0.Draw(_tmpVar+'>>'+hname, _tmpCut, 'goff')
     histograms[_tmpDir+'/'+_tmpVar] = h0.Clone()
     histograms[_tmpDir+'/'+_tmpVar].SetDirectory(0)
     if opts.verbose:
       print _tmpDir+'/'+_tmpVar, '("'+_tmpCut+'")', '[#events = '+str(histograms[_tmpDir+'/'+_tmpVar].GetEntries())+']'

   f0.Close()

   ### output file -------
   output_file = opts.output

   output_dirname = os.path.dirname(os.path.abspath(output_file))
   MKDIRP(output_dirname, verbose=opts.verbose, dry_run=opts.dry_run)

   if not opts.dry_run:
     output_tfile = ROOT.TFile(output_file, 'create')
     if (not output_tfile) or output_tfile.IsZombie() or output_tfile.TestBit(ROOT.TFile.kRecovered):
       raise RuntimeError(output_file)

     for i_idx in sorted(histograms.keys()):
       if hasattr(histograms[i_idx], 'GetEntries') and (histograms[i_idx].GetEntries() == 0):
         continue

       output_tfile.cd()

       out_key = i_idx

       while '/' in out_key:
         slash_index = out_key.find('/')
         out_dir = out_key[:slash_index]
         out_key = out_key[slash_index+1:]
         out_dir = getattr(output_tfile, 'Get' if output_tfile.Get(out_dir) else 'mkdir')(out_dir)
         out_dir.cd()

       histograms[i_idx].SetName(out_key)
       histograms[i_idx].SetTitle(out_key)
       histograms[i_idx].Write()

     output_tfile.Close()

   print colored_text('[output]', ['1','92']), os.path.relpath(output_file)
   ### -------------------
