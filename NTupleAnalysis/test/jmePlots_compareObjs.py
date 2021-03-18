#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import ROOT

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

from jmePlots_compareFiles import updateDictionary, getTH1sFromTFile, Histogram, plot, getPlotLabels

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', nargs='+', default=[], required=True,
                       help='list of input files [format: "PATH:LEGEND:LINECOLOR:LINESTYLE:MARKERSTYLE:MARKERCOLOR:MARKERSIZE"]')

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                       help='path to output directory')

   parser.add_argument('-k', '--keywords', dest='keywords', nargs='+', default=[],
                       help='list of keywords to skim inputs (input is a match if any of the keywords is part of the input\'s name)')

   parser.add_argument('-l', '--label', dest='label', action='store', default='',
                       help='text label (displayed in top-left corner)')

   parser.add_argument('-u', '--upgrade', dest='upgrade', action='store_true', default=False,
                       help='labels for Phase-2 plots')

   parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf'],
                       help='list of extension(s) for output file(s)')

   parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                       help='verbosity level')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   ROOT.gROOT.SetBatch()
   ROOT.gErrorIgnoreLevel = ROOT.kWarning

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation ---
   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output directory already exists [-o]: '+opts.output)

   OUTDIR = os.path.abspath(os.path.realpath(opts.output))

   KEYWORDS = sorted(list(set(opts.keywords)))
   KEYWORDS = [_tmp.replace('\'','').replace('"','') for _tmp in KEYWORDS]

   EXTS = list(set(opts.exts))
   ### -------------------

   if len(opts.inputs) > 1:
      raise RuntimeError('')

   inputList = []
   th1Keys = []
   for _input in opts.inputs:
       _input_pieces = _input.split(':')
       if len(_input_pieces) >= 3:
          _tmp = {}
          _tmp['TH1s'] = getTH1sFromTFile(_input_pieces[0], keywords=KEYWORDS, verbose=(opts.verbosity > 20))
          th1Keys += _tmp['TH1s'].keys()
          _tmp['Legend'] = _input_pieces[1]
          _tmp['LineColor'] = int(_input_pieces[2])
          _tmp['LineStyle'] = int(_input_pieces[3]) if len(_input_pieces) >= 4 else 1
          _tmp['MarkerStyle'] = int(_input_pieces[4]) if len(_input_pieces) >= 5 else 20
          _tmp['MarkerColor'] = int(_input_pieces[5]) if len(_input_pieces) >= 6 else int(_input_pieces[2])
          _tmp['MarkerSize'] = float(_input_pieces[6]) if len(_input_pieces) >= 7 else 1.0
          inputList.append(_tmp)
       else:
          KILL(log_prx+'argument of --inputs has invalid format: '+_input)

   if not inputList:
      raise SystemExit(0)

   th1Keys = sorted(list(set(th1Keys)))

   apply_style(0)

   ROOT.TGaxis.SetMaxDigits(4)

   Top = ROOT.gStyle.GetPadTopMargin()
   Rig = ROOT.gStyle.GetPadRightMargin()
   Bot = ROOT.gStyle.GetPadBottomMargin()
   Lef = ROOT.gStyle.GetPadLeftMargin()

   ROOT.TGaxis.SetExponentOffset(-Lef+.50*Lef, 0.03, 'y')

   label_sample = get_text(Lef+(1-Lef-Rig)*0.00, (1-Top)+Top*0.25, 11, .035, opts.label)

   for _hkey in th1Keys:

       _hkey_basename = os.path.basename(_hkey)

       if ('_wrt_' not in _hkey_basename) and (not _hkey_basename.endswith('_eff')) and (not ('MET' in _hkey_basename and _hkey_basename.endswith('_pt'))) and ('pt_over' not in _hkey_basename):
          continue

       if ('/' in _hkey) and (not _hkey.startswith('NoSelection/')):
          if ('_pt0' not in _hkey_basename) or _hkey_basename.endswith('pt0_eff') or _hkey_basename.endswith('pt0') or ('pt0_over' in _hkey_basename):
             continue

       _hIsProfile = '_wrt_' in _hkey_basename

       _hIsEfficiency = _hkey_basename.endswith('_eff')

       _hkey_jmeColl, _leg_jmeColl, _jmeCollList = None, '', []

       if opts.upgrade:
          if 'hltPFMET_' in _hkey:
             _hkey_jmeColl = 'hltPFMET'
             _leg_jmeColl = 'MET'
             _jmeCollList = [
#              ('offlinePFMET_Raw'   , ROOT.kPink+3  , [inputList[0]]),
               ('offlinePuppiMET_Raw', ROOT.kPink+1  , [inputList[0]]),
               ('hltPFClusterMET'    , ROOT.kOrange+1, [inputList[0]]),
               ('hltPFMET'           , ROOT.kBlack   ,  inputList    ),
               ('PFSoftKillerMET'    , ROOT.kBlue    ,  inputList    ),
               ('hltPFCHSMET'        , ROOT.kViolet  ,  inputList    ),
               ('hltPuppiMET'        , ROOT.kRed     ,  inputList    ),
             ]
          elif 'hltAK4PFJets_' in _hkey:
             _hkey_jmeColl = 'hltAK4PFJets'
             _leg_jmeColl = 'HLT AK4'
             _jmeCollList = [
               ('hltAK4CaloJets'     , ROOT.kGray+1  , [inputList[0]]),
               ('hltAK4PFClusterJets', ROOT.kOrange+1, [inputList[0]]),
               ('hltAK4PFJets'       , ROOT.kBlack   ,  inputList    ),
#              ('hltAK4PFCHSJets'    , ROOT.kViolet  ,  inputList    ),
               ('hltAK4PuppiJets'    , ROOT.kRed     ,  inputList    ),
             ]
          elif 'hltAK4PFJetsCorrected_' in _hkey:
             _hkey_jmeColl = 'hltAK4PFJetsCorrected'
             _leg_jmeColl = 'HLT AK4'
             _jmeCollList = [
#              ('offlineAK4PuppiJetsCorrected', ROOT.kPink+1  , [inputList[0]]),
#              ('hltAK4CaloJets'              , ROOT.kGray+1  , [inputList[0]]),
#              ('hltAK4PFClusterJets'         , ROOT.kOrange+1, [inputList[0]]),
               ('hltAK4PFJetsCorrected'       , ROOT.kBlack   ,  inputList    ),
               ('hltAK4PFCHSJetsCorrected'    , ROOT.kViolet  ,  inputList    ),
               ('hltAK4PuppiJetsCorrected'    , ROOT.kRed     ,  inputList    ),
             ]
          elif 'hltAK8PFJets_' in _hkey:
             _hkey_jmeColl = 'hltAK8PFJets'
             _leg_jmeColl = 'HLT AK8'
             _jmeCollList = [
               ('hltAK8CaloJets'     , ROOT.kGray+1  , [inputList[0]]),
               ('hltAK8PFClusterJets', ROOT.kOrange+1, [inputList[0]]),
               ('hltAK8PFJets'       , ROOT.kBlack   ,  inputList    ),
#              ('hltAK8PFCHSJets'    , ROOT.kViolet  ,  inputList    ),
               ('hltAK8PuppiJets'    , ROOT.kRed     ,  inputList    ),
             ]
          elif 'hltAK8PFJetsCorrected_' in _hkey:
             _hkey_jmeColl = 'hltAK8PFJetsCorrected'
             _leg_jmeColl = 'HLT AK8'
             _jmeCollList = [
#              ('offlineAK8PuppiJetsCorrected', ROOT.kPink+1  , [inputList[0]]),
#              ('hltAK8CaloJets'              , ROOT.kGray+1  , [inputList[0]]),
#              ('hltAK8PFClusterJets'         , ROOT.kOrange+1, [inputList[0]]),
               ('hltAK8PFJetsCorrected'       , ROOT.kBlack   ,  inputList    ),
               ('hltAK8PFCHSJetsCorrected'    , ROOT.kViolet  ,  inputList    ),
               ('hltAK8PuppiJetsCorrected'    , ROOT.kRed     ,  inputList    ),
             ]
          elif 'MatchedToPF_' in _hkey:
             _hkey_jmeColl = 'PF'
             _leg_jmeColl = 'HLT'
             _jmeCollList = [
               ('Calo'     , ROOT.kGray+1  , [inputList[0]]),
               ('PFCluster', ROOT.kOrange+1, [inputList[0]]),
               ('PF'       , ROOT.kBlack   ,  inputList    ),
#              ('PFCHS'    , ROOT.kViolet  ,  inputList    ),
               ('Puppi'    , ROOT.kRed     ,  inputList    ),
             ]
          elif 'MatchedToPFCorr_' in _hkey:
             _hkey_jmeColl = 'PFCorr'
             _leg_jmeColl = 'HLT'
             _jmeCollList = [
#              ('OfflinePuppiCorr', ROOT.kPink+1  , [inputList[0]]),
#              ('Calo'            , ROOT.kGray+1  , [inputList[0]]),
#              ('PFCluster'       , ROOT.kOrange+1, [inputList[0]]),
               ('PFCorr'          , ROOT.kBlack   ,  inputList    ),
               ('PFCHSCorr'       , ROOT.kViolet  ,  inputList    ),
               ('PuppiCorr'       , ROOT.kRed     ,  inputList    ),
             ]
       else:
          if 'hltPFMET_' in _hkey:
             _hkey_jmeColl = 'hltPFMET'
             _leg_jmeColl = 'MET'
             _jmeCollList = [
#              ('offlinePFMET_Raw', ROOT.kPink+3, [inputList[0]]),
               ('offlinePuppiMET_Raw', ROOT.kPink+1, [inputList[0]]),
               ('hltPFMET', 1, inputList),
               ('hltCaloMET', ROOT.kGray+1, inputList),
               ('hltPFCHSv1MET', ROOT.kBlue, inputList),
               ('hltPFCHSv2MET', ROOT.kViolet, inputList),
               ('hltPuppiV2MET', ROOT.kRed, inputList),
               ('hltPuppiV4MET', ROOT.kOrange+1, inputList),
             ]
          elif 'hltAK4PFJets_' in _hkey:
             _hkey_jmeColl = 'hltAK4PFJets'
             _leg_jmeColl = 'HLT AK4'
             _jmeCollList = [
               ('offlineAK4PuppiJetsCorrected', ROOT.kPink+1, [inputList[0]]),
               ('hltAK4CaloJets', ROOT.kGray+1, inputList),
               ('hltAK4PFClusterJets', ROOT.kGreen-5, inputList),
               ('hltAK4PFJets', ROOT.kBlack, inputList),
               ('hltAK4PFCHSv1Jets', ROOT.kBlue, inputList),
               ('hltAK4PFCHSv2Jets', ROOT.kViolet, inputList),
               ('hltAK4PuppiV1Jets', ROOT.kOrange+1, inputList),
               ('hltAK4PuppiV3Jets', ROOT.kRed, inputList),
             ]
          elif 'hltAK4PFJetsCorrected_' in _hkey:
             _hkey_jmeColl = 'hltAK4PFJetsCorrected'
             _leg_jmeColl = 'HLT AK4'
             _jmeCollList = [
               ('offlineAK4PuppiJetsCorrected', ROOT.kPink+1, [inputList[0]]),
               ('hltAK4CaloJetsCorrected', ROOT.kGray+1, inputList),
               ('hltAK4PFJetsCorrected', ROOT.kBlack, inputList),
               ('hltAK4PFCHSv1JetsCorrected', ROOT.kBlue, inputList),
               ('hltAK4PFCHSv2JetsCorrected', ROOT.kViolet, inputList),
               ('hltAK4PuppiV1JetsCorrected', ROOT.kOrange+1, inputList),
               ('hltAK4PuppiV3JetsCorrected', ROOT.kRed, inputList),
             ]
          elif 'hltAK8PFJets_' in _hkey:
             _hkey_jmeColl = 'hltAK8PFJets'
             _leg_jmeColl = 'HLT AK8'
             _jmeCollList = [
               ('offlineAK8PuppiJetsCorrected', ROOT.kPink+1, [inputList[0]]),
               ('hltAK8CaloJets', ROOT.kGray+1, inputList),
               ('hltAK8PFClusterJets', ROOT.kGreen-5, inputList),
               ('hltAK8PFJets', ROOT.kBlack, inputList),
               ('hltAK8PFCHSv1Jets', ROOT.kBlue, inputList),
               ('hltAK8PFCHSv2Jets', ROOT.kViolet, inputList),
               ('hltAK8PuppiV1Jets', ROOT.kOrange+1, inputList),
               ('hltAK8PuppiV3Jets', ROOT.kRed, inputList),
             ]
          elif 'hltAK8PFJetsCorrected_' in _hkey:
             _hkey_jmeColl = 'hltAK8PFJetsCorrected'
             _leg_jmeColl = 'HLT AK8'
             _jmeCollList = [
               ('offlineAK8PuppiJetsCorrected', ROOT.kPink+1, [inputList[0]]),
               ('hltAK8CaloJetsCorrected', ROOT.kGray+1, inputList),
               ('hltAK8PFJetsCorrected', ROOT.kBlack, inputList),
               ('hltAK8PFCHSv1JetsCorrected', ROOT.kBlue, inputList),
               ('hltAK8PFCHSv2JetsCorrected', ROOT.kViolet, inputList),
               ('hltAK8PuppiV1JetsCorrected', ROOT.kOrange+1, inputList),
               ('hltAK8PuppiV3JetsCorrected', ROOT.kRed, inputList),
             ]
          elif 'MatchedToPF_' in _hkey:
             _hkey_jmeColl = 'PF'
             _leg_jmeColl = 'HLT'
             _jmeCollList = [
               ('OfflineCorr', ROOT.kPink+1, [inputList[0]]),
               ('Calo', ROOT.kGray+1, inputList),
               ('PFCluster', ROOT.kGreen-5, inputList),
               ('PF', ROOT.kBlack, inputList),
               ('PFCHSv1', ROOT.kBlue, inputList),
               ('PFCHSv2', ROOT.kViolet, inputList),
               ('PuppiV1', ROOT.kOrange+1, inputList),
               ('PuppiV3', ROOT.kRed, inputList),
             ]
          elif 'MatchedToPFCorr_' in _hkey:
             _hkey_jmeColl = 'PFCorr'
             _leg_jmeColl = 'HLT'
             _jmeCollList = [
               ('OfflineCorr', ROOT.kPink+1, [inputList[0]]),
               ('CaloCorr', ROOT.kGray+1, inputList),
               ('PFCorr', ROOT.kBlack, inputList),
               ('PFCHSv1Corr', ROOT.kBlue, inputList),
               ('PFCHSv2Corr', ROOT.kViolet, inputList),
               ('PuppiV1Corr', ROOT.kOrange+1, inputList),
               ('PuppiV3Corr', ROOT.kRed, inputList),
             ]

       if _hkey_jmeColl is None:
          continue

       ## histograms
       _divideByBinWidth = False
       _normalizedToUnity = False

       _hists = []
       for inp in inputList:
           if _hkey not in inp['TH1s']: continue

           for (_jmeCollName, _jmeCollColor, _jmeInputFiles) in _jmeCollList:
               if inp not in _jmeInputFiles: continue

               _hkeyNew = _hkey.replace(_hkey_jmeColl, _jmeCollName)

               if _hkeyNew not in inp['TH1s']:
                  continue

               h0 = inp['TH1s'][_hkeyNew].Clone()

               if h0.InheritsFrom('TH2'):
                  continue

               h0.UseCurrentStyle()
               if hasattr(h0, 'SetDirectory'):
                  h0.SetDirectory(0)

               h0.SetLineColor(_jmeCollColor)
               h0.SetLineStyle(1 if (_hIsProfile or _hIsEfficiency) else inp['LineStyle'])
               h0.SetMarkerStyle(inp['MarkerStyle'])
               h0.SetMarkerColor(_jmeCollColor)
               h0.SetMarkerSize(inp['MarkerSize'] if (_hIsProfile or _hIsEfficiency) else 0.)

               h0.SetBit(ROOT.TH1.kNoTitle)

               if hasattr(h0, 'SetStats'):
                  h0.SetStats(0)

               if (len(_hists) == 0) and (not (_hIsProfile or _hIsEfficiency)):
                  _tmpBW = None
                  for _tmp in range(1, h0.GetNbinsX()+1):
                      if _tmpBW is None:
                         _tmpBW = h0.GetBinWidth(_tmp)
                      elif (abs(_tmpBW-h0.GetBinWidth(_tmp))/max(abs(_tmpBW), abs(h0.GetBinWidth(_tmp)))) > 1e-4:
                         _divideByBinWidth = True
                         break

               if _divideByBinWidth:
                  h0.Scale(1., 'width')

               if _normalizedToUnity:
                  h0.Scale(1. / h0.Integral())

               hist0 = Histogram()
               hist0.th1 = h0
               hist0.draw = 'ep' if (_hIsProfile or _hIsEfficiency) else 'hist,e0'
               hist0.draw += ',same'
               hist0.legendName = inp['Legend']+_jmeCollName
               hist0.legendDraw = 'ep' if (_hIsProfile or _hIsEfficiency) else 'l'
               _hists.append(hist0)

       if len(_hists) < 2:
          continue

       ## labels and axes titles
       _titleX, _titleY, _objLabel = getPlotLabels(_hkey_basename, isProfile=_hIsProfile, isEfficiency=_hIsEfficiency, useUpgradeLabels=opts.upgrade)

       _objLabel = _objLabel.replace(_hkey_jmeColl, _leg_jmeColl)

       label_obj = get_text(Lef+(1-Rig-Lef)*0.95, Bot+(1-Top-Bot)*0.925, 31, .035, _objLabel)
       _labels = [label_sample, label_obj]

       if _divideByBinWidth:
          _titleY += ' / Bin width'

       _htitle = ';'+_titleX+';'+_titleY

       _logY = ('_NotMatchedTo' in _hkey_basename) and _hkey_basename.endswith('pt_eff')

       ## plot
       plot(**{
         'histograms': _hists,
         'title': _htitle,
         'labels': _labels,
         'legXY': [Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.50, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.90],
         'outputs': [OUTDIR+'/'+_hkey+'.'+_tmp for _tmp in EXTS],
         'ratio': True,
         'logY': _logY,
         'autoRangeX': True,
       })

       del _hists
