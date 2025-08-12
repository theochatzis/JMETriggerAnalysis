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

from jmePlots_compareFiles import updateDictionary, getTH1sFromTFile, Histogram, plot

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

   parser.add_argument('-u', '--upgrade', dest='upgrade', action='store_true', default=False,
                       help='labels for Phase-2 plots')

   parser.add_argument('-l', '--label', dest='label', action='store', default='',
                       help='text label (displayed in top-left corner)')

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

       _outname = _hkey

       _hkey_basename = os.path.basename(_hkey)

       _hIsProfile = '_wrt_' in _hkey_basename

       _hIsEfficiency = _hkey_basename.endswith('_eff')

       _hkey_dqmColl, _dqmCollList = None, []

       _legXY = [Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.50, Lef+(1-Rig-Lef)*0.99, Bot+(1-Bot-Top)*0.99]

       _logY = False
       _xMin, _xMax = None, None

       if _hkey.endswith('pfcand_pt_2'):
          _logY, _xMin, _xMax = True, 0., 100.

       _skip = False
       _hkey_dirname = os.path.dirname(_hkey)
       for _pfTypeTag in ['_h', '_e', '_mu', '_gamma', '_h0']:
          if _hkey_dirname.endswith(_pfTypeTag) and _hkey_basename.startswith('pfcand_mult_') and (not _hkey_basename.endswith(_pfTypeTag)):
             _skip = True
             break
       if _skip: continue

       if opts.upgrade:
          if ('_particleFlowTmp/' in _hkey) or ('_particleFlowTmp_' in _hkey):
             _hkey_dqmColl = 'particleFlowTmp'
             _outname = _hkey.replace('_particleFlowTmp', '')
             _dqmCollList = [
               ('offlineParticleFlow', ROOT.kPink+1  , [inputList[0]]),
               ('simPFProducer'      , ROOT.kOrange+1,  inputList    ),
               ('pfTICL'             , ROOT.kBlue    ,  inputList    ),
               ('particleFlowTmp'    , ROOT.kBlack   ,  inputList    ),
#              ('hltPuppi'           , ROOT.kRed     ,  inputList    ),
             ]
             _legXY = [Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.70, Lef+(1-Rig-Lef)*0.99, Bot+(1-Bot-Top)*0.99]
       else:
          if ('_hltParticleFlow/' in _hkey) or ('_hltParticleFlow_' in _hkey):
             _hkey_dqmColl = 'hltParticleFlow'
             _outname = _hkey.replace('_hltParticleFlow', '')
             _dqmCollList = [
               ('hltParticleFlow'     , ROOT.kBlack   ,  inputList    ),
#              ('hltParticleFlowCHSv1', ROOT.kBlue    ,  inputList    ),
               ('hltParticleFlowCHSv2', ROOT.kViolet  ,  inputList    ),
#              ('hltPuppiV1'          , ROOT.kOrange+1,  inputList    ),
               ('hltPuppiV3'          , ROOT.kRed     ,  inputList    ),
               ('offlineParticleFlow' , ROOT.kPink+1  , [inputList[0]]),
             ]
          elif '_hltMergedTracks/' in _hkey:
             _hkey_dqmColl = 'hltMergedTracks'
             _outname = _hkey.replace('_hltMergedTracks', '')
             _dqmCollList = [
               ('hltIter0PFlowTrackSelectionHighPurity', ROOT.kBlack, inputList),
               ('hltMergedTracks'                      , ROOT.kRed  , inputList),
             ]
             _legXY = [Lef+(1-Rig-Lef)*0.45, Bot+(1-Bot-Top)*0.70, Lef+(1-Rig-Lef)*0.99, Bot+(1-Bot-Top)*0.99]

       if _hkey_dqmColl is None:
          continue

       ## histograms
       _divideByBinWidth = False
       _normalizedToUnity = False

       _hists = []
       for inp in inputList:
           if _hkey not in inp['TH1s']: continue

           for (_dqmCollName, _dqmCollColor, _dqmInputFiles) in _dqmCollList:
               if inp not in _dqmInputFiles: continue

               _hkeyNew = _hkey.replace(_hkey_dqmColl, _dqmCollName)

               if _hkeyNew not in inp['TH1s']:
                  continue

               h0 = inp['TH1s'][_hkeyNew].Clone()

               if h0.InheritsFrom('TH2'):
                  continue

               h0.UseCurrentStyle()
               if hasattr(h0, 'SetDirectory'):
                  h0.SetDirectory(0)

               h0.SetLineColor(_dqmCollColor)
               h0.SetLineStyle(1 if (_hIsProfile or _hIsEfficiency) else inp['LineStyle'])
               h0.SetMarkerStyle(inp['MarkerStyle'])
               h0.SetMarkerColor(_dqmCollColor)
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
               hist0.legendName = inp['Legend']+' '+_dqmCollName
               hist0.legendDraw = 'ep' if (_hIsProfile or _hIsEfficiency) else 'l'
               _hists.append(hist0)

       if len(_hists) < 2:
          continue

       ## labels and axes titles
       _titleX, _titleY, _objLabel = _hkey_basename, 'Entries', ''

       _objLabel = _objLabel.replace(_hkey_dqmColl, '')

       label_obj = get_text(Lef+(1-Rig-Lef)*0.95, Bot+(1-Top-Bot)*0.925, 31, .035, _objLabel)
       _labels = [label_sample, label_obj]

       if _divideByBinWidth:
          _titleY += ' / Bin width'

       _htitle = ';'+_titleX+';'+_titleY

       ## plot
       plot(**{
         'histograms': _hists,
         'title': _htitle,
         'labels': _labels,
         'legXY': _legXY,
         'outputs': [OUTDIR+'/'+_outname+'.'+_tmp for _tmp in EXTS],
         'ratio': True,
         'logY': _logY,
         'xMin': _xMin,
         'xMax': _xMax,
         'autoRangeX': True,
       })

       del _hists
