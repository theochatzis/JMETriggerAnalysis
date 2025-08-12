#!/usr/bin/env python3
"""add harvesting products (e.g. profiles, efficiencies)"""
import os
import argparse
import glob
import ctypes
import ROOT

from common.utils import *
from common.efficiency import *

def updateDictionary(dictionary, TDirectory, prefix=''):

    key_prefix = ''
    if len(prefix) > 0: key_prefix = prefix+'/'

    for j_key in TDirectory.GetListOfKeys():

        j_key_name = j_key.GetName()

        j_obj = TDirectory.Get(j_key_name)

        if j_obj.InheritsFrom('TDirectory'):

           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name)

        elif j_obj.InheritsFrom('TH1'):

           out_key = key_prefix+j_key_name

           if out_key in dictionary:
              KILL(log_prx+'input error -> found duplicate of template ["'+out_key+'"] in input file: '+TDirectory.GetName())

           dictionary[out_key] = j_obj.Clone()
#           dictionary[out_key].SetDirectory(0)

           if opts.verbose:
              print (colored_text('[input]', ['1', '92']), out_key)

    return dictionary

def getTH1sFromTFile(tfile):

    input_histos_dict = {}

    updateDictionary(input_histos_dict, tfile, prefix='')

    return input_histos_dict

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser(description=__doc__)

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=[],
                       help='path to input file(s)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default='',
                       help='path to output file (1 input) or directory (multiple inputs')

   parser.add_argument('-s', '--separator-2d', dest='separator_2d', action='store', default='__vs__',
                       help='string used to split name of 2D histograms (to construct profile histograms)')

   parser.add_argument('-l', '--level', dest='level', action='store', type=int, default=0,
                       help='level of directory depth in output directory')

   parser.add_argument('--copy-only', dest='copy_only', action='store_true', default=False,
                       help='disable addition of new objects (e.g. profiles)')

   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                       help='enable verbose mode')

   parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                       help='enable dry-run mode')
   
   parser.add_argument('-me', '--make-eff', dest='make_matching_eff', action='store_false', default=True,
                       help='make matching efficiencies, will require NoSelection directory')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   log_prx = os.path.basename(__file__)+' -- '

   ROOT.gROOT.SetBatch()

   ROOT.gErrorIgnoreLevel = ROOT.kError

   ### args validation ---
   if opts.level < 0:
      KILL(log_prx+'negative level of directory depth in output directory (must be >=0) [-l]: '+str(opts.level))

   INPUT_FILES = []
   for i_inpf in opts.inputs:
       i_inpf_ls = glob.glob(i_inpf)
       for i_inpf_2 in i_inpf_ls:
           if os.path.isfile(i_inpf_2):
              INPUT_FILES += [os.path.abspath(os.path.realpath(i_inpf_2))]
   INPUT_FILES = sorted(list(set(INPUT_FILES)))

   if len(INPUT_FILES) == 0:
      KILL(log_prx+'empty list of input files')

#  if os.path.exists(opts.output):
#     KILL(log_prx+'target path to output file/directory already exists [-o]: '+opts.output)
   ### -------------------

   ROOT.TH1.AddDirectory(False)

   for inpf in INPUT_FILES:

       ### Input Histograms
       i_inptfile = ROOT.TFile.Open(inpf)
       if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
          continue

       histograms = getTH1sFromTFile(i_inptfile)

       if not opts.copy_only:
          ### Histograms for profile of Mean
          for i_h2_key in sorted(histograms.keys()):
   
              if not histograms[i_h2_key].InheritsFrom('TH2'):
                 continue
              elif histograms[i_h2_key].GetEntries() == 0:
                 continue
   
              i_h2_key_basename = os.path.basename(i_h2_key)
   
              i_h2_key_dirname = os.path.dirname(i_h2_key)
              if i_h2_key_dirname: i_h2_key_dirname += '/'
   
              key_vars_split = i_h2_key_basename.split(opts.separator_2d)
              if len(key_vars_split) != 2:
                 KILL('ZZZ '+i_h2_key_basename)
   
              key_varX = key_vars_split[0]
              key_varY = key_vars_split[1]
              
              
              #if not (key_varX.endswith('GEN') or key_varX.endswith('Offline')):
              #   continue
              if not (key_varX.endswith('GEN') or key_varX.endswith('Offline') or ('njets' in key_varX)):
                 continue
         

              tmp_h2 = histograms[i_h2_key]

              # Mean of X, in bins of Y
              h_name0 = i_h2_key_dirname+key_varX+'_Mean_wrt_'+key_varY
              if h_name0 in histograms: KILL('aaa1 '+h_name0)
   
              tmp_h1_xMean = tmp_h2.ProjectionY(h_name0)
#              tmp_h1_xMean.SetDirectory(0)
              tmp_h1_xMean.Reset()
   
              for _idx in range(1, 1+tmp_h2.GetNbinsY()):
                  _htmp = tmp_h2.ProjectionX('_htmp'+str(_idx), _idx, _idx, 'e')
#                  _htmp.SetDirectory(0)

                  _val = _htmp.GetMean()
                  _err = _htmp.GetMeanError()
#                  _med, _medQ = ctypes.c_double(0.), ctypes.c_double(0.5)
#                  _htmp.ComputeIntegral()
#                  _htmp.GetQuantiles(1, _med, _medQ)
#                  _val = _med.value
#                  _err = 1.253 * _htmp.GetMeanError()

                  tmp_h1_xMean.SetBinContent(_idx, _val)
                  tmp_h1_xMean.SetBinError(_idx, _err)

#                  histograms[h_name0+'_'+str(_idx)] = _htmp.Clone()
                  del _htmp
   
              histograms[h_name0] = tmp_h1_xMean
          ### -------------------
   
          ### Histograms for profile of RMS
          ### (requires mean-Response histograms created in previous block)
          for i_h2_key in sorted(histograms.keys()):
   
              if not histograms[i_h2_key].InheritsFrom('TH2'):
                 continue
              elif histograms[i_h2_key].GetEntries() == 0:
                 continue
   
              i_h2_key_basename = os.path.basename(i_h2_key)
   
              i_h2_key_dirname = os.path.dirname(i_h2_key)
              if i_h2_key_dirname: i_h2_key_dirname += '/'
   
              key_vars_split = i_h2_key_basename.split(opts.separator_2d)
              if len(key_vars_split) != 2:
                 KILL('ZZZ '+i_h2_key_basename)
   
              key_varX = key_vars_split[0]
              key_varY = key_vars_split[1]
   
              if key_varX.endswith('GEN'): compTag = 'GEN'
              elif key_varX.endswith('Offline'): compTag = 'Offline'
              else: continue
   
              tmp_h2 = histograms[i_h2_key]
   
              # RMS of X, in bins of Y
              h_name1 = i_h2_key_dirname+key_varX+'_RMS_wrt_'+key_varY
              if h_name1 in histograms: KILL('aaa3 '+h_name1)
   
              tmp_h1_xRMS = tmp_h2.ProjectionY(h_name1)
#              tmp_h1_xRMS.SetDirectory(0)
              tmp_h1_xRMS.Reset()
   
              for _idx in range(1, 1+tmp_h2.GetNbinsY()):
                  _htmp = tmp_h2.ProjectionX('_htmp'+str(_idx), _idx, _idx, 'e')
#                  _htmp.SetDirectory(0)
                  tmp_h1_xRMS.SetBinContent(_idx, _htmp.GetRMS())
                  tmp_h1_xRMS.SetBinError(_idx, _htmp.GetRMSError())
                  del _htmp
   
              histograms[h_name1] = tmp_h1_xRMS

              # RMS of X divided by Mean Response, in bins of Y
              h_name2 = i_h2_key_dirname+key_varX+'_RMSOverMean_wrt_'+key_varY
              if h_name2 in histograms: KILL('aaa4 '+h_name2)

              h_name4 = i_h2_key_dirname+key_varX[:key_varX.rfind('_')]+'_over'+compTag+'_Mean_wrt_'+key_varY
              if h_name4 not in histograms:
                 if opts.verbose:
                    WARNING('aaa5 '+h_name2+' '+h_name4)
              else:
                 tmp_h1_ratioMeanNoErr = histograms[h_name4].Clone()
                 for _idx in range(tmp_h1_ratioMeanNoErr.GetNbinsX()+2):
                     tmp_h1_ratioMeanNoErr.SetBinError(_idx, 0)
   
                 tmp_h1_xRMSScaled = tmp_h1_xRMS.Clone()
                 tmp_h1_xRMSScaled.SetName(h_name2)
#                 tmp_h1_xRMSScaled.SetDirectory(0)
                 tmp_h1_xRMSScaled.Divide(tmp_h1_ratioMeanNoErr)

                 histograms[h_name2] = tmp_h1_xRMSScaled
                 del tmp_h1_ratioMeanNoErr
          ### -------------------
   
          ### Matching Efficiencies
          for hkey_i in sorted(histograms.keys()):
   
              if histograms[hkey_i].InheritsFrom('TH1') and (histograms[hkey_i].GetEntries() == 0):
                 continue
              elif histograms[hkey_i].InheritsFrom('TGraph') and (histograms[hkey_i].GetN() == 0):
                 continue
   
              hkey_i_basename = os.path.basename(hkey_i)
   
              if '_wrt_' in hkey_i_basename:
                 continue
   
              hkey_i_dirname = os.path.dirname(hkey_i)
              if hkey_i_dirname: hkey_i_dirname += '/'
   
              if not (('_MatchedTo' in hkey_i_basename) or ('_NotMatchedTo' in hkey_i_basename)):
                 continue
   
              if (opts.separator_2d in hkey_i_basename) and (not hkey_i_basename.endswith('_eta__vs__pt')):
                 continue
              
              #elif not (hkey_i_basename.endswith('_pt') or hkey_i_basename.endswith('_eta') or hkey_i_basename.endswith('_phi')):
              #   continue
              elif not (hkey_i_basename.endswith('_pt') or hkey_i_basename.endswith('_eta') or hkey_i_basename.endswith('_phi') or hkey_i_basename.endswith('_simNPU')):
                 continue
              
   
              hkey_i_num, hkey_i_den = hkey_i_dirname+hkey_i_basename, None
              if '_MatchedTo' in hkey_i_basename:
                 hkey_i_den1 = hkey_i_basename.split('_MatchedTo')[0]
                 hkey_i_den2 = hkey_i_basename.split('_MatchedTo')[1]
                 hkey_i_den = hkey_i_dirname+hkey_i_den1+hkey_i_den2[hkey_i_den2.find('_'):]
              elif '_NotMatchedTo' in hkey_i_basename:
                 hkey_i_den1 = hkey_i_basename.split('_NotMatchedTo')[0]
                 hkey_i_den2 = hkey_i_basename.split('_NotMatchedTo')[1]
                 hkey_i_den = hkey_i_dirname+hkey_i_den1+hkey_i_den2[hkey_i_den2.find('_'):]
   
              if hkey_i_num not in histograms:
                 KILL(log_prx+'AAA '+hkey_i_num)
   
              if hkey_i_den not in histograms:
                 KILL(log_prx+'BBB '+hkey_i_den)
   
              tmp_hnum = histograms[hkey_i_num]
              tmp_hden = histograms[hkey_i_den]
   
              if hkey_i_num+'_eff' in histograms:
                 KILL(log_prx+'CCC '+hkey_i_num+'_eff')
   
              if tmp_hnum.InheritsFrom('TH2') and tmp_hden.InheritsFrom('TH2'):
                 tmp_hratio = tmp_hnum.Clone()
                 tmp_hratio.Divide(tmp_hden)
                 histograms[hkey_i_num+'_eff'] = tmp_hratio
              else:
                 histograms[hkey_i_num+'_eff'] = get_efficiency_graph(tmp_hnum, tmp_hden)
          ### -------------------

          ### Histograms for trigger rates
          for i_h2_key in sorted(histograms.keys()):

              if histograms[i_h2_key].InheritsFrom('TH2') or histograms[i_h2_key].InheritsFrom('TH3'):
                 continue

              if not (histograms[i_h2_key].InheritsFrom('TH1') and (histograms[i_h2_key].GetEntries() > 0)):
                 continue

              i_h2_key_basename = os.path.basename(i_h2_key)

              i_h2_key_dirname = os.path.dirname(i_h2_key)
              if i_h2_key_dirname: i_h2_key_dirname += '/'

              keep_th1 = bool(('Jets' in i_h2_key_basename) and (i_h2_key_basename.endswith('_pt0') or i_h2_key_basename.endswith('_HT') or i_h2_key_basename.endswith('_MHT')) and ('MatchedTo' not in i_h2_key_basename))
              keep_th1 += bool(('MET' in i_h2_key_basename) and i_h2_key_basename.endswith('_pt') and ('GEN_' not in i_h2_key_basename) and ('Offline_' not in i_h2_key_basename))
              if not keep_th1: continue

              tmp_h1 = histograms[i_h2_key].Clone()

              tmp_h1_name = i_h2_key+'_cumul'
              if tmp_h1_name in histograms: KILL('aaa4 '+tmp_h1_name)

              tmp_h1.SetTitle(tmp_h1.GetName()+'_cumul')
              tmp_h1.SetName(tmp_h1.GetName()+'_cumul')
#              tmp_h1.SetDirectory(0)

              for _tmp_bin_i in range(1, 1+tmp_h1.GetNbinsX()):
                  _err = ctypes.c_double(0.)
                  tmp_h1.SetBinContent(_tmp_bin_i, tmp_h1.IntegralAndError(_tmp_bin_i, -1, _err))
                  tmp_h1.SetBinError(_tmp_bin_i, _err.value)

              histograms[tmp_h1_name] = tmp_h1
          ### -------------------

          ### Trigger Efficiencies [HLT_*Jet*]
          for hkey_i in sorted(histograms.keys()):

              if histograms[hkey_i].InheritsFrom('TH1') and (histograms[hkey_i].GetEntries() == 0):
                 continue
              elif histograms[hkey_i].InheritsFrom('TGraph') and (histograms[hkey_i].GetN() == 0):
                 continue

              hkey_i_basename = os.path.basename(hkey_i)

              if '_wrt_' in hkey_i_basename:
                 continue

              if not (('_MatchedTo' in hkey_i_basename) and ('_pt0' in hkey_i_basename) and (opts.separator_2d in hkey_i_basename)):
                 continue
   
              hkey_i_dirname = os.path.dirname(hkey_i)
              if hkey_i_dirname: hkey_i_dirname += '/'
   
              if not (('HLT_' in hkey_i_dirname) and ('Jet' in hkey_i_dirname)):
                 continue
              
              if opts.make_matching_eff:
               hkey_i_num = hkey_i
               hkey_i_den = 'NoSelection/'+hkey_i_basename
      
               if hkey_i_num not in histograms: KILL(log_prx+'AAA2 '+hkey_i_num)
               if hkey_i_den not in histograms: KILL(log_prx+'BBB2 '+hkey_i_den)
      
               tmp_hnum = histograms[hkey_i_num]
               tmp_hden = histograms[hkey_i_den]
      
               if not tmp_hnum.InheritsFrom('TH2'): KILL(log_prx+'AAA3 '+hkey_i_num)
               if not tmp_hden.InheritsFrom('TH2'): KILL(log_prx+'BBB3 '+hkey_i_den)
      
               tmp_hnum0 = tmp_hnum.ProjectionY('tmp_hnum0')
               tmp_hden0 = tmp_hden.ProjectionY('tmp_hden0')

               tmp_effname = hkey_i_num.replace(opts.separator_2d, '_')+'_eff'
      
               if tmp_effname in histograms: KILL(log_prx+'CCC2 '+tmp_effname)
   
               print (tmp_effname)
               histograms[tmp_effname] = get_efficiency_graph(tmp_hnum0, tmp_hden0)

              del tmp_hnum0
              del tmp_hden0
          ### -------------------

       ### output file -------
       output_file = None
       if (len(INPUT_FILES) == -1) and (opts.level == 0):
          output_file = opts.output
       else:
          input_name_pieces = [os.path.basename(inpf)]
          input_dirname = os.path.dirname(inpf)
          while opts.level >= len(input_name_pieces):
             input_name_pieces.insert(0, os.path.basename(input_dirname))
             input_dirname = os.path.dirname(input_dirname)
          del input_dirname
          output_file = opts.output+'/'+('/'.join(input_name_pieces))

       if os.path.exists(output_file):
          WARNING(log_prx+'logic error - target output file already exists (will be skipped): '+output_file)
          continue

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

       i_inptfile.Close()

       #for _tmp in histograms.keys():
       #  del histograms[_tmp]
       for _tmp in list(histograms):
         del histograms[_tmp]

       print (colored_text('[output]', ['1','92']), os.path.relpath(output_file))
       ### -------------------
