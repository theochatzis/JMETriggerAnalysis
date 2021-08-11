#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import fnmatch
import ROOT

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

def updateDictionary(dictionary, TDirectory, prefix='', keywords=[], verbose=False):

    key_prefix = ''
    if len(prefix) > 0: key_prefix = prefix+'/'

    for j_key in TDirectory.GetListOfKeys():

        j_key_name = j_key.GetName()

        j_obj = TDirectory.Get(j_key_name)

        if j_obj.InheritsFrom('TDirectory'):

           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name, keywords=keywords, verbose=verbose)

        elif j_obj.InheritsFrom('TH1') or j_obj.InheritsFrom('TGraph'):

           out_key = key_prefix+j_key_name

           if keywords:
              skip = True
              for _keyw in keywords:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip = False
                     break
              if skip: continue

           if out_key in dictionary:
              KILL(log_prx+'input error -> found duplicate of template ["'+out_key+'"] in input file: '+TDirectory.GetName())

           dictionary[out_key] = j_obj.Clone()
           if hasattr(dictionary[out_key], 'SetDirectory'):
              dictionary[out_key].SetDirectory(0)

           if verbose:
              print(colored_text('[input]', ['1','92']), out_key)

    return dictionary

def getTH1sFromTFile(path, keywords, verbose=False):

    input_histos_dict = {}

    i_inptfile = ROOT.TFile.Open(path)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return input_histos_dict

    updateDictionary(input_histos_dict, i_inptfile, prefix='', keywords=keywords, verbose=verbose)

    i_inptfile.Close()

    return input_histos_dict

class Histogram:
    def __init__(self):
        self.th1 = None
        self.draw = ''
        self.legendName = ''
        self.legendDraw = ''

def plot(histograms, outputs, title, labels, legXY=[], ratio=False, ratioPadFrac=0.3, xMin=None, xMax=None, yMin=None, yMax=None, logX=False, logY=False, autoRangeX=False):

    xyMinMax = []
    if histograms[0].th1.InheritsFrom('TGraph'):
       xyMinMax = get_xyminmax_from_graph(histograms[0].th1)

    nvalid_histograms = len(histograms)

    canvas = ROOT.TCanvas()
    canvas.SetGrid(1,1)
    canvas.SetTickx()
    canvas.SetTicky()

    Top = canvas.GetTopMargin()
    Rig = canvas.GetRightMargin()
    Bot = canvas.GetBottomMargin()
    Lef = canvas.GetLeftMargin()

    leg = None
    if len(legXY) == 4:
       leg = ROOT.TLegend(legXY[0], legXY[1], legXY[2], legXY[3])
       leg.SetBorderSize(2)
       leg.SetTextFont(42)
       leg.SetFillColor(0)
       for _tmp in histograms:
           if _tmp.th1 is not None:
              if (_tmp.th1.InheritsFrom('TH1') and _tmp.th1.GetEntries()) or (_tmp.th1.InheritsFrom('TGraph') and _tmp.th1.GetN()):
                 leg.AddEntry(_tmp.th1, _tmp.legendName, _tmp.legendDraw)

    if autoRangeX:
       xMinCalc, xMaxCalc = None, None
       for _tmp in histograms:
           if (_tmp.th1 is not None):
              if hasattr(_tmp.th1, 'GetNbinsX'):
                 tmpXMin, tmpXMax = _tmp.th1.GetBinLowEdge(1), _tmp.th1.GetBinLowEdge(1+_tmp.th1.GetNbinsX())
                 if _tmp.th1.Integral() > 0.:
                    for i_bin in range(1, _tmp.th1.GetNbinsX()+1):
                        if (_tmp.th1.GetBinContent(i_bin) != 0.) or (_tmp.th1.GetBinError(i_bin) != 0.): break
                        tmpXMin = _tmp.th1.GetBinLowEdge(i_bin)
                    for i_bin in reversed(range(1, _tmp.th1.GetNbinsX()+1)):
                        if (_tmp.th1.GetBinContent(i_bin) != 0.) or (_tmp.th1.GetBinError(i_bin) != 0.): break
                        tmpXMax = _tmp.th1.GetBinLowEdge(i_bin)
                 xMinCalc = min(xMinCalc, tmpXMin) if xMinCalc is not None else tmpXMin
                 xMaxCalc = max(xMaxCalc, tmpXMax) if xMaxCalc is not None else tmpXMax
              else:
                 _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1)
                 xMinCalc = min(xMinCalc, _tmp_xyMinMax[0]) if xMinCalc is not None else _tmp_xyMinMax[0]
                 xMaxCalc = max(xMaxCalc, _tmp_xyMinMax[2]) if xMaxCalc is not None else _tmp_xyMinMax[2]
    else:
       xMinCalc = xyMinMax[0] if xyMinMax else histograms[0].th1.GetBinLowEdge(1)
       xMaxCalc = xyMinMax[2] if xyMinMax else histograms[0].th1.GetBinLowEdge(1+histograms[0].th1.GetNbinsX())

    XMIN = xMinCalc if xMin is None else (max(xMin, xMinCalc) if autoRangeX else xMin)
    XMAX = xMaxCalc if xMax is None else (min(xMax, xMaxCalc) if autoRangeX else xMax)

    HMIN, HMAX = 1e8, -1e8
    for _tmp in histograms:
        if (_tmp.th1 is not None):
           if hasattr(_tmp.th1, 'GetNbinsX'):
              for i_bin in range(1, _tmp.th1.GetNbinsX()+1):
                  HMAX = max(HMAX, (_tmp.th1.GetBinContent(i_bin) + _tmp.th1.GetBinError(i_bin)))
           else:
              _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1)
              HMIN = min(HMIN, _tmp_xyMinMax[1])
              HMAX = max(HMAX, _tmp_xyMinMax[3])

    YMIN, YMAX = yMin, yMax
    if YMIN is None: YMIN = .0003 if logY else .0001
    if YMAX is None: YMAX = .0003*((HMAX/.0003)**(1./.85)) if logY else .0001+((HMAX-.0001) *(1./.85))

    canvas.cd()

    if not ratio:

       h0 = canvas.DrawFrame(XMIN, YMIN, XMAX, YMAX)

       canvas.SetTickx()
       canvas.SetTicky()

       canvas.SetLogx(logX)
       canvas.SetLogy(logY)

       for _tmp in histograms:
           if _tmp.th1 is not None:
              _tmp.th1.Draw(_tmp.draw)

       h0.Draw('axis,same')
       h0.SetTitle(title)
#       h0.GetXaxis().SetRangeUser(XMIN, XMAX)
#       h0.GetYaxis().SetRangeUser(YMIN, YMAX)

       if leg: leg.Draw('same')

       for _tmp in labels:
           if hasattr(_tmp, 'Draw'):
              _tmp.Draw('same')

    else:

       pad1H = max(0.01, 1.-ratioPadFrac)

       pad1 = ROOT.TPad('pad1', 'pad1', 0, 1-pad1H, 1, 1)

       pad1.SetTopMargin(pad1.GetTopMargin()/pad1H)
       pad1.SetBottomMargin(0.02)
       pad1.SetGrid(1,1)
       pad1.SetTickx()
       pad1.SetTicky()
       pad1.SetLogx(logX)
       pad1.SetLogy(logY)
       pad1.Draw()

       ROOT.SetOwnership(pad1, False)

       pad1.cd()

       h0 = pad1.DrawFrame(XMIN, YMIN, XMAX, YMAX)

       h11 = None
       for _tmp in histograms:
           if _tmp.th1 is not None:
              if h11 is None: h11 = _tmp.th1
              _tmp.th1.Draw(_tmp.draw)

       if not h11: return 1

       h0.Draw('axis,same')
       h0.GetXaxis().SetTitle('')
       h0.GetYaxis().SetTitle(title.split(';')[2])
       h0.GetXaxis().SetRangeUser(XMIN, XMAX)

       h0.GetYaxis().SetTitleSize(h0.GetYaxis().GetTitleSize()/pad1H)
       h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset()*pad1H)
       h0.GetXaxis().SetLabelSize(0)
       h0.GetYaxis().SetLabelSize(h0.GetYaxis().GetLabelSize()/pad1H)
       h0.GetXaxis().SetTickLength(h0.GetXaxis().GetTickLength()/pad1H)

       if YMIN is None: YMIN = .0003 if logY else .0001
       if YMAX is None: YMAX = .0003*((HMAX/.0003)**(1./.85)) if logY else .0001+((HMAX-.0001)*(1./.85))

       h0.GetYaxis().SetRangeUser(YMIN, YMAX)

       if leg:
          leg.Draw('same')
          pad1.Update()
          leg.SetY1NDC(1.-(1.-leg.GetY1NDC())/pad1H)
          leg.SetY2NDC(1.-(1.-leg.GetY2NDC())/pad1H)

       labels2 = []
       for _tmp in labels:
           if hasattr(_tmp, 'Clone'):
              _tmp2 = _tmp.Clone()
              labels2 += [_tmp2]

       for _tmp in labels2:
           _tmp.Draw('same')
           pad1.Update()
           _tmp.SetTextSize(_tmp.GetTextSize()/pad1H)
           _tmp.SetY(1.-(1.-_tmp.GetY())/pad1H)

       pad1.Update()

       canvas.cd()

       pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, 1-pad1H)
       pad2.SetTopMargin(0)
       pad2.SetBottomMargin(pad2.GetBottomMargin()/(1-pad1H))
       pad2.SetGrid(1,1)
       pad2.SetLogx(logX)
       pad2.SetTickx()
       pad2.SetTicky()
       pad2.Draw()

       denom = h11.Clone()
       if hasattr(denom, 'GetNbinsX'):
          for _tmp in range(0, denom.GetNbinsX()+2): denom.SetBinError(_tmp, 0.)
       else:
          for _tmp in range(denom.GetN()):
              denom.SetPointEYhigh(_tmp, 0.)
              denom.SetPointEYlow(_tmp, 0.)

       plot_ratios = []

       for _tmp in histograms:
           histo = Histogram()
           if _tmp.th1 is not None:
              histo.th1 = _tmp.th1.Clone()
              if histo.th1.InheritsFrom('TH1'):
                 histo.th1.Divide(denom)
              else:
                 histo.th1 = get_ratio_graph(histo.th1, denom)

           histo.draw = _tmp.draw
           if _tmp.th1.InheritsFrom('TH1') and ('same' not in histo.draw):
              histo.draw += ',same'

           histo.legendName = _tmp.legendName
           histo.legendDraw = _tmp.legendDraw

           if hasattr(histo.th1, 'SetStats'):
              histo.th1.SetStats(0)

           plot_ratios += [histo]

       ROOT.SetOwnership(pad2, False)

       pad2.cd()

       h21 = pad2.DrawFrame(XMIN, 0., XMAX, 2.)

       h21.SetFillStyle(3017)
       h21.SetFillColor(16)

       h21.GetXaxis().SetTitle(title.split(';')[1])
       h21.GetYaxis().SetTitle('Ratio')
       h21.GetYaxis().CenterTitle()
       h21.GetXaxis().SetTitleSize(h21.GetXaxis().GetTitleSize()/(1-pad1H))
       h21.GetYaxis().SetTitleSize(h21.GetYaxis().GetTitleSize()/(1-pad1H))
       h21.GetXaxis().SetTitleOffset(h21.GetXaxis().GetTitleOffset())
       h21.GetYaxis().SetTitleOffset(h21.GetYaxis().GetTitleOffset()*(1-pad1H))
       h21.GetXaxis().SetLabelSize(h21.GetYaxis().GetLabelSize()/(1-pad1H))
       h21.GetYaxis().SetLabelSize(h21.GetYaxis().GetLabelSize()/(1-pad1H))
       h21.GetXaxis().SetTickLength(h21.GetXaxis().GetTickLength()/(1-pad1H))
       h21.GetXaxis().SetLabelOffset(h21.GetXaxis().GetLabelOffset()/(1-pad1H))
       h21.GetYaxis().SetNdivisions(404)

       h21.GetXaxis().SetRangeUser(XMIN, XMAX)

       h2max, h2min = None, None
       for _tmp in plot_ratios:
           if _tmp.th1 is None: continue
           if hasattr(_tmp.th1, 'GetNbinsX'):
              for _tmpb in range(1, _tmp.th1.GetNbinsX()+1):
                  if (abs(_tmp.th1.GetBinContent(_tmpb)) > 1e-7) and (abs(_tmp.th1.GetBinError(_tmpb)) > 1e-7):
                     h2max = max(h2max, _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)) if (h2max is not None) else _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)
                     h2min = min(h2min, _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)) if (h2min is not None) else _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)
           else:
              _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1)
              h2min = min(h2min, _tmp_xyMinMax[1]) if (h2min is not None) else _tmp_xyMinMax[1]
              h2max = max(h2max, _tmp_xyMinMax[3]) if (h2max is not None) else _tmp_xyMinMax[3]

       if (h2max is not None) and (h2min is not None):
          h2min = min(int(h2min*105.)/100., int(h2min*95.)/100.)
          h2max = max(int(h2max*105.)/100., int(h2max*95.)/100.)

          h2min = max(h2min, -5)
          h2max = min(h2max, 5)

          h21.GetYaxis().SetRangeUser(h2min, h2max)

#       h21.Draw('e2')
       for _tmp in plot_ratios:
           if _tmp.th1 is not None:
              _tmp.th1.Draw(_tmp.draw)
       h21.Draw('axis,same')

    canvas.cd()
    canvas.Update()

    for output_file in outputs:
        output_dirname = os.path.dirname(output_file)
        if not os.path.isdir(output_dirname):
           EXE('mkdir -p '+output_dirname)

        canvas.SetName(os.path.splitext(output_file)[0])
        canvas.SaveAs(output_file)

        print(colored_text('[output]', ['1', '92']), os.path.relpath(output_file))

    canvas.Close()

    if ratio:
       del plot_ratios
       del denom

    return 0

def getPlotLabels(key, isProfile, isEfficiency, useUpgradeLabels):

    _objLabel = ''
    if   key.startswith('ak4GenJets_'):                _objLabel = 'AK4GenJets'
    elif key.startswith('hltAK4CaloJets_'):            _objLabel = 'HLT AK4CaloJets'
    elif key.startswith('hltAK4CaloJetsCorrected_'):   _objLabel = 'HLT AK4CaloJetsCorrected'
    elif key.startswith('hltAK4PFJets_'):              _objLabel = 'HLT AK4PFJets'
    elif key.startswith('hltAK4PFJetsCorrected_'):     _objLabel = 'HLT AK4PFJetsCorrected'
    elif key.startswith('hltAK4PFCHSJets_'):           _objLabel = 'HLT AK4PFCHSJets'
    elif key.startswith('hltAK4PFCHSJetsCorrected_'):  _objLabel = 'HLT AK4PFCHSJetsCorrected'
    elif key.startswith('hltAK4PFCHSv1Jets_'):         _objLabel = 'HLT AK4PFCHSv1Jets'
    elif key.startswith('hltAK4PFCHSv1JetsCorrected_'):_objLabel = 'HLT AK4PFCHSv1JetsCorrected'
    elif key.startswith('hltAK4PFCHSv2Jets_'):         _objLabel = 'HLT AK4PFCHSv2Jets'
    elif key.startswith('hltAK4PFCHSv2JetsCorrected_'):_objLabel = 'HLT AK4PFCHSv2JetsCorrected'
    elif key.startswith('hltAK4PuppiJets_'):           _objLabel = 'HLT AK4PuppiJets'
    elif key.startswith('hltAK4PuppiJetsCorrected_'):  _objLabel = 'HLT AK4PuppiJetsCorrected'
    elif key.startswith('hltAK4PuppiV1Jets_'):         _objLabel = 'HLT AK4PuppiV1Jets'
    elif key.startswith('hltAK4PuppiV3Jets_'):         _objLabel = 'HLT AK4PuppiV3Jets'
    elif key.startswith('ak8GenJets_'):                _objLabel = 'AK8GenJets'
    elif key.startswith('hltAK8CaloJets_'):            _objLabel = 'HLT AK8CaloJets'
    elif key.startswith('hltAK8CaloJetsCorrected_'):   _objLabel = 'HLT AK8CaloJetsCorrected'
    elif key.startswith('hltAK8PFJets_'):              _objLabel = 'HLT AK8PFJets'
    elif key.startswith('hltAK8PFJetsCorrected_'):     _objLabel = 'HLT AK8PFJetsCorrected'
    elif key.startswith('hltAK8PFCHSJets_'):           _objLabel = 'HLT AK8PFCHSJets'
    elif key.startswith('hltAK8PFCHSJetsCorrected_'):  _objLabel = 'HLT AK8PFCHSJetsCorrected'
    elif key.startswith('hltAK8PuppiJets_'):           _objLabel = 'HLT AK8PuppiJets'
    elif key.startswith('hltAK8PuppiJetsCorrected_'):  _objLabel = 'HLT AK8PuppiJetsCorrected'
    elif key.startswith('hltCaloMET_'):                _objLabel = 'HLT CaloMET'
    elif key.startswith('hltPFMET_'):                  _objLabel = 'HLT PFMET'
    elif key.startswith('hltPFMETNoMu_'):              _objLabel = 'HLT PFMETNoMu'
    elif key.startswith('hltPFMETTypeOne_'):           _objLabel = 'HLT PFMET Type-1'
    elif key.startswith('hltPuppiMET_'):               _objLabel = 'HLT PuppiMET'
    elif key.startswith('hltPuppiMETNoMu_'):           _objLabel = 'HLT PuppiMETNoMu'
    elif key.startswith('hltPuppiV1MET_'):             _objLabel = 'HLT PuppiV1MET'
    elif key.startswith('hltPuppiV1METNoMu_'):         _objLabel = 'HLT PuppiV1METNoMu'
    elif key.startswith('hltPuppiV2MET_'):             _objLabel = 'HLT PuppiV2MET'
    elif key.startswith('hltPuppiV2METNoMu_'):         _objLabel = 'HLT PuppiV2METNoMu'
    elif key.startswith('hltPuppiV3MET_'):             _objLabel = 'HLT PuppiV3MET'
    elif key.startswith('hltPuppiV3METNoMu_'):         _objLabel = 'HLT PuppiV3METNoMu'
    elif key.startswith('hltPuppiV4MET_'):             _objLabel = 'HLT PuppiV4MET'
    elif key.startswith('hltPuppiV4METNoMu_'):         _objLabel = 'HLT PuppiV4METNoMu'
    elif key.startswith('hltPFMETCHS_'):               _objLabel = 'HLT PF+CHS MET'
    elif key.startswith('hltPFMETSoftKiller_'):        _objLabel = 'HLT PF+SoftKiller MET'
    elif key.startswith('hltPFCHSv2MET_'):             _objLabel = 'HLT PF+CHSv1 MET'
    elif key.startswith('hltPFCHSv2MET_'):             _objLabel = 'HLT PF+CHSv2 MET'

    if   '_EtaIncl_' in key: pass
    elif '_HB_'      in key: _objLabel += ', |#eta|<'+('1.5' if useUpgradeLabels else '1.3')
    elif '_HGCal_'   in key: _objLabel += ', 1.5<|#eta|<3.0'
    elif '_HE_'      in key: _objLabel += ', 1.3<|#eta|<3.0'
    elif '_HE1_'     in key: _objLabel += ', 1.3<|#eta|<2.5'
    elif '_HE2_'     in key: _objLabel += ', 2.5<|#eta|<3.0'
    elif '_HF_'      in key: _objLabel += ', 3.0<|#eta|<5.0'
    elif '_HF1_'     in key: _objLabel += ', 3.0<|#eta|<4.0'
    elif '_HF2_'     in key: _objLabel += ', 4.0<|#eta|<5.0'

    if   '_NotMatchedToGEN'     in key: _objLabel += ' [Not Matched to GEN]'
    elif '_NotMatchedToOffline' in key: _objLabel += ' [Not Matched to Offline]'
    elif '_NotMatchedToCalo'    in key: _objLabel += ' [Not Matched to Calo]'
    elif '_NotMatchedToPF'      in key: _objLabel += ' [Not Matched to PF]'
    elif '_NotMatchedToPFCHS'   in key: _objLabel += ' [Not Matched to PFCHS]'
    elif '_NotMatchedToPuppi'   in key: _objLabel += ' [Not Matched to Puppi]'
    elif '_MatchedToGEN'        in key: _objLabel += ' [Matched to GEN]'
    elif '_MatchedToOffline'    in key: _objLabel += ' [Matched to Offline]'
    elif '_MatchedToCalo'       in key: _objLabel += ' [Matched to Calo]'
    elif '_MatchedToPF'         in key: _objLabel += ' [Matched to PF]'
    elif '_MatchedToPFCHS'      in key: _objLabel += ' [Matched to PFCHS]'
    elif '_MatchedToPuppi'      in key: _objLabel += ' [Matched to Puppi]'

    ## axes' titles
    _titleX, _titleY = key, ''
    if isProfile:
       if 'Jets' in key:
          if key.endswith('_pt'): _titleX = 'Jet p_{T} [GeV]'
          elif key.endswith('_eta'): _titleX = 'Jet #eta'
          elif key.endswith('_phi'): _titleX = 'Jet #phi'
          elif key.endswith('_mass'): _titleX = 'Jet mass [GeV]'
       elif 'MET' in key:
          if key.endswith('_pt'): _titleX = 'MET [GeV]'
          elif key.endswith('_phi'): _titleX = 'MET #phi'
          elif key.endswith('_sumEt'): _titleX = 'MET Sum-E_{T} [GeV]'
       if ('_GEN_' in key) or ('GenJets' in key):
          _titleX = 'GEN '+_titleX
       elif '_Offline_' in key:
          _titleX = 'Offline '+_titleX
    elif isEfficiency:
       if 'Jets' in key:
          if key.endswith('_pt_eff'): _titleX = 'Jet p_{T} [GeV]'
          elif key.endswith('_eta_eff'): _titleX = 'Jet #eta'
          elif key.endswith('_phi_eff'): _titleX = 'Jet #phi'
          elif key.endswith('_mass_eff'): _titleX = 'Jet mass [GeV]'
       elif 'MET' in key:
          if key.endswith('_pt_eff'): _titleX = 'MET [GeV]'
          elif key.endswith('_phi_eff'): _titleX = 'MET #phi'
          elif key.endswith('_sumEt_eff'): _titleX = 'MET Sum-E_{T} [GeV]'
       if ('_GEN_' in key) or ('GenJets' in key):
          _titleX = 'GEN '+_titleX
       elif '_Offline_' in key:
          _titleX = 'Offline '+_titleX
    else:
       if 'MET' in key:
          _titleY = 'Events'
       elif 'Jets' in key:
          if '_njets' in key:
             _titleY = 'Events'
          else:
             _titleY = 'Entries'

    if isEfficiency:
       _titleY = 'Efficiency'

    if   '_pt_overGEN_Mean_' in key: _titleY = '#LTp_{T} / p_{T}^{GEN}#GT'
    elif '_pt_overGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T} / p_{T}^{GEN}) / #LTp_{T} / p_{T}^{GEN}#GT'
    elif '_pt_overGEN_RMS_' in key: _titleY = '#sigma(p_{T} / p_{T}^{GEN})'
    elif '_pt_overGEN' in key: _titleX = 'p_{T} / p_{T}^{GEN}'

    elif '_pt_overOffline_Mean_' in key: _titleY = '#LTp_{T} / p_{T}^{Offl}#GT'
    elif '_pt_overOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T} / p_{T}^{Offl}) / #LTp_{T} / p_{T}^{Offl}#GT'
    elif '_pt_overOffline_RMS_' in key: _titleY = '#sigma(p_{T} / p_{T}^{Offl})'
    elif '_pt_overOffline' in key: _titleX = 'p_{T} / p_{T}^{Offl}'

    elif '_mass_overGEN_Mean_' in key: _titleY = '#LTmass / mass^{GEN}#GT'
    elif '_mass_overGEN_RMSOverMean_' in key: _titleY = '#sigma(m / m^{GEN}) / #LTm / m^{GEN}#GT'
    elif '_mass_overGEN_RMS_' in key: _titleY = '#sigma(mass / mass^{GEN})'
    elif '_mass_overGEN' in key: _titleX = 'mass / mass^{GEN}'

    elif '_mass_overOffline_Mean_' in key: _titleY = '#LTmass / mass^{Offl}#GT'
    elif '_mass_overOffline_RMSOverMean_' in key: _titleY = '#sigma(m / m^{Offl}) / #LTm / m^{Offl}#GT'
    elif '_mass_overOffline_RMS_' in key: _titleY = '#sigma(mass / mass^{Offl})'
    elif '_mass_overOffline' in key: _titleX = 'mass / mass^{Offl}'

    elif '_sumEt_overGEN_Mean_' in key: _titleY = '#LTSum-E_{T} / Sum-E_{T}^{GEN}#GT'
    elif '_sumEt_overGEN_RMSOverMean_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{GEN}) / #LTSum-E_{T} / Sum-E_{T}^{GEN}#GT'
    elif '_sumEt_overGEN_RMS_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{GEN})'
    elif '_sumEt_overGEN' in key: _titleX = 'Sum-E_{T} / Sum-E_{T}^{GEN}'

    elif '_sumEt_overOffline_Mean_' in key: _titleY = '#LTSum-E_{T} / Sum-E_{T}^{Offl}#GT'
    elif '_sumEt_overOffline_RMSOverMean_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{Offl}) / #LTSum-E_{T} / Sum-E_{T}^{Offl}#GT'
    elif '_sumEt_overOffline_RMS_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{Offl})'
    elif '_sumEt_overOffline' in key: _titleX = 'Sum-E_{T} / Sum-E_{T}^{Offl}'

    elif '_deltaPhiGEN_Mean_' in key: _titleY = '#LT#Delta#phi^{GEN}#GT'
#    elif '_deltaPhiGEN_RMSOverMean_' in key: _titleY = '#sigma(#Delta#phi^{GEN}) / #LT#Delta#phi^{GEN}#GT'
    elif '_deltaPhiGEN_RMS_' in key: _titleY = '#sigma(#Delta#phi^{GEN})'
    elif '_deltaPhiGEN' in key: _titleX = '#Delta#phi^{GEN}'

    elif '_deltaPhiOffline_Mean_' in key: _titleY = '#LT#Delta#phi^{Offl}#GT'
#    elif '_deltaPhiOffline_RMSOverMean_' in key: _titleY = '#sigma(#Delta#phi^{Offl}) / #LT#Delta#phi^{Offl}#GT'
    elif '_deltaPhiOffline_RMS_' in key: _titleY = '#sigma(#Delta#phi^{Offl})'
    elif '_deltaPhiOffline' in key: _titleX = '#Delta#phi^{Offl}'

    elif '_pt_paraToGEN_Mean_' in key: _titleY = '#LTp_{T}^{#parallel GEN}#GT [GeV]'
    elif '_pt_paraToGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN}) / #LTp_{T} / p_{T}^{GEN}#GT [GeV]'
    elif '_pt_paraToGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN}) [GeV]'
    elif '_pt_paraToGEN' in key: _titleX = 'p_{T}^{#parallel GEN} [GeV]'

    elif '_pt_paraToOffline_Mean_' in key: _titleY = '#LTp_{T}^{#parallel Offl}#GT [GeV]'
    elif '_pt_paraToOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
    elif '_pt_paraToOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl}) [GeV]'
    elif '_pt_paraToOffline' in key: _titleX = 'p_{T}^{#parallel Offl} [GeV]'

    elif '_pt_paraToGENMinusGEN_Mean_' in key: _titleY = '#LTp_{T}^{#parallel GEN} - p_{T}^{GEN}#GT [GeV]'
    elif '_pt_paraToGENMinusGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN} - p_{T}^{GEN}) / #LTp_{T} / p_{T}^{GEN}#GT [GeV]'
    elif '_pt_paraToGENMinusGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN} - p_{T}^{GEN}) [GeV]'
    elif '_pt_paraToGENMinusGEN' in key: _titleX = 'p_{T}^{#parallel GEN} - p_{T}^{GEN} [GeV]'

    elif '_pt_paraToOfflineMinusOffline_Mean_' in key: _titleY = '#LTp_{T}^{#parallel Offl} - p_{T}^{Offl}#GT [GeV]'
    elif '_pt_paraToOfflineMinusOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl} - p_{T}^{Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
    elif '_pt_paraToOfflineMinusOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl} - p_{T}^{Offl}) [GeV]'
    elif '_pt_paraToOfflineMinusOffline' in key: _titleX = 'p_{T}^{#parallel Offl} - p_{T}^{Offl} [GeV]'

    elif '_pt_perpToGEN_Mean_' in key: _titleY = '#LTp_{T}^{#perp GEN}#GT [GeV]'
    elif '_pt_perpToGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#perp GEN}) / #LTp_{T} / p_{T}^{GEN}#GT [GeV]'
    elif '_pt_perpToGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#perp GEN}) [GeV]'
    elif '_pt_perpToGEN' in key: _titleX = 'p_{T}^{#perp GEN} [GeV]'

    elif '_pt_perpToOffline_Mean_' in key: _titleY = '#LTp_{T}^{#perp Offl}#GT [GeV]'
    elif '_pt_perpToOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#perp Offl}) / #LTp_{T} / p_{T}^{Offl}#GT [GeV]'
    elif '_pt_perpToOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#perp Offl}) [GeV]'
    elif '_pt_perpToOffline' in key: _titleX = 'p_{T}^{#perp Offl} [GeV]'

    elif key.endswith('_pt0'): _titleX = 'p_{T}-Leading Jet p_{T} [GeV]'
    elif key.endswith('_pt'): _titleX = 'MET [GeV]' if 'MET' in key else 'Jet p_{T} [GeV]'
    elif key.endswith('_eta'): _titleX = 'Jet #eta'
    elif key.endswith('_phi'): _titleX = 'MET #phi' if 'MET' in key else 'Jet #phi'
    elif key.endswith('_sumEt'): _titleX = 'Sum-E_{T} [GeV]'
    elif key.endswith('_mass'): _titleX = 'Jet mass [GeV]'
    elif key.endswith('_dRmatch'): _titleX = '#DeltaR'
    elif key.endswith('_numberOfDaughters'): _titleX = 'Number of jet constituents'
    elif key.endswith('_njets'): _titleX = 'Number of jets'
    elif key.endswith('_chargedHadronEnergyFraction'): _titleX = 'Charged-Hadron Energy Fraction'
    elif key.endswith('_chargedHadronMultiplicity'): _titleX = 'Charged-Hadron Multiplicity'
    elif key.endswith('_neutralHadronEnergyFraction'): _titleX = 'Neutral-Hadron Energy Fraction'
    elif key.endswith('_neutralHadronMultiplicity'): _titleX = 'Neutral-Hadron Multiplicity'
    elif key.endswith('_electronEnergyFraction'): _titleX = 'Electron Energy Fraction'
    elif key.endswith('_electronMultiplicity'): _titleX = 'Electron Multiplicity'
    elif key.endswith('_photonEnergyFraction'): _titleX = 'Photon Energy Fraction'
    elif key.endswith('_photonMultiplicity'): _titleX = 'Photon Multiplicity'
    elif key.endswith('_muonEnergyFraction'): _titleX = 'Muon Energy Fraction'
    elif key.endswith('_muonMultiplicity'): _titleX = 'Muon Multiplicity'

    return _titleX, _titleY, _objLabel

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

       if ('_wrt_' not in _hkey_basename) and (not _hkey_basename.endswith('_eff')) and (not ('MET' in _hkey_basename and _hkey_basename.endswith('_pt'))):
          continue

       if ('/' in _hkey) and (not _hkey.startswith('NoSelection/')):
          if ('_pt0' not in _hkey_basename) or _hkey_basename.endswith('pt0_eff') or _hkey_basename.endswith('pt0') or ('pt0_over' in _hkey_basename):
             continue

       _hIsProfile = '_wrt_' in _hkey_basename

       _hIsEfficiency = _hkey_basename.endswith('_eff')

       ## histograms
       _divideByBinWidth = False
       _normalizedToUnity = False

       _hists = []
       for inp in inputList:
           if _hkey not in inp['TH1s']: continue

           h0 = inp['TH1s'][_hkey].Clone()

           if h0.InheritsFrom('TH2'):
              continue

           h0.UseCurrentStyle()
           if hasattr(h0, 'SetDirectory'):
              h0.SetDirectory(0)

           h0.SetLineColor(inp['LineColor'])
           h0.SetLineStyle(1 if (_hIsProfile or _hIsEfficiency) else inp['LineStyle'])
           h0.SetMarkerStyle(inp['MarkerStyle'])
           h0.SetMarkerColor(inp['MarkerColor'])
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
           hist0.draw = 'ep,same' if (_hIsProfile or _hIsEfficiency) else 'hist,e0,same'
           hist0.legendName = inp['Legend']
           hist0.legendDraw = 'ep' if (_hIsProfile or _hIsEfficiency) else 'l'
           _hists.append(hist0)

       if len(_hists) < 2:
          continue

       ## labels and axes titles
       _titleX, _titleY, _objLabel = getPlotLabels(_hkey_basename, isProfile=_hIsProfile, isEfficiency=_hIsEfficiency, useUpgradeLabels=opts.upgrade)

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
         'legXY': [Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.60, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.90],
         'outputs': [OUTDIR+'/'+_hkey+'.'+_tmp for _tmp in EXTS],
         'ratio': True,
         'logY': _logY,
         'autoRangeX': True,
       })

       del _hists
