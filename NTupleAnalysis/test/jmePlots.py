#!/usr/bin/env python3
import argparse
import os
import fnmatch
import math
import ROOT

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

def updateDictionary(dictionary, TDirectory, prefix='', matches=[], skip=[], verbose=False):

    key_prefix = prefix+'/' if (len(prefix) > 0) else ''

    for j_key in TDirectory.GetListOfKeys():

        j_key_name = j_key.GetName()

        j_obj = TDirectory.Get(j_key_name)

        if j_obj.InheritsFrom('TDirectory'):
           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name, matches=matches, skip=skip, verbose=verbose)

        elif j_obj.InheritsFrom('TH1') or j_obj.InheritsFrom('TGraph'):
           out_key = key_prefix+j_key_name

           if skip:
              skip_key = False
              for _keyw in skip:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip_key = True
                     break
              if skip_key:
                 continue

           if matches:
              skip_key = True
              for _keyw in matches:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip_key = False
                     break
              if skip_key:
                 continue

           if out_key in dictionary:
              KILL(log_prx+'input error -> found duplicate of template ["'+out_key+'"] in input file: '+TDirectory.GetName())

           dictionary[out_key] = j_obj.Clone()
           if hasattr(dictionary[out_key], 'SetDirectory'):
              dictionary[out_key].SetDirectory(0)

           if verbose:
              print (colored_text('[input]', ['1','92']), out_key)

    return dictionary

def getTH1sFromTFile(path, matches, skip, verbose=False):

    input_histos_dict = {}

    i_inptfile = ROOT.TFile.Open(path)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return input_histos_dict

    updateDictionary(input_histos_dict, i_inptfile, prefix='', matches=matches, skip=skip, verbose=verbose)

    i_inptfile.Close()

    return input_histos_dict

class Histogram:
    def __init__(self):
        self.th1 = None
        self.draw = ''
        self.Legend = ''
        self.LegendDraw = ''

def plot(histograms, outputs, title, labels, legXY=[], ratio=False, ratioPadFrac=0.3, xMin=None, xMax=None, yMin=None, yMax=None, logX=False, logY=False, autoRangeX=False, xLabelSize=None, xBinLabels=None):

    xyMinMax = []
    if histograms[0].th1.InheritsFrom('TGraph'):
       xyMinMax = get_xyminmax_from_graph(histograms[0].th1, error=False)

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
       leg.SetBorderSize(0)
       leg.SetBorderSize(0)
       leg.SetTextFont(42)
       leg.SetTextSize(0.04)
       leg.SetFillColor(0)
       leg.SetFillStyle(0)
       for _tmp in histograms:
           if _tmp.th1 is not None:
              if (_tmp.th1.InheritsFrom('TH1') and _tmp.th1.GetEntries()) or (_tmp.th1.InheritsFrom('TGraph') and _tmp.th1.GetN()):
                 leg.AddEntry(_tmp.th1, _tmp.Legend, _tmp.LegendDraw)

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
                 _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1, error=False)
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
              _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1, error=False)
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

       if xLabelSize:
          h0.GetXaxis().SetLabelSize(xLabelSize)

       if xBinLabels:
          xBinLabels = xBinLabels[int(round(XMIN)):int(round(XMAX))]
          h0.GetXaxis().Set(len(xBinLabels), XMIN, XMAX)
          for tmpIdx, tmpLab in enumerate(xBinLabels):
              h0.GetXaxis().SetBinLabel(tmpIdx+1, tmpLab)

       h0.GetXaxis().SetRangeUser(XMIN, XMAX)
       h0.GetYaxis().SetRangeUser(YMIN, YMAX)

       if leg:
          leg.Draw('same')

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

           histo.Legend = _tmp.Legend
           histo.LegendDraw = _tmp.LegendDraw

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

       if xLabelSize:
          h21.GetXaxis().SetLabelSize(xLabelSize)

       if xBinLabels:
          xBinLabels = xBinLabels[int(round(XMIN)):int(round(XMAX))]
          h21.GetXaxis().Set(len(xBinLabels), XMIN, XMAX)
          for tmpIdx, tmpLab in enumerate(xBinLabels):
              h21.GetXaxis().SetBinLabel(tmpIdx+1, tmpLab)

       h21.GetXaxis().SetRangeUser(XMIN, XMAX)

       h2max, h2min = None, None
       for _tmp in plot_ratios:
           if _tmp.th1 is None: continue
           if hasattr(_tmp.th1, 'GetNbinsX'):
              for _tmpb in range(1, _tmp.th1.GetNbinsX()+1):
                  if (abs(_tmp.th1.GetBinContent(_tmpb)) > 1e-7) and (abs(_tmp.th1.GetBinError(_tmpb)) > 1e-7) and (abs(_tmp.th1.GetBinError(_tmpb))/abs(_tmp.th1.GetBinContent(_tmpb)) < 0.10): # ignore bins where the error bar is higher than 10%.
                     h2max = max(h2max, _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)) if (h2max is not None) else _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)
                     h2min = min(h2min, _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)) if (h2min is not None) else _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)
           else:
              _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1, error=False)
              h2min = min(h2min, _tmp_xyMinMax[1]) if (h2min is not None) else _tmp_xyMinMax[1]
              h2max = max(h2max, _tmp_xyMinMax[3]) if (h2max is not None) else _tmp_xyMinMax[3]

       if (h2max is not None) and (h2min is not None):
          h2min = min(int(h2min*105.)/100., int(h2min*95.)/100.)
          h2max = max(int(h2max*105.)/100., int(h2max*95.)/100.)

          h2min = max(h2min, -5)
          h2max = min(h2max, 5)

          h21.GetYaxis().SetRangeUser(h2min, h2max)

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

        print (colored_text('[output]', ['1', '92']), os.path.relpath(output_file))

    canvas.Close()

    if ratio:
       del plot_ratios
       del denom

    return 0

def getPlotLabels(key, isProfile, isEfficiency, keyword):

    _objLabel = ''
    if   key.startswith('ak4GenJets_'):                _objLabel = 'AK4GenJets'
    elif key.startswith('ak4GenJetsNoNu_'):            _objLabel = 'AK4GenJetsNoNu'
    elif key.startswith('offlineAK4PFPuppiJetsCorrected_'):  _objLabel = 'Offline AK4PuppiJets'
    elif key.startswith('offlineAK8PFPuppiJetsCorrected_'):  _objLabel = 'Offline AK8PuppiJets'
    elif key.startswith('hltAK4CaloJets_'):            _objLabel = 'HLT AK4CaloJets'
    elif key.startswith('hltAK4CaloJetsCorrected_'):   _objLabel = 'HLT AK4CaloJetsCorrected'
    #elif key.startswith('hltAK4CaloJetsCorrected_'):   _objLabel = 'PFHC/JEC 2023'
    elif key.startswith('hltAK4PFClusterJets_'):            _objLabel = 'HLT AK4PFClusterJets'
    elif key.startswith('hltAK4PFClusterJetsCorrected_'):   _objLabel = 'HLT AK4PFClusterJetsCorrected'
    elif key.startswith('hltAK4PFJets_'):              _objLabel = 'HLT AK4PFJets'
    elif key.startswith('hltAK4PFJetsCorrected_'):     _objLabel = 'HLT AK4PFJetsCorrected'
    elif key.startswith('hltAK4PFCHSJets_'):           _objLabel = 'HLT AK4PFCHSJets'
    elif key.startswith('hltAK4PFCHSJetsCorrected_'):  _objLabel = 'HLT AK4PFCHSJetsCorrected'
    elif key.startswith('hltAK4PFCHSv1Jets_'):         _objLabel = 'HLT AK4PFCHSv1Jets'
    elif key.startswith('hltAK4PFCHSv1JetsCorrected_'):_objLabel = 'HLT AK4PFCHSv1JetsCorrected'
    elif key.startswith('hltAK4PFCHSv2Jets_'):         _objLabel = 'HLT AK4PFCHSv2Jets'
    elif key.startswith('hltAK4PFCHSv2JetsCorrected_'):_objLabel = 'HLT AK4PFCHSv2JetsCorrected'
    elif key.startswith('hltAK4PFPuppiJets_'):           _objLabel = 'HLT AK4PFPuppiJets'
    elif key.startswith('hltAK4PFPuppiJetsCorrected_'):  _objLabel = 'HLT AK4PFPuppiJetsCorrected'
    elif key.startswith('hltAK4PFPuppiV1Jets_'):         _objLabel = 'HLT AK4PFPuppiV1Jets'
    elif key.startswith('hltAK4PFPuppiV3Jets_'):         _objLabel = 'HLT AK4PFPuppiV3Jets'
    elif key.startswith('ak8GenJets_'):                _objLabel = 'AK8GenJets'
    elif key.startswith('hltAK8CaloJets_'):            _objLabel = 'HLT AK8CaloJets'
    elif key.startswith('hltAK8CaloJetsCorrected_'):   _objLabel = 'HLT AK8CaloJetsCorrected'
    elif key.startswith('hltAK8PFClusterJets_'):            _objLabel = 'HLT AK8PFClusterJets'
    elif key.startswith('hltAK8PFClusterJetsCorrected_'):   _objLabel = 'HLT AK8PFClusterJetsCorrected'
    elif key.startswith('hltAK8PFJets_'):              _objLabel = 'HLT AK8PFJets'
    elif key.startswith('hltAK8PFJetsCorrected_'):     _objLabel = 'HLT AK8PFJetsCorrected'
    elif key.startswith('hltAK8PFCHSJets_'):           _objLabel = 'HLT AK8PFCHSJets'
    elif key.startswith('hltAK8PFCHSJetsCorrected_'):  _objLabel = 'HLT AK8PFCHSJetsCorrected'
    elif key.startswith('hltAK8PFPuppiJets_'):           _objLabel = 'HLT AK8PFPuppiJets'
    elif key.startswith('hltAK8PFPuppiJetsCorrected_'):  _objLabel = 'HLT AK8PFPuppiJetsCorrected'
    elif key.startswith('hltCaloMET_'):                _objLabel = 'HLT CaloMET'
    elif key.startswith('hltCaloMETTypeOne_'):           _objLabel = 'HLT CaloMET Type-1'
    elif key.startswith('hltPFClusterMET_'):                _objLabel = 'HLT PFClusterMET'
    elif key.startswith('hltPFMET_'):                  _objLabel = 'HLT PFMET'
    elif key.startswith('hltPFMETNoMu_'):              _objLabel = 'HLT PFMETNoMu'
    elif key.startswith('hltPFMETTypeOne_'):           _objLabel = 'HLT PFMET Type-1'
    elif key.startswith('hltPFPuppiMET_'):               _objLabel = 'HLT PFPuppiMET'
    elif key.startswith('hltPFPuppiMETNoMu_'):           _objLabel = 'HLT PFPuppiMETNoMu'
    elif key.startswith('hltPFPuppiV1MET_'):             _objLabel = 'HLT PFPuppiV1MET'
    elif key.startswith('hltPFPuppiV1METNoMu_'):         _objLabel = 'HLT PFPuppiV1METNoMu'
    elif key.startswith('hltPFPuppiV2MET_'):             _objLabel = 'HLT PFPuppiV2MET'
    elif key.startswith('hltPFPuppiV2METNoMu_'):         _objLabel = 'HLT PFPuppiV2METNoMu'
    elif key.startswith('hltPFPuppiV3MET_'):             _objLabel = 'HLT PFPuppiV3MET'
    elif key.startswith('hltPFPuppiV3METNoMu_'):         _objLabel = 'HLT PFPuppiV3METNoMu'
    elif key.startswith('hltPFPuppiV4MET_'):             _objLabel = 'HLT PFPuppiV4MET'
    elif key.startswith('hltPFPuppiV4METNoMu_'):         _objLabel = 'HLT PFPuppiV4METNoMu'
    elif key.startswith('hltPFCHSMET_'):               _objLabel = 'HLT PF+CHS MET'
    elif key.startswith('hltPFCHSv1MET_'):             _objLabel = 'HLT PF+CHSv1 MET'
    elif key.startswith('hltPFCHSv2MET_'):             _objLabel = 'HLT PF+CHSv2 MET'
    elif key.startswith('hltPFSoftKillerMET_'):        _objLabel = 'HLT PF+SoftKiller MET'

    if   '_EtaIncl_' in key: pass
    elif '_Eta2p4_'  in key: _objLabel += ', |#eta|<2.4'
    elif '_Eta2p5_'  in key: _objLabel += ', |#eta|<2.5'
    elif '_HB_'      in key: _objLabel += ', |#eta|<1.3'
    elif '_HGCal_'   in key: _objLabel += ', 1.5<|#eta|<3.0'
    elif '_HE_'      in key: _objLabel += ', 1.3<|#eta|<3.0'
    elif '_HE1_'     in key: _objLabel += ', 1.3<|#eta|<2.5'
    elif '_HE2_'     in key: _objLabel += ', 2.5<|#eta|<3.0'
    elif '_HF_'      in key: _objLabel += ', 3.0<|#eta|<5.0'
    elif '_HF1_'     in key: _objLabel += ', 3.0<|#eta|<4.0'
    elif '_HF2_'     in key: _objLabel += ', 4.0<|#eta|<5.0'
    elif '_HE21_'     in key: _objLabel += ', 2.5<|#eta|<2.7'
    elif '_HE22_'     in key: _objLabel += ', 2.7<|#eta|<3.0'
    elif '_BPix_'     in key: _objLabel += ', BPix'
    elif '_BPix_plus4_'     in key: _objLabel += ', BPix plus'
    elif '_BPix_minus4_'     in key: _objLabel += ', BPix minus'
    elif '_BPix_plus8_'     in key: _objLabel += ', BPix plus'
    elif '_BPix_minus8_'     in key: _objLabel += ', BPix minus'
    elif '_BPixVeto_'     in key: _objLabel += ', Barrel NoBPix region'
    
    if   'Pt0_'   in key: _objLabel += ', 30<p_{T}<60'
    elif 'Pt1_'   in key: _objLabel += ', 60<p_{T}<80'
    elif 'Pt2_'   in key: _objLabel += ', 80<p_{T}<130'
    elif 'Pt3_'   in key: _objLabel += ', p_{T}>130'
    
    if   '_NotMatchedToGEN'             in key: _objLabel += ' [Not Matched to GEN]'
    elif '_NotMatchedTohltCalo'         in key: _objLabel += ' [Not Matched to Calo]'
    elif '_NotMatchedTohltCaloCorr'     in key: _objLabel += ' [Not Matched to CaloCorr]'
    elif '_NotMatchedTohltPF'           in key: _objLabel += ' [Not Matched to PF]'
    elif '_NotMatchedTohltPFCorr'       in key: _objLabel += ' [Not Matched to PFCorr]'
    elif '_NotMatchedTohltPFCHS'        in key: _objLabel += ' [Not Matched to PFCHS]'
    elif '_NotMatchedTohltPFCHSCorr'    in key: _objLabel += ' [Not Matched to PFCHSCorr]'
    elif '_NotMatchedTohltPFPuppi'      in key: _objLabel += ' [Not Matched to PFPuppi]'
    elif '_NotMatchedTohltPFPuppiCorr'  in key: _objLabel += ' [Not Matched to PFPuppiCorr]'
    elif '_NotMatchedToofflPFPuppiCorr' in key: _objLabel += ' [Not Matched to Offline]'

    elif '_MatchedToGEN'             in key: _objLabel += ' [Matched to GEN]'
    elif '_MatchedTohltCalo'         in key: _objLabel += ' [Matched to Calo]'
    elif '_MatchedTohltCaloCorr'     in key: _objLabel += ' [Matched to CaloCorr]'
    elif '_MatchedTohltPF'           in key: _objLabel += ' [Matched to PF]'
    elif '_MatchedTohltPFCorr'       in key: _objLabel += ' [Matched to PFCorr]'
    elif '_MatchedTohltPFCHS'        in key: _objLabel += ' [Matched to PFCHS]'
    elif '_MatchedTohltPFCHSCorr'    in key: _objLabel += ' [Matched to PFCHSCorr]'
    elif '_MatchedTohltPFPuppi'      in key: _objLabel += ' [Matched to PFPuppi]'
    elif '_MatchedTohltPFPuppiCorr'  in key: _objLabel += ' [Matched to PFPuppiCorr]'
    elif '_MatchedToOffline'         in key: _objLabel += ' [Matched to Offline]'
    elif '_MatchedToHLT'         in key: _objLabel += ' [Matched to HLT]'

    ## axes' titles
    _titleX, _titleY = key, ''
    if isProfile:
       if 'Jets' in key:
          if key.endswith('_pt'): _titleX = 'Jet p_{T} [GeV]'
          elif key.endswith('_eta'): _titleX = 'Jet #eta'
          elif key.endswith('_phi'): _titleX = 'Jet #phi'
          elif key.endswith('_mass'): _titleX = 'Jet mass [GeV]'
          elif key.endswith('_offlineNPV'): _titleX = 'N_{PV}'
          elif key.endswith('_simNPU'): _titleX = 'N_{PU}'
       elif 'MET' in key:
          if key.endswith('_pt'): _titleX = 'MET [GeV]'
          elif key.endswith('_phi'): _titleX = 'MET #phi'
          elif key.endswith('_sumEt'): _titleX = 'MET Sum-E_{T} [GeV]'
          elif key.endswith('_offlineNPV'): _titleX = 'Offline N_{PV}'
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
          elif key.endswith('_simNPU_eff'): _titleX = 'N_{PU}'
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
       if key.endswith('_eff'):
         if '_NotMatchedTo' in key: _titleY = 'Jet Mis-tag' #'1 - #varepsilon_{Matching}'
         elif '_MatchedTo' in key: _titleY = 'Efficiency' #'#varepsilon_{Matching}'
         if '_MatchedToGEN' in key: _titleY = 'Purity'
         if '_MatchedToOffline' in key: _titleY = 'Purity'

    if   '_pt_overGEN_Mean_' in key: _titleY = '<p_{T} / p_{T}^{GEN}>'
    elif '_pt_overGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T} / p_{T}^{GEN}) / <p_{T} / p_{T}^{GEN}>'
    elif '_pt_overGEN_RMS_' in key: _titleY = '#sigma(p_{T} / p_{T}^{GEN})'

    elif '_pt_overOffline_Mean_' in key: _titleY = '<p_{T} / p_{T}^{Offl}>'
    elif '_pt_overOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T} / p_{T}^{Offl}) / <p_{T} / p_{T}^{Offl}>'
    elif '_pt_overOffline_RMS_' in key: _titleY = '#sigma(p_{T} / p_{T}^{Offl})'

    if   '_pt0_overGEN_Mean_' in key: _titleY = '<p_{T} / p_{T}^{GEN}>'
    elif '_pt0_overGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T} / p_{T}^{GEN}) / <p_{T} / p_{T}^{GEN}>'
    elif '_pt0_overGEN_RMS_' in key: _titleY = '#sigma(p_{T} / p_{T}^{GEN})'

    elif '_pt0_overOffline_Mean_' in key: _titleY = '<p_{T} / p_{T}^{Offl}>'
    elif '_pt0_overOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T} / p_{T}^{Offl}) / <p_{T} / p_{T}^{Offl}>'
    elif '_pt0_overOffline_RMS_' in key: _titleY = '#sigma(p_{T} / p_{T}^{Offl})'

    elif '_mass_overGEN_Mean_' in key: _titleY = '<mass / mass^{GEN}>'
    elif '_mass_overGEN_RMSOverMean_' in key: _titleY = '#sigma(m / m^{GEN}) / <m / m^{GEN}>'
    elif '_mass_overGEN_RMS_' in key: _titleY = '#sigma(mass / mass^{GEN})'

    elif '_mass_overOffline_Mean_' in key: _titleY = '<mass / mass^{Offl}>'
    elif '_mass_overOffline_RMSOverMean_' in key: _titleY = '#sigma(m / m^{Offl}) / <m / m^{Offl}>'
    elif '_mass_overOffline_RMS_' in key: _titleY = '#sigma(mass / mass^{Offl})'

    elif '_sumEt_overGEN_Mean_' in key: _titleY = '<Sum-E_{T} / Sum-E_{T}^{GEN}>'
    elif '_sumEt_overGEN_RMSOverMean_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{GEN}) / <Sum-E_{T} / Sum-E_{T}^{GEN}>'
    elif '_sumEt_overGEN_RMS_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{GEN})'

    elif '_sumEt_overOffline_Mean_' in key: _titleY = '<Sum-E_{T} / Sum-E_{T}^{Offl}>'
    elif '_sumEt_overOffline_RMSOverMean_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{Offl}) / <Sum-E_{T} / Sum-E_{T}^{Offl}>'
    elif '_sumEt_overOffline_RMS_' in key: _titleY = '#sigma(Sum-E_{T} / Sum-E_{T}^{Offl})'

    elif '_deltaPhiGEN_Mean_' in key: _titleY = '<#Delta#phi^{GEN}>'
#   elif '_deltaPhiGEN_RMSOverMean_' in key: _titleY = '#sigma(#Delta#phi^{GEN}) / <#Delta#phi^{GEN}>'
    elif '_deltaPhiGEN_RMS_' in key: _titleY = '#sigma(#Delta#phi^{GEN})'

    elif '_deltaPhiOffline_Mean_' in key: _titleY = '<#Delta#phi^{Offl}>'
#   elif '_deltaPhiOffline_RMSOverMean_' in key: _titleY = '#sigma(#Delta#phi^{Offl}) / <#Delta#phi^{Offl}>'
    elif '_deltaPhiOffline_RMS_' in key: _titleY = '#sigma(#Delta#phi^{Offl})'

    elif '_pt_paraToGEN_Mean_' in key: _titleY = '<p_{T}^{#parallel GEN}> [GeV]'
    elif '_pt_paraToGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN}) / <p_{T} / p_{T}^{GEN}> [GeV]'
    elif '_pt_paraToGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN}) [GeV]'

    elif '_pt_paraToOffline_Mean_' in key: _titleY = '<p_{T}^{#parallel Offl}> [GeV]'
    elif '_pt_paraToOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl}) / <p_{T} / p_{T}^{Offl}> [GeV]'
    elif '_pt_paraToOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl}) [GeV]'

    elif '_pt_paraToGENMinusGEN_Mean_' in key: _titleY = '<p_{T}^{#parallel GEN} - p_{T}^{GEN}> [GeV]'
    elif '_pt_paraToGENMinusGEN_RMSOverMean_' in key: _titleY = '#sigma(#Deltap_{T}^{#parallel GEN}) / <p_{T} / p_{T}^{GEN}> [GeV]'
    elif '_pt_paraToGENMinusGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel GEN} - p_{T}^{GEN}) [GeV]'

    elif '_pt_paraToOfflineMinusOffline_Mean_' in key: _titleY = '<p_{T}^{#parallel Offl} - p_{T}^{Offl}> [GeV]'
    elif '_pt_paraToOfflineMinusOffline_RMSOverMean_' in key: _titleY = '#sigma(#Deltap_{T}^{#parallel Offl}) / <p_{T} / p_{T}^{Offl}> [GeV]'
    elif '_pt_paraToOfflineMinusOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#parallel Offl} - p_{T}^{Offl}) [GeV]'

    elif '_pt_perpToGEN_Mean_' in key: _titleY = '<p_{T}^{#perp GEN}> [GeV]'
    elif '_pt_perpToGEN_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#perp GEN}) / <p_{T} / p_{T}^{GEN}> [GeV]'
    elif '_pt_perpToGEN_RMS_' in key: _titleY = '#sigma(p_{T}^{#perp GEN}) [GeV]'

    elif '_pt_perpToOffline_Mean_' in key: _titleY = '<p_{T}^{#perp Offl}> [GeV]'
    elif '_pt_perpToOffline_RMSOverMean_' in key: _titleY = '#sigma(p_{T}^{#perp Offl}) / <p_{T} / p_{T}^{Offl}> [GeV]'
    elif '_pt_perpToOffline_RMS_' in key: _titleY = '#sigma(p_{T}^{#perp Offl}) [GeV]'

    elif ('Jets' in key) and not (isProfile or isEfficiency):
      if   key.endswith('_pt_overGEN'): _titleX = 'p_{T} / p_{T}^{GEN}'
      elif key.endswith('_pt_overOffline'): _titleX = 'p_{T} / p_{T}^{Offl}'
      elif key.endswith('_pt0_overGEN'): _titleX = 'p_{T} / p_{T}^{GEN}'
      elif key.endswith('_pt0_overOffline'): _titleX = 'p_{T} / p_{T}^{Offl}'
      elif key.endswith('_mass_overGEN'): _titleX = 'mass / mass^{GEN}'
      elif key.endswith('_mass_overOffline'): _titleX = 'mass / mass^{Offl}'
      elif key.endswith('_pt0'): _titleX = 'p_{T}-Leading Jet p_{T} [GeV]'
      elif key.endswith('_pt0_cumul'): _titleX = 'Jet p_{T} threshold [GeV]'
      elif key.endswith('_pt'): _titleX = 'Jet p_{T} [GeV]'
      elif key.endswith('_eta'): _titleX = 'Jet #eta'
      elif key.endswith('_phi'): _titleX = 'Jet #phi [rad]'
      elif key.endswith('_mass'): _titleX = 'Jet mass [GeV]'
      elif key.endswith('_dRmatch'): _titleX = '#DeltaR'
      elif key.endswith('_numberOfDaughters'): _titleX = 'Number of jet constituents'
      elif key.endswith('_njets'): _titleX = 'Number of jets'
      elif key.endswith('_HT'): _titleX = 'H_{T} [GeV]'
      elif key.endswith('_HT_cumul'): _titleX = 'H_{T} threshold [GeV]'
      elif key.endswith('_MHT'): _titleX = 'MHT [GeV]'
      elif key.endswith('_MHT_cumul'): _titleX = 'MHT threshold [GeV]'
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

    elif ('MET' in key) and not (isProfile or isEfficiency):
      if   key.endswith('_pt_overGEN'): _titleX = 'MET / MET^{GEN}'
      elif key.endswith('_pt_overOffline'): _titleX = 'MET / MET^{Offl}'
      elif key.endswith('_pt_paraToGEN'): _titleX = 'p_{T}^{#parallel GEN} [GeV]'
      elif key.endswith('_pt_paraToOffline'): _titleX = 'p_{T}^{#parallel Offl} [GeV]'
      elif key.endswith('_pt_paraToGENMinusGEN'): _titleX = 'p_{T}^{#parallel GEN} - p_{T}^{GEN} [GeV]'
      elif key.endswith('_pt_paraToOfflineMinusOffline'): _titleX = 'p_{T}^{#parallel Offl} - p_{T}^{Offl} [GeV]'
      elif key.endswith('_pt_perpToGEN'): _titleX = 'p_{T}^{#perp GEN} [GeV]'
      elif key.endswith('_pt_perpToOffline'): _titleX = 'p_{T}^{#perp Offl} [GeV]'
      elif key.endswith('_pt'): _titleX = 'MET [GeV]'
      elif key.endswith('_pt_cumul'): _titleX = 'MET threshold [GeV]'
      elif key.endswith('_phi'): _titleX = 'MET #phi'
      elif key.endswith('_sumEt'): _titleX = 'Sum-E_{T} [GeV]'
      elif key.endswith('_sumEt_overGEN'): _titleX = 'Sum-E_{T} / Sum-E_{T}^{GEN}'
      elif key.endswith('_sumEt_overOffline'): _titleX = 'Sum-E_{T} / Sum-E_{T}^{Offl}'
      elif key.endswith('_deltaPhiGEN'): _titleX = '#Delta#phi^{GEN}'
      elif key.endswith('_deltaPhiOffline'): _titleX = '#Delta#phi^{Offl}'

    return _titleX, _titleY, _objLabel

class PlotConfig:
    def __init__(self):
        self.hists = []
        self.IsProfile = False
        self.IsEfficiency = False
        self.logY = False
        self.logX = False
        self.titleX = ''
        self.titleY = ''
        self.objLabel = ''
#        self.divideByBinWidth = False
        self.normalizedToUnity = True
        self.legXY = [0.75, 0.60, 0.95, 0.90]
        self.xMin = None
        self.xMax = None
        self.yMin = None
        self.yMax = None
        self.ratio = True
        self.autoRangeX = True
        self.xLabelSize = None
        self.xBinLabels= []
        self.outputName = 'tmp'

def getHistogram(key, inputDict, plotCfg, **kwargs):

    Legend      = kwargs.get('Legend'     , inputDict['Legend'])
    Color       = kwargs.get('Color'      , inputDict['LineColor'])
    LineWidth   = kwargs.get('LineStyle'  , 2)
    LineStyle   = kwargs.get('LineStyle'  , inputDict['LineStyle'])
    MarkerStyle = kwargs.get('MarkerStyle', inputDict['MarkerStyle'])
    MarkerSize  = kwargs.get('MarkerSize' , inputDict['MarkerSize'])

    if key not in inputDict['TH1s']:
       return None

    h0 = inputDict['TH1s'][key].Clone()

    if h0.InheritsFrom('TH2'):
       return None

    h0.UseCurrentStyle()
    if hasattr(h0, 'SetDirectory'):
       h0.SetDirectory(0)

    h0.SetLineColor(Color)
    h0.SetLineWidth(2)
    h0.SetLineStyle(1 if (plotCfg.IsProfile or plotCfg.IsEfficiency) else LineStyle)
    h0.SetMarkerStyle(MarkerStyle)
    h0.SetMarkerColor(Color)
    h0.SetMarkerSize(MarkerSize if (plotCfg.IsProfile or plotCfg.IsEfficiency) else 0.)

    h0.SetBit(ROOT.TH1.kNoTitle)

    if hasattr(h0, 'SetStats'):
       h0.SetStats(0)

    hist0 = Histogram()
    hist0.th1 = h0
    hist0.draw = 'ep' if (plotCfg.IsProfile or plotCfg.IsEfficiency) else 'hist,e0'
    hist0.draw += ',same'
    hist0.Legend = Legend
    hist0.LegendDraw = 'ep' if (plotCfg.IsProfile or plotCfg.IsEfficiency) else 'l'

    return hist0

def getPlotConfig(key, keyword, inputList):

    cfg = PlotConfig()

    key_basename = os.path.basename(key)
    key_dirname = os.path.dirname(key)

    cfg.outputName = key

    cfg.IsProfile = '_wrt_' in key_basename

    cfg.IsEfficiency = key_basename.endswith('_eff')

    cfg.logY = ('_NotMatchedTo' in key_basename) and key_basename.endswith('pt_eff')

    cfg.titleX, cfg.titleY, cfg.objLabel = getPlotLabels(key=key_basename, isProfile=cfg.IsProfile, isEfficiency=cfg.IsEfficiency, keyword=keyword)

    cfg.hists = []

    ##
    ## keyword: run3_dqm_compareTRK2
    ##
    if keyword == 'run3_dqm_compareTRK2':

       if key.endswith('pfcand_particleId'):
          cfg.xLabelSize, cfg.xBinLabels = 0.2, ['X', 'h', 'e', '#mu', '#gamma', 'h0', 'h_HF', 'eg_HF']

       if key.endswith('_pt_2'):
          cfg.logY, cfg.xMin, cfg.xMax = True, 0., 300.

       skip_key = False
       for _pfTypeTag in ['_h', '_e', '_mu', '_gamma', '_h0']:
          if key_dirname.endswith(_pfTypeTag) and key_basename.startswith('pfcand_mult_') and (not key_basename.endswith(_pfTypeTag)):
             skip_key = True
             break
       if skip_key:
          return

       if ('_hltParticleFlow/' in key) or ('_hltParticleFlow_' in key):
         cfg.legXY = [0.55, 0.50, 0.99, 0.99]
         cfg.outputName = key.replace('_hltParticleFlow', '')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_offlineParticleFlow') , Legend='Offline PF'            , Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltParticleFlow')     , Legend='hltParticleFlow'+legTag, Color=ROOT.kBlack)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltParticleFlowCHSv1'), Legend='hltPFCHSv1'     +legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltParticleFlowCHSv2'), Legend='hltPFCHSv2'     +legTag, Color=ROOT.kViolet)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltPFPuppiV1')          , Legend='hltPFPuppiV1'     +legTag, Color=ROOT.kOrange+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltPFPuppiV3')          , Legend='hltPFPuppiV3'     +legTag, Color=ROOT.kRed)]

       elif '_hltPixelTracks' in key:
         cfg.legXY = [0.55, 0.75, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPixelTracks'+legTag)]

       elif '_hltMergedTracks' in key:
         cfg.legXY = [0.45, 0.70, 0.99, 0.99]
         cfg.outputName = key.replace('_hltMergedTracks', '')
         iter0Tracks = 'hltIter0PFlowTrackSelectionHighPurity'
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltMergedTracks', '_hltMergedTracks'), Legend='hltMergedTracks'+legTag) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltMergedTracks', '_'+iter0Tracks), Legend=iter0Tracks+legTag) if (idx != 0) else None]

       elif '_hltPixelVertices' in key:
         cfg.legXY = [0.55, 0.70, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPixelVertices', '_offlineSlimmedPrimaryVertices'), Legend='offlinePrimaryVertices', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPixelVertices', '_hltPixelVertices'), Legend='hltPixelVertices'+legTag)]

       elif '_hltVerticesPF' in key:
         cfg.legXY = [0.55, 0.70, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltVerticesPF', '_offlineSlimmedPrimaryVertices'), Legend='offlinePrimaryVertices', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltVerticesPF', '_hltVerticesPF'), Legend='hltVerticesPF'+legTag)]

    ##
    ## keyword: run3_dqm_compareTRK5
    ##
    elif keyword == 'run3_dqm_compareTRK5':

       if key.endswith('pfcand_particleId'):
          cfg.xLabelSize, cfg.xBinLabels = 0.2, ['X', 'h', 'e', '#mu', '#gamma', 'h0', 'h_HF', 'eg_HF']

       if key.endswith('_pt_2'):
          cfg.logY, cfg.xMin, cfg.xMax = True, 0., 300.

       skip_key = False
       for _pfTypeTag in ['_h', '_e', '_mu', '_gamma', '_h0']:
          if key_dirname.endswith(_pfTypeTag) and key_basename.startswith('pfcand_mult_') and (not key_basename.endswith(_pfTypeTag)):
             skip_key = True
             break
       if skip_key:
          return

       if ('_hltParticleFlow/' in key) or ('_hltParticleFlow_' in key):
         cfg.legXY = [0.55, 0.60, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_offlineParticleFlow'), Legend='Offline PF', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltParticleFlow'+legTag)]

       elif '_hltPFPuppiV1' in key:
         cfg.legXY = [0.55, 0.60, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPFPuppiV1', '_offlineParticleFlow'), Legend='Offline PF', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFPuppiV1'+legTag)]

       elif '_hltPFPuppiV3' in key:
         cfg.legXY = [0.55, 0.60, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPFPuppiV3', '_offlineParticleFlow'), Legend='Offline PF', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFPuppiV3'+legTag)]

       elif '_hltVerticesPF' in key:
         cfg.legXY = [0.45, 0.70, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltVerticesPF', '_offlineSlimmedPrimaryVertices'), Legend='offlinePrimaryVertices', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltVerticesPF', '_hltPixelVertices'), Legend='hltPixelVertices'+legTag, Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltVerticesPF'+legTag)]

       elif '_hltMergedTracks' in key:
         cfg.legXY = [0.45, 0.70, 0.99, 0.99]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltMergedTracks'+legTag, Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltMergedTracks', '_hltIter0PFlowTrackSelectionHighPurity'), Legend='hltIter0PFlowTrackSelectionHighPurity'+legTag)]
    ###
    ### compare_PFCalo_PFHC
    ###
    elif keyword == 'compare_PFCalo_PFHC':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if key.endswith('_pt_eff'):
          cfg.xMin, cfg.xMax = 0., 300.
       
       cfg.legXY = [0.50, 0.22, 1.0, 0.55]

       ## MET
      #  if 'hltPFMET_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltPFMETTypeOne_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       ## Jets
      #  elif 'hltAK4PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
      #  if ('hltAK4PFJetsCorrected_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      
       if 'hltAK4PFJets_'  in key:
          if ('_MatchedToGEN_' in key) and (('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             for idx, inp in enumerate(inputList):
               if 'Pt' in key:
                  break
               if ('RMSOverMean_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key):
                  cfg.legXY = [0.15, 0.50, 0.95, 0.95]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'hltAK4CaloJets_'), Legend='Calo', Color=ROOT.kBlue, LineStyle=2) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      
      #  elif 'hltAK4CaloJets_'  in key:
      #     if ('MatchedToGEN_' in key) and (('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
      #        for idx, inp in enumerate(inputList):
      #          if 'Pt' in key:
      #             break
      #          if ('RMSOverMean_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key):
      #             cfg.legXY = [0.15, 0.50, 0.95, 0.95]
      #          #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJets_', 'offlineAK4PFPuppiJets_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
      #          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltAK8PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif ('hltAK4CaloJets_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJets_', 'offlineAK4PFPuppiJets_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'MatchedTohltPF_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltCaloCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltCaloCorr_', 'MatchedToofflPFPuppiCorr_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]
       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltPFCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltPFCorr_', 'MatchedToofflPFPuppiCorr_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
    
    
    ###
    ### compare_PFCalo_PFHC
    ###
    elif keyword == 'compare_PFCalo_PFHC_withOffline':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if key.endswith('_pt_eff'):
          cfg.xMin, cfg.xMax = 0., 300.
       
       cfg.legXY = [0.50, 0.22, 1.0, 0.55]

       ## MET
      #  if 'hltPFMET_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltPFMETTypeOne_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       ## Jets
      #  elif 'hltAK4PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
      #  if ('hltAK4PFJetsCorrected_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      
       if 'hltAK4PFJets_'  in key:
          if ('_MatchedToGEN_' in key) and (('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             for idx, inp in enumerate(inputList):
               if 'Pt' in key:
                  break
               if ('RMSOverMean_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key):
                  cfg.legXY = [0.15, 0.50, 0.95, 0.95]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'hltAK4CaloJets_'), Legend='HLT Calo', Color=ROOT.kBlue, LineStyle=2) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'offlineAK4PFPuppiJets_'), Legend='Offline PF', Color=ROOT.kRed, LineStyle=2) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      
      #  elif 'hltAK4CaloJets_'  in key:
      #     if ('MatchedToGEN_' in key) and (('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
      #        for idx, inp in enumerate(inputList):
      #          if 'Pt' in key:
      #             break
      #          if ('RMSOverMean_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key):
      #             cfg.legXY = [0.15, 0.50, 0.95, 0.95]
      #          #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJets_', 'offlineAK4PFPuppiJets_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
      #          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltAK8PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif ('hltAK4CaloJets_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJets_', 'offlineAK4PFPuppiJets_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'MatchedTohltPF_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltCaloCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltCaloCorr_', 'MatchedToofflPFPuppiCorr_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]
       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltPFCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltPFCorr_', 'MatchedToofflPFPuppiCorr_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
    

    ###
    ### version_check
    ###
    elif keyword == 'version_check':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if key.endswith('_pt_eff'):
          cfg.xMin, cfg.xMax = 0., 300.
       
       cfg.legXY = [0.50, 0.22, 1.0, 0.55]

       ## MET
      #  if 'hltPFMET_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltPFMETTypeOne_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       ## Jets
      #  elif 'hltAK4PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
      #  if ('hltAK4PFJetsCorrected_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      
       if 'hltAK4PFJetsCorrected_'  in key:
          if ('_MatchedToGEN_' in key) and (('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             for idx, inp in enumerate(inputList):
               if 'Pt' in key:
                  break
               if ('RMSOverMean_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key):
                  cfg.legXY = [0.15, 0.50, 0.95, 0.95]
               #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      
       elif 'hltAK4CaloJetsCorrected_'  in key:
          if ('MatchedToGEN_' in key) and (('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             for idx, inp in enumerate(inputList):
               if 'Pt' in key:
                  break
               if ('RMSOverMean_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key):
                  cfg.legXY = [0.15, 0.50, 0.95, 0.95]
               #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltAK8PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif ('hltAK4CaloJetsCorrected_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'MatchedTohltPF_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltCaloCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltCaloCorr_', 'MatchedToofflPFPuppiCorr_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]
       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltPFCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltPFCorr_', 'MatchedToofflPFPuppiCorr_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

    ###
    ### version_check_mc
    ###
    elif keyword == 'version_check_mc':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

      #  if key.endswith('_pt_eff'):
      #     cfg.xMin, cfg.xMax = 0., 300.
       
       cfg.legXY = [0.50, 0.22, 1.0, 0.55]

       ## MET
      #  if 'hltPFMET_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltPFMETTypeOne_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       ## Jets
      #  elif 'hltAK4PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
      #  if ('hltAK4PFJetsCorrected_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
       
       
       if 'hltAK4PFJetsCorrected_'  in key:
          distributionQuantity = ((('EtaIncl' in key) and (key.endswith('_pt') or key.endswith('_eta') or key.endswith('_phi') or key.endswith('_HT'))) or key.endswith('_chargedHadronEnergyFraction') or key.endswith('_chargedHadronMultiplicity') or key.endswith('_neutralHadronEnergyFraction') or key.endswith('_neutralHadronMultiplicity') or key.endswith('_photonEnergyFraction') or key.endswith('_photonMultiplicity') ) 
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt') or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          if ('_MatchedToGEN_' in key) and (distributionQuantity or ('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or ('_phi' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             for idx, inp in enumerate(inputList):
               #if 'Pt' in key:
               #   break
               if ('RMS_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key) or key.endswith('_HT'):
                  cfg.legXY = [0.50, 0.50, 0.95, 0.95]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'hltAK4CaloJetsCorrected_'), Legend='Calo', Color=ROOT.kBlue) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltPFCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key) or ('_phi_eff' in key)):
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt')  or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltPFCorr_', 'MatchedTohltCaloCorr_'), Legend='Calo', Color=ROOT.kBlue) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])] 

       if 'hltAK8PFJetsCorrected_'  in key:
          distributionQuantity = ((('EtaIncl' in key) and (key.endswith('_pt') or key.endswith('_eta') or key.endswith('_phi') or key.endswith('_HT'))) or key.endswith('_chargedHadronEnergyFraction') or key.endswith('_chargedHadronMultiplicity') or key.endswith('_neutralHadronEnergyFraction') or key.endswith('_neutralHadronMultiplicity') or key.endswith('_photonEnergyFraction') or key.endswith('_photonMultiplicity') ) 
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt') or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          if ('_MatchedToGEN_' in key) and (distributionQuantity or ('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or ('_phi' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             for idx, inp in enumerate(inputList):
               #if 'Pt' in key:
               #   break
               if ('RMS_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key) or key.endswith('_HT'):
                  cfg.legXY = [0.50, 0.50, 0.95, 0.95]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PFJetsCorrected_', 'hltAK8CaloJetsCorrected_'), Legend='Calo', Color=ROOT.kBlue) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
       elif ('ak8GenJetsNoNu' in key) and ('_MatchedTohltPFCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key) or ('_phi_eff' in key)):
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt')  or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltPFCorr_', 'MatchedTohltCaloCorr_'), Legend='Calo', Color=ROOT.kBlue) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])] 
       '''
       elif 'hltAK4CaloJetsCorrected_'  in key:
          distributionQuantity = ((('EtaIncl' in key) and (key.endswith('_pt') or key.endswith('_eta') or key.endswith('_phi') or key.endswith('_HT')))) 
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt') or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          if ('MatchedToGEN_' in key) and (distributionQuantity or ('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             for idx, inp in enumerate(inputList):
               #if 'Pt' in key:
               #   break
               if ('RMS_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key) or key.endswith('_HT'):
                  cfg.legXY = [0.50, 0.50, 0.95, 0.95]
               #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]
       

       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltCaloCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt')  or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltCaloCorr_', 'MatchedToofflPFPuppiCorr_'), Legend='Offline PUPPI', Color=ROOT.kPink, LineStyle=2) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]
       '''
    
        ###
    ### version_check_data_new
    ###
    elif keyword == 'version_check_data_new':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

      #  if key.endswith('_pt_eff'):
      #     cfg.xMin, cfg.xMax = 0., 300.
       
       cfg.legXY = [0.50, 0.22, 1.0, 0.55]

       ## MET
      #  if 'hltPFMET_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltPFMETTypeOne_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       ## Jets
      #  elif 'hltAK4PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
      #  if ('hltAK4PFJetsCorrected_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
       
       
      #  if 'hltAK4PFJetsCorrected_'  in key:
      #     distributionQuantity = ((('EtaIncl' in key) and (key.endswith('_pt') or key.endswith('_eta') or key.endswith('_phi') or key.endswith('_HT'))) or key.endswith('_chargedHadronEnergyFraction') or key.endswith('_chargedHadronMultiplicity') or key.endswith('_neutralHadronEnergyFraction') or key.endswith('_neutralHadronMultiplicity') or key.endswith('_photonEnergyFraction') or key.endswith('_photonMultiplicity') ) 
      #     cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
      #     cfg.logY=((key.endswith('_pt') or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
      #     if ('_MatchedToOffline_' in key) and (distributionQuantity or ('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_simNPU' in key) or ('pt_overOffline' in key) or ('_pt_eff' in key) or ('_phi' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overOffline_Mean_wrt_Offline_eta' in key)))):
      #        for idx, inp in enumerate(inputList):
      #          #if 'Pt' in key:
      #          #   break
      #          if ('RMS_wrt_Offline_pt' in key) or ('NotMatchedToOffline_' in key) or key.endswith('_HT'):
      #             cfg.legXY = [0.50, 0.50, 0.95, 0.95]
      #          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'hltAK4CaloJetsCorrected_'), Legend='Calo', Color=ROOT.kBlue) if idx==0 else None]
      #          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
      #  elif ('offlineAK4PFPuppiJetsCorrected_' in key) and ('_MatchedTohltPFCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key) or ('_phi_eff' in key)):
      #     cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
      #     cfg.logY=((key.endswith('_pt')  or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltPFCorr_', 'MatchedTohltCaloCorr_'), Legend='Calo', Color=ROOT.kBlue) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])] 

       if 'hltAK4CaloJetsCorrected_'  in key:
          distributionQuantity = (((key.endswith('_pt') or key.endswith('_eta') or key.endswith('_phi') or key.endswith('_HT'))) or key.endswith('_chargedHadronEnergyFraction') or key.endswith('_chargedHadronMultiplicity') or key.endswith('_neutralHadronEnergyFraction') or key.endswith('_neutralHadronMultiplicity') or key.endswith('_photonEnergyFraction') or key.endswith('_photonMultiplicity') ) 
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt') or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          if ('_MatchedToOffline_' in key) and (distributionQuantity or ('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_simNPU' in key) or ('pt_overOffline' in key) or ('_pt_eff' in key) or ('_phi' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overOffline_Mean_wrt_Offline_eta' in key)))):
             for idx, inp in enumerate(inputList):
               #if 'Pt' in key:
               #   break
               if ('RMS_wrt_Offline_pt' in key):
                  cfg.xMin=40
                  cfg.xMax=300
               if ('RMS_wrt_Offline_pt' in key) or ('NotMatchedToOffline_' in key) or key.endswith('_HT'):
                  cfg.legXY = [0.50, 0.50, 0.95, 0.95]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJetsCorrected_', 'hltAK4PFJetsCorrected_'), Legend='PF', Color=ROOT.kBlue) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]
       
       elif ('offlineAK4CaloPuppiJetsCorrected_' in key) and ('_MatchedTohltCaloCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key) or ('_phi_eff' in key)):
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt')  or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltCaloCorr_', 'MatchedTohltPFCorr_'), Legend='PF', Color=ROOT.kBlue) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])] 

      #  if 'hltAK8PFJetsCorrected_'  in key:
      #     distributionQuantity = ((('EtaIncl' in key) and (key.endswith('_pt') or key.endswith('_eta') or key.endswith('_phi') or key.endswith('_HT'))) or key.endswith('_chargedHadronEnergyFraction') or key.endswith('_chargedHadronMultiplicity') or key.endswith('_neutralHadronEnergyFraction') or key.endswith('_neutralHadronMultiplicity') or key.endswith('_photonEnergyFraction') or key.endswith('_photonMultiplicity') ) 
      #     cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
      #     cfg.logY=((key.endswith('_pt') or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
      #     if ('_MatchedToGEN_' in key) and (distributionQuantity or ('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or ('_phi' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
      #        for idx, inp in enumerate(inputList):
      #          #if 'Pt' in key:
      #          #   break
      #          if ('RMS_wrt_GEN_pt' in key) or ('NotMatchedToGEN_' in key) or key.endswith('_HT'):
      #             cfg.legXY = [0.50, 0.50, 0.95, 0.95]
      #          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PFJetsCorrected_', 'hltAK8CaloJetsCorrected_'), Legend='Calo', Color=ROOT.kBlue) if idx==0 else None]
      #          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
      #  elif ('ak8GenJetsNoNu' in key) and ('_MatchedTohltPFCorr_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key) or ('_phi_eff' in key)):
      #     cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
      #     cfg.logY=((key.endswith('_pt')  or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltPFCorr_', 'MatchedTohltCaloCorr_'), Legend='Calo', Color=ROOT.kBlue) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])] 
      
      #  elif ( ('hltPFMET' in key ) and ( (key=='NoSelection/hltPFMET_pt') or (key=='NoSelection/hltPFMET_phi') or (('_Mean_' in key) or ('_RMSOverMean_' in key)) ) ):
      #     cfg.logY=(key=='NoSelection/hltPFMET_pt')
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT PF MET('+inp['Legend']+')')]
       elif ( ('hltCaloMET' in key ) and ( (key=='NoSelection/hltCaloMET_pt') or (key=='NoSelection/hltCaloMET_phi') or (('_Mean_' in key) or ('_RMSOverMean_' in key) or (('_RMS_' in key))) ) ):
          cfg.logY=(key=='NoSelection/hltCaloMET_pt')
 
          if ('_wrt_Offline_pt' in key):
             cfg.xMin=50
             cfg.xMax=200
             cfg.legXY = [0.50, 0.50, 0.95, 0.95]
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCaloMET_', 'hltPFMET_'), Legend='PF', Color=ROOT.kBlue) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT Calo MET('+inp['Legend']+')')]

    ###
    ### version_check_mc_raw
    ###
    elif keyword == 'version_check_mc_raw':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

      #  if key.endswith('_pt_eff'):
      #     cfg.xMin, cfg.xMax = 0., 300.
       
       cfg.legXY = [0.50, 0.22, 1.0, 0.55]

       ## MET
      #  if 'hltPFMET_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'hltPFMETTypeOne_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       ## Jets
      #  elif 'hltAK4PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
      #  if ('hltAK4PFJetsCorrected_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
       
       
       if 'hltAK4PFJets_'  in key:
          distributionQuantity = ((('EtaIncl' in key) and (key.endswith('_pt') or key.endswith('_eta') or key.endswith('_phi') or key.endswith('_HT'))) or key.endswith('_chargedHadronEnergyFraction') or key.endswith('_chargedHadronMultiplicity') or key.endswith('_neutralHadronEnergyFraction') or key.endswith('_neutralHadronMultiplicity') or key.endswith('_photonEnergyFraction') or key.endswith('_photonMultiplicity') ) 
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt') or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          if ('_MatchedToGEN_' in key) and (distributionQuantity or ('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('pt_overGEN' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             for idx, inp in enumerate(inputList):
               if 'Pt' in key:
                  break
               if ('RMS_' in key) or ('NotMatchedToGEN_' in key) or key.endswith('_HT') or ('RMSOverMean_' in key):
                  cfg.legXY = [0.50, 0.50, 0.95, 0.95]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'hltAK4CaloJets_'), Legend='Calo', Color=ROOT.kBlue, LineStyle=2) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
       
     
      #  elif 'hltAK8PFJets_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif ('hltAK4CaloJetsCorrected_' in key) and ('MatchedToGEN_' in key):
      #     for idx, inp in enumerate(inputList):
      #       #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

      #  elif 'MatchedTohltPF_' in key:
      #     for idx, inp in enumerate(inputList):
      #       cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

       elif ('ak4GenJetsNoNu' in key) and ('_MatchedTohltPF_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          cfg.logX=(key.endswith('_pt') or key.endswith('_pt_eff'))
          cfg.logY=((key.endswith('_pt')  or key.endswith('_HT')) and not (('RMS' in key) or ('Mean' in key)) )
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('MatchedTohltPF_', 'MatchedTohltCalo_'), Legend='Calo', Color=ROOT.kBlue, LineStyle=2) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])] 

       elif ( ('hltPFMET' in key ) and ( (key=='NoSelection/hltPFMET_pt') or (key=='NoSelection/hltPFMET_phi') or (('_Mean_' in key) or ('_RMSOverMean_' in key)) ) ):
          cfg.logY=(key=='NoSelection/hltPFMET_pt')
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT PF MET('+inp['Legend']+')')]

    ###
    ### version_check_data
    ###
    elif keyword == 'version_check_data':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

      #  if key.endswith('_pt_eff'):
      #     cfg.xMin, cfg.xMax = 0., 300.
       
       cfg.legXY = [0.35, 0.22, 1.0, 0.55]

       ## Jets
       
       # AK4

       if 'hltAK4PFJetsCorrected_'  in key:
          if ('_MatchedToOffline_' in key) and (('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_offlineNPV' in key) or ('pt_overOffline' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overOffline_Mean_wrt_Offline_eta' in key)))):
             for idx, inp in enumerate(inputList):
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      
       elif 'hltAK4CaloJetsCorrected_'  in key:
          if ('MatchedToOffline_' in key) and (('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_offlineNPV' in key) or ('pt_overOffline' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overOffline_Mean_wrt_Offline_eta' in key)))):
             for idx, inp in enumerate(inputList):
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

       elif ('offlineAK4PFPuppiJetsCorrected' in key) and ('_MatchedToHLT_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]

      
      # AK8

       if 'hltAK8PFJetsCorrected_'  in key:
          if ('_MatchedToOffline_' in key) and (('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_offlineNPV' in key) or ('pt_overOffline' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overOffline_Mean_wrt_Offline_eta' in key)))):
             for idx, inp in enumerate(inputList):
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      
       elif 'hltAK8CaloJetsCorrected_'  in key:
          if ('MatchedToOffline_' in key) and (('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_offlineNPV' in key) or ('pt_overOffline' in key) or ('_pt_eff' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overOffline_Mean_wrt_Offline_eta' in key)))):
             for idx, inp in enumerate(inputList):
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=inp['LineColor'])]

       elif ('offlineAK8PFPuppiJetsCorrected' in key) and ('_MatchedToHLT_' in key) and ((('eta_eff' in key) and ('EtaIncl' in key)) or ('pt_eff' in key)):
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
      


      ## MET ## 

       elif ( ('hltPFMET' in key ) and ( (key=='NoSelection/hltPFMET_pt') or (key=='NoSelection/hltPFMET_phi') or (('pt_overOffline_Mean_wrt_offlineNPV' in key) or ('pt_overOffline_RMSOverMean_wrt_offlineNPV' in key) or ('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key)) ) ):
          cfg.logY=(key=='NoSelection/hltPFMET_pt')
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT PF MET('+inp['Legend']+')')]

       elif ( ('hltCaloMET' in key ) and ( (key=='NoSelection/hltCaloMET_pt') or (key=='NoSelection/hltCaloMET_phi') or (('pt_overOffline_Mean_wrt_offlineNPV' in key) or ('pt_overOffline_RMSOverMean_wrt_offlineNPV' in key) or ('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key)) ) ):
          cfg.logY=(key=='NoSelection/hltCaloMET_pt')
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT Calo MET('+inp['Legend']+')')]  
        
       elif ( ('hltPFMETTypeOne' in key ) and ( (key=='NoSelection/hltPFMETTypeOne_pt') or (key=='NoSelection/hltPFMETTypeOne_phi') or (('pt_overOffline_Mean_wrt_offlineNPV' in key) or ('pt_overOffline_RMSOverMean_wrt_offlineNPV' in key) or ('pt_overOffline_Mean_wrt_Offline_pt' in key) or ('pt_overOffline_RMSOverMean_wrt_Offline_pt' in key)) ) ):
          cfg.logY=(key=='NoSelection/hltPFMETTypeOne_pt')
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT PF Type1 MET('+inp['Legend']+')')] 

    ##
    ## keyword: run3_jme_pfperformance
    ##
    elif keyword == 'run3_jme_pfperformance':
       
       if ('/' in key) and ((not key.startswith('NoSelection/')) and (not key.startswith('noPUtracks/')) and (not key.startswith('withPUtracks/')) ):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.22, 1.0, 0.40]

       

       ## AK4 PF jets ##
       if 'hltAK4PFJetsCorrected_'  in key:
          #if ('_MatchedToGEN_' in key) and (('pt_overGEN_Mean_wrt_GEN_simNPU' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key)):
          if ('_MatchedToGEN_' in key) and (('pt_overGEN_Mean_wrt_GEN_simNPU' in key) or ('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_simNPU' in key) or ('_simNPU_eff' in key) or ('_pt_eff' in key) or ('_phi_' in key) or (('EtaIncl' in key) and (('_eta_eff' in key) or ('pt_overGEN_Mean_wrt_GEN_eta' in key)))):
             if 'GEN_pt' in key:
               cfg.logX = True
             for idx, inp in enumerate(inputList):
               # if 'Pt' in key:
               #    break
               #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'hltAK4CaloJetsCorrected_'), Legend='HLT Calo', Color=ROOT.kBlack) if idx==0 else None]
               cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'hltAK4PFJetsCorrected_'), Legend='HLT PF [ '+inp['Legend']+' ]')]
               #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT  [ '+inp['Legend']+' ]') if idx>0 else None]
          
       
       elif ('_MatchedTohltPFCorr_simNPU_eff' in key) or ('_MatchedTohltPFCorr_pt_eff' in key) or ('EtaIncl_MatchedTohltPFCorr_eta_eff' in key) or ('_MatchedTohltPFCorr_phi_eff' in key):
         for idx, inp in enumerate(inputList):
           #   if 'Pt' in key:
           #          break
           #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFCorr_', 'hltCaloCorr_'), Legend='HLT Calo', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFCorr_', 'hltPFCorr_'), Legend='HLT PF [ '+inp['Legend']+' ]')]
           #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT  [ '+inp['Legend']+' ]') if idx>0 else None]   
      
      ## MET ##   
       elif ( ('hltPFMETTypeOne' in key ) and ( (key=='NoSelection/hltPFMETTypeOne_pt') or (('pt_overGEN_Mean_wrt_simNPU' in key) or ('pt_overGEN_RMSOverMean_wrt_simNPU' in key) or ('pt_overGEN_Mean_wrt_GEN_pt' in key) or ('pt_overGEN_RMSOverMean_wrt_GEN_pt' in key)) ) ):
          cfg.logY=(key=='NoSelection/hltPFMETTypeOne_pt')
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_'), Legend='Offline',Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMETTypeOne_', 'hltPFMETTypeOne_'), Legend='Type1 MET PF [ '+inp['Legend']+' ]')]
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT Type1 MET') if idx>0 else None] 
    ##
    ## keyword: run3_jme_compareTRK1
    ##
    elif keyword == 'run3_jme_compareTRK1':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.40, 0.95, 0.90]

       if 'hltPFMET_' in key:
         cfg.objLabel = cfg.objLabel.replace('hltPFMET', 'MET')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_')     , Legend='Offline PFMET'       , Color=ROOT.kGreen+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline PFPuppiMET'  , Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltCaloMET_')           , Legend='hltCaloMET'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFClusterMET_')      , Legend='hltPFClusterMET'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFMET_')             , Legend='hltPFMET'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFPuppiMET_')        , Legend='hltPFPuppiMET'+legTag, Color=ROOT.kRed)]

       elif 'hltAK4PFJets_' in key:
         baseColl = 'hltAK4PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4')
         cfg.legXY = [0.55, 0.50, 0.95, 0.90]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJets_')     , Legend='hltAK4CaloJets'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFClusterJets_'), Legend='hltAK4PFClusterJets'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJets_')       , Legend='hltAK4PFJets'+legTag     , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFPuppiJets_')  , Legend='hltAK4PFPuppiJets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK4PFJetsCorrected_' in key:
         baseColl = 'hltAK4PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4+JECs')
         cfg.legXY = [0.55, 0.50, 0.95, 0.90]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='offlineAK4PFPuppiJetsCorrected', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJetsCorrected_')       , Legend='hltAK4CaloJetsCorrected'       , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJetsCorrected_')         , Legend='hltAK4PFJetsCorrected'+legTag  , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFPuppiJets_')             , Legend='hltAK4PFPuppiJets'+legTag      , Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJets_' in key:
         baseColl = 'hltAK8PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8')
         cfg.legXY = [0.55, 0.40, 0.95, 0.90]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJets_')     , Legend='hltAK8CaloJets'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFClusterJets_'), Legend='hltAK8PFClusterJets'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJets_')       , Legend='hltAK8PFJets'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFPuppiJets_')  , Legend='hltAK8PFPuppiJets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJetsCorrected_' in key:
         baseColl = 'hltAK8PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8+JECs')
         cfg.legXY = [0.55, 0.50, 0.95, 0.90]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='offlineAK8PFPuppiJetsCorrected', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJetsCorrected_')       , Legend='hltAK8CaloJetsCorrected'       , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJetsCorrected_')         , Legend='hltAK8PFJetsCorrected'+legTag  , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFPuppiJets_')             , Legend='hltAK8PFPuppiJets'+legTag      , Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPF_' in key:
         baseColl = 'PF'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(w/o JECs)')
         cfg.legXY = [0.55, 0.50, 0.95, 0.90]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltCalo_')     , Legend='Calo'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFCluster_'), Legend='PFCluster'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPF_')       , Legend='PF'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFPuppi_')  , Legend='PFPuppi'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPFCorr_' in key:
         baseColl = 'PFCorr'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(+JECs)')
         cfg.legXY = [0.55, 0.50, 0.95, 0.90]
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlPFPuppiCorr_') , Legend='OfflineCorr'       , Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltCaloCorr_')     , Legend='CaloCorr'          , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFClusterCorr_'), Legend='PFClusterCorr'     , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFCorr_')       , Legend='PFCorr'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFPuppi_')      , Legend='PFPuppi'    +legTag, Color=ROOT.kRed)]
         del baseColl, legTag

    ##
    ## keyword: run3_jme_compareTRK2
    ##
    elif keyword == 'run3_jme_compareTRK2':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.75, 0.70, 0.95, 0.90]

       if 'hltPFMET_' in key:
         cfg.objLabel = cfg.objLabel.replace('hltPFMET', 'MET')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_')     , Legend='Offline PFMET'     , Color=ROOT.kGreen+2)  if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline PFPuppiMET', Color=ROOT.kPink+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltCaloMET_')           , Legend='hltCaloMET'        , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFClusterMET_')      , Legend='hltPFClusterMET'   , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFMET_')             , Legend='hltPFMET'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFPuppiV4MET_')      , Legend='hltPFPuppiMET'+legTag, Color=ROOT.kRed)]

       elif 'hltAK4PFJets_' in key:
         baseColl = 'hltAK4PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJets_')     , Legend='hltAK4CaloJets'     , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFClusterJets_'), Legend='hltAK4PFClusterJets', Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJets_')       , Legend='hltAK4PFJets'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFPuppiJets_')  , Legend='hltAK4PFPuppiJets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK4PFJetsCorrected_' in key:
         baseColl = 'hltAK4PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4+JECs')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='offlineAK4PFPuppiJetsCorrected', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJetsCorrected_'), Legend='hltAK4CaloJetsCorrected', Color=ROOT.kGray+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJetsCorrected_'), Legend=legTag)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFPuppiJets_')  , Legend='hltAK4PFPuppiJets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJets_' in key:
         baseColl = 'hltAK8PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJets_')     , Legend='hltAK8CaloJets'          , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFClusterJets_'), Legend='hltAK8PFClusterJets'     , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJets_')       , Legend='hltAK8PFJets'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFPuppiJets_')  , Legend='hltAK8PFPuppiJets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJetsCorrected_' in key:
         baseColl = 'hltAK8PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8+JECs')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='offlineAK8PFPuppiJetsCorrected', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJetsCorrected_'), Legend='hltAK8CaloJetsCorrected', Color=ROOT.kGray+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJetsCorrected_'), Legend='hltAK8PFJetsCorrected'+legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFPuppiJets_'), Legend='hltAK8PFPuppiJets'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPF_' in key:
         baseColl = 'PF'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(w/o JECs)')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltCalo_')     , Legend='Calo'          , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFCluster_'), Legend='PFCluster'     , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPF_')       , Legend='PF'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFPuppi_')  , Legend='PFPuppi'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPFCorr_' in key:
         baseColl = 'PFCorr'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(+JECs)')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlPFPuppiCorr_') , Legend='OfflineCorr'       , Color=ROOT.kPink+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltCaloCorr_')     , Legend='CaloCorr'          , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFClusterCorr_'), Legend='PFClusterCorr'     , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFCorr_')       , Legend='PFCorr'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltPFPuppiCorr_')  , Legend='PFPuppiCorr'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

    ##
    ## keyword: run3_jme_compareTRK5
    ##
    elif keyword == 'run3_jme_compareTRK5':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       #cfg.legXY = [0.55, 0.60, 0.95, 0.90]
       cfg.legXY = [0.75, 0.70, 0.95, 0.90]

       ## MET
       if 'hltCaloMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCaloMET_', 'offlinePFMET_Raw_'), Legend='Offline PFMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltCaloMET [ '+inp['Legend']+' ]')]

       if 'hltCaloMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCaloMETTypeOne_', 'offlineCaloMET_Type1_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       if 'hltPFPuppiMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiMETTypeOne_', 'offlinePFPuppiMET_Type1_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       if 'hltPFClusterMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFClusterMETTypeOne_', 'offlinePFClusterMET_Type1_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltPFMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_'), Legend='Offline PFMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltPFMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMETTypeOne_', 'offlinePFMET_Type1_'), Legend='Offline',Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPF', 'hltPFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

       elif 'hltPFSoftKillerMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFSoftKillerMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline PFPuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFSoftKillerMET [ '+inp['Legend']+' ]')]

       elif 'hltPFPuppiV4MET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiV4MET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline PFPuppiMET', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFPuppiV3MET [ '+inp['Legend']+' ]')]

       ## Jets
       elif 'hltAK4PFJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline AK4PFPuppi', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltAK4PFJets [ '+inp['Legend']+' ]')]

       elif 'hltAK4PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltAK8PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PFJetsCorrected_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltAK4PFPuppiJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltAK8PFPuppiJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PFPuppiJetsCorrected_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltAK4CaloJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4CaloJetsCorrected_', 'offlineAK4CaloJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltAK8CaloJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8CaloJetsCorrected_', 'offlineAK8CaloJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltAK4PFClusterJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFClusterJetsCorrected_', 'offlineAK4PFClusterJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'hltAK8PFClusterJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PFClusterJetsCorrected_', 'offlineAK8PFClusterJetsCorrected_'), Legend='Offline', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend=inp['Legend'])]

       elif 'MatchedTohltPF_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPF_', 'offlPFPuppiCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPF'+' [ '+inp['Legend']+' ]')]

       elif 'MatchedTohltPFCorr_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFCorr_', 'offlPFPuppiCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFCorr'+' [ '+inp['Legend']+' ]')]

       elif 'MatchedTohltPFPuppi_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppi_', 'offlPFPuppiCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFPuppi'+' [ '+inp['Legend']+' ]')]

       elif 'MatchedTohltPFPuppiCorr_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiCorr_', 'offlPFPuppiCorr_'), Legend='OfflineCorr', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='hltPFPuppiCorr'+' [ '+inp['Legend']+' ]')]

    ###
    ### run3_jme_comparePF
    ###
    elif keyword == 'run3_jme_comparePF':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if key.endswith('_pt_eff'):
          cfg.xMin, cfg.xMax = 0., 300.

       cfg.legXY = [0.55, 0.60, 0.95, 0.90]

       ## MET
       if 'hltPFMET_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltPFMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Type1_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltPFPuppiMET_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltPFPuppiMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiMET_', 'offlinePFPuppiMET_Type1_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       ## Jets
       elif 'hltAK4PFJets_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK4PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK8PFJets_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PFJets_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK8PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'MatchedTohltPF_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline', Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'MatchedTohltPFCorr_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline', Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK4PFPuppiJets_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJets_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK4PFPuppiJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK8PFPuppiJets_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PFPuppiJets_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK8PFPuppiJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'MatchedTohltPFPuppi_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFPuppiCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline', Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'MatchedTohltPFPuppiCorr_' in key:
          for idx, inp in enumerate(inputList):
#            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFPuppiCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline', Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

    ###
    ### run3_jme_compareCaloVsPF
    ###
    elif keyword == 'run3_jme_compareCaloVsPF':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if key.endswith('_pt_eff'):
          cfg.xMin, cfg.xMax = 0., 300.

       if key.endswith('_eff'):
          cfg.legXY = [0.55, 0.30, 0.95, 0.50]
       else:
          cfg.legXY = [0.55, 0.60, 0.95, 0.80]

       ## MET
       if 'hltCaloMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltCaloMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       ## Jets
       elif 'hltAK4CaloJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4Calo', 'hltAK4PF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK4CaloJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4Calo', 'hltAK4PF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK8CaloJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8Calo', 'hltAK8PF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK8CaloJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8Calo', 'hltAK8PF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'MatchedTohltCalo_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'MatchedTohltCaloCorr_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

    ###
    ### run3_jme_comparePFVsPFPuppi
    ###
    elif keyword == 'run3_jme_comparePFVsPFPuppi':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if key.endswith('_pt_eff'):
          cfg.xMin, cfg.xMax = 0., 300.

#       cfg.legXY = [0.55, 0.60, 0.95, 0.90]
       if key.endswith('_eff'):
          cfg.legXY = [0.55, 0.30, 0.95, 0.50]
       else:
          cfg.legXY = [0.55, 0.60, 0.95, 0.80]

       ## MET
       if 'hltPFMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPF', 'hltPFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

       elif 'hltPFMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Type1_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPF', 'hltPFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

       ## Jets
       elif 'hltAK4PFJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PF', 'hltAK4PFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

       elif 'hltAK4PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PF', 'hltAK4PFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

       elif 'hltAK8PFJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PFJets_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PF', 'hltAK8PFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

       elif 'hltAK8PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8PF', 'hltAK8PFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

       elif 'MatchedTohltPF_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline', Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPF', 'hltPFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

       elif 'MatchedTohltPFCorr_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline', Color=ROOT.kPink+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPF', 'hltPFPuppi'), Legend='PF+PUPPI ('+inp['Legend']+')', Color=ROOT.kRed)]

    ###
    ### trig_review_2023
    ###
    elif keyword == 'trig_review_2023':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if key.endswith('_pt_eff'):
          cfg.xMin, cfg.xMax = 0., 300.

#       cfg.legXY = [0.55, 0.60, 0.95, 0.90]
       if key.endswith('_eff'):
          cfg.legXY = [0.55, 0.30, 0.95, 0.50]
       else:
          cfg.legXY = [0.55, 0.60, 0.95, 0.80]

       ## MET
       if 'hltPFMET_' in key:
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltPFMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       ## Jets
       elif 'hltAK4PFJets_' in key:
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK4PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK8PFJets_' in key:
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK8PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'MatchedTohltPF_' in key:
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'MatchedTohltPFCorr_' in key:
          for idx, inp in enumerate(inputList):
            #cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF ('+inp['Legend']+')', Color=inp['LineColor'])]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       ## MET
       if 'hltCaloMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltCaloMETTypeOne_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       ## Jets
       elif 'hltAK4CaloJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4Calo', 'hltAK4PF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK4CaloJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4Calo', 'hltAK4PF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK8CaloJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8Calo', 'hltAK8PF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'hltAK8CaloJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK8Calo', 'hltAK8PF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'MatchedTohltCalo_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

       elif 'MatchedTohltCaloCorr_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo ('+inp['Legend']+')', Color=ROOT.kOrange+1)]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCalo', 'hltPF'), Legend='PF ('+inp['Legend']+')', Color=ROOT.kViolet)]

    ##
    ## keyword: phase2_dqm_compareTRK
    ##
    elif keyword == 'phase2_dqm_compareTRK':

       if key.endswith('pfcand_particleId'):
          cfg.xLabelSize, cfg.xBinLabels = 0.2, ['X', 'h', 'e', '#mu', '#gamma', 'h0', 'h_HF', 'eg_HF']

       if key.endswith('_pt_2'):
          cfg.logY, cfg.xMin, cfg.xMax = True, 0., 300.

       cfg.legXY = [0.55, 0.60, 0.95, 0.90]

       if '_hltGeneralTracks' in key:
         cfg.objLabel = 'hltGeneralTracks'
         for inp in inputList:
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

       elif '_hltPrimaryVertices' in key:
         cfg.objLabel = 'hltPrimaryVertices'
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltPrimaryVertices', '_offlinePrimaryVertices'), Legend='offlinePrimaryVertices', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

       elif ('_hltParticleFlow/' in key) or ('_hltParticleFlow_' in key):
         cfg.objLabel = 'hltParticleFlow'
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_offlineParticleFlow'), Legend='Offline PF', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

       elif ('_hltPFPuppi/' in key) or ('_hltPFPuppi_' in key):
         cfg.objLabel = 'hltPFPuppi'
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

       elif ('_simPFProducer/' in key) or ('_simPFProducer_' in key):
         cfg.objLabel = 'simPFProducer'
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

       elif ('_pfTICL/' in key) or ('_pfTICL_' in key):
         cfg.objLabel = 'pfTICL'
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

    ##
    ## keyword: phase2_dqm_compareTRK2
    ##
    elif keyword == 'phase2_dqm_compareTRK2':

       if key.endswith('pfcand_particleId'):
          cfg.xLabelSize, cfg.xBinLabels = 0.2, ['X', 'h', 'e', '#mu', '#gamma', 'h0', 'h_HF', 'eg_HF']

       if key.endswith('_pt_2'):
          cfg.logY, cfg.xMin, cfg.xMax = True, 0., 300.

       skip_key = False
       for _pfTypeTag in ['_h', '_e', '_mu', '_gamma', '_h0']:
          if key_dirname.endswith(_pfTypeTag) and key_basename.startswith('pfcand_mult_') and (not key_basename.endswith(_pfTypeTag)):
             skip_key = True
             break
       if skip_key:
          return

       if ('_hltParticleFlow/' in key) or ('_hltParticleFlow_' in key):
        cfg.legXY = [0.55, 0.70, 0.99, 0.99]
        cfg.outputName = key.replace('_hltParticleFlow', '')
        for idx, inp in enumerate(inputList):
          legTag = '[ '+inp['Legend']+' ] '
          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_offlineParticleFlow'), Legend=       'Offline PF'     , Color=ROOT.kPink+1) if idx==0 else None]
          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_simPFProducer')      , Legend=legTag+'simPFProducer'  , Color=ROOT.kOrange+1)]
          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_pfTICL')             , Legend=legTag+'pfTICL'         , Color=ROOT.kBlue)]
          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltParticleFlow')    , Legend=legTag+'hltParticleFlow', Color=ROOT.kBlack)]
#         cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('_hltParticleFlow', '_hltPFPuppi')         , Legend=legTag+'hltPFPuppi'     , Color=ROOT.kRed)]

    ##
    ## keyword: phase2_jme_compareTRK1
    ##
    elif keyword == 'phase2_jme_compareTRK1':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.40, 0.95, 0.90]

       if 'hltPFPuppiMET_' in key:
         cfg.objLabel = cfg.objLabel.replace('hltPFPuppiMET', 'MET')+' [ '+inputList[0]['Legend']+' ]'
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_')     , Legend='Offline PF'     , Color=ROOT.kGreen+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline PFPuppi', Color=ROOT.kPink+1)]
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltCaloMET_')           , Legend='Calo'           , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFClusterMET_')      , Legend='PFCluster'      , Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFMET_')             , Legend='PF'             , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFSoftKillerMET_')   , Legend='SoftKiller'     , Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFCHSMET_')          , Legend='CHS'            , Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFPuppiMET_')        , Legend='PFPuppi'        , Color=ROOT.kOrange+1)]

       elif 'hltAK4PFJets_' in key:
         baseColl = 'hltAK4PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4Jets(Uncorr) [ '+inputList[0]['Legend']+' ]')
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJets_')     , Legend='Calo'     , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFClusterJets_'), Legend='PFCluster', Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJets_')       , Legend='PF'       , Color=ROOT.kBlack)]
         del baseColl

       elif 'hltAK4PFPuppiJetsCorrected_' in key:
         baseColl = 'hltAK4PFPuppiJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4JetsCorrected [ '+inputList[0]['Legend']+' ]')
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJetsCorrected_')         , Legend='PF'     , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSJetsCorrected_')      , Legend='CHS'    , Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFPuppiJetsCorrected_')    , Legend='PFPuppi', Color=ROOT.kRed)]
         del baseColl

       elif 'hltAK8PFJets_' in key:
         baseColl = 'hltAK8PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8Jets(Uncorr) [ '+inputList[0]['Legend']+' ]')
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJets_')     , Legend='Calo'     , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFClusterJets_'), Legend='PFCluster', Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJets_')       , Legend='PF'       , Color=ROOT.kBlack)]
         del baseColl

       elif 'hltAK8PFPuppiJetsCorrected_' in key:
         baseColl = 'hltAK8PFPuppiJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8JetsCorrected [ '+inputList[0]['Legend']+' ]')
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJetsCorrected_')         , Legend='PF'   , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSJetsCorrected_')      , Legend='CHS'  , Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFPuppiJetsCorrected_')    , Legend='PFPuppi', Color=ROOT.kRed)]
         del baseColl

       elif 'MatchedToPFPuppi_' in key:
         baseColl = 'PFPuppi'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(Uncorr) [ '+inputList[0]['Legend']+' ]')
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'Calo_')     , Legend='Calo'     , Color=ROOT.kGray+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCluster_'), Legend='PFCluster', Color=ROOT.kOrange+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PF_')       , Legend='PF'       , Color=ROOT.kBlack)]
         del baseColl

       elif 'MatchedToPFPuppiCorr_' in key:
         baseColl = 'PFPuppiCorr'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(Corr) [ '+inputList[0]['Legend']+' ]')
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCorr_')     , Legend='PF'     , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSCorr_')  , Legend='CHS'    , Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFPuppiCorr_'), Legend='PFPuppi', Color=ROOT.kRed)]
         del baseColl

    ##
    ## keyword: phase2_jme_compareTRK1_withL1T
    ##
    elif keyword == 'phase2_jme_compareTRK1_withL1T':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.40, 0.95, 0.90]

       if 'hltPFMET_' in key:
         cfg.objLabel = cfg.objLabel.replace('hltPFMET', 'MET')+' [ '+inputList[0]['Legend']+' ]'
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'l1tCaloMET_')         , Legend='L1T Calo'       , Color=ROOT.kGray)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'l1tPFMET_')           , Legend='L1T PF'         , Color=ROOT.kGreen+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'l1tPFPuppiMET_')        , Legend='L1T PFPuppi'      , Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFMET_')           , Legend='HLT PF'         , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFPuppiMET_')        , Legend='HLT PFPuppi'      , Color=ROOT.kOrange+1)]

       elif 'hltAK4PFJetsCorrected_' in key:
         baseColl = 'hltAK4PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4JetsCorrected [ '+inputList[0]['Legend']+' ]')
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'l1tAK4CaloJetsCorrected_')     , Legend='L1T Calo'       , Color=ROOT.kGray)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'l1tAK4PFJetsCorrected_')       , Legend='L1T PF'         , Color=ROOT.kGreen+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'l1tAK4PFPuppiJetsCorrected_')  , Legend='L1T PFPuppi'    , Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJetsCorrected_')       , Legend='HLT PF'         , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFPuppiJetsCorrected_')  , Legend='HLT PFPuppi'    , Color=ROOT.kOrange+1)]
         del baseColl

       elif 'MatchedToPFCorr_' in key:
         baseColl = 'PFCorr'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(Corr) [ '+inputList[0]['Legend']+' ]')
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'L1TCaloCorr_')     , Legend='L1T Calo'       , Color=ROOT.kGray)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'L1TPFCorr_')       , Legend='L1T PF'         , Color=ROOT.kGreen+2)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'L1TPFPuppiCorr_')    , Legend='L1T PFPuppi'      , Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCorr_')          , Legend='HLT PF'         , Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFPuppiCorr_')       , Legend='HLT PFPuppi'      , Color=ROOT.kOrange+1)]
         del baseColl

    ##
    ## keyword: phase2_jme_compareTRK1_onlyMET
    ##
    elif keyword == 'phase2_jme_compareTRK1_onlyMET':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.70, 0.95, 0.90]

       if 'hltPFPuppiMET_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT PF+Puppi, Raw', Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiMET_', 'hltPFPuppiMETTypeOne_'), Legend='HLT PF+Puppi, Type-1', Color=ROOT.kRed)]

    ##
    ## keyword: phase2_jme_compareTRK2
    ##
    elif keyword == 'phase2_jme_compareTRK2':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.40, 0.95, 0.90]

       if 'hltPFMET_' in key:
         cfg.objLabel = cfg.objLabel.replace('hltPFMET', 'MET')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_')     , Legend='Offline PF'       , Color=ROOT.kGreen+2)  if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline PFPuppi'  , Color=ROOT.kPink+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFClusterMET_')      , Legend='PFCluster'        , Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFMET_')             , Legend='PF'        +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFSoftKillerMET_')   , Legend='SoftKiller'+legTag, Color=ROOT.kViolet)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFCHSMET_')          , Legend='CHS'       +legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'hltPFPuppiMET_')        , Legend='PFPuppi'   +legTag, Color=ROOT.kRed)]

       elif 'hltAK4PFJets_' in key:
         baseColl = 'hltAK4PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4Jets')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4CaloJets_')     , Legend='Calo'     , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFClusterJets_'), Legend='PFCluster', Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJets_')       , Legend='PF'+legTag, Color=ROOT.kBlack)]
         del baseColl, legTag

       elif 'hltAK4PFJetsCorrected_' in key:
         baseColl = 'hltAK4PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK4JetsCorrected')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFJetsCorrected_')         , Legend='PF'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFCHSJetsCorrected_')      , Legend='CHS'    +legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK4PFPuppiJetsCorrected_')    , Legend='PFPuppi'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'hltAK8PFJets_' in key:
         baseColl = 'hltAK8PFJets'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8Jets')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8CaloJets_')     , Legend='Calo'     , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFClusterJets_'), Legend='PFCluster', Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJets_')       , Legend='PF'+legTag, Color=ROOT.kBlack)]
         del baseColl, legTag

       elif 'hltAK8PFJetsCorrected_' in key:
         baseColl = 'hltAK8PFJetsCorrected'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'AK8JetsCorrected')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK8PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFJetsCorrected_')         , Legend='PF'     +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFCHSJetsCorrected_')      , Legend='CHS'    +legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'hltAK8PFPuppiJetsCorrected_')    , Legend='PFPuppi'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

       elif 'MatchedToPF_' in key:
         baseColl = 'PF'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(Uncorr)')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'Calo_')     , Legend='Calo'     , Color=ROOT.kGray+1)   if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCluster_'), Legend='PFCluster', Color=ROOT.kOrange+2) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PF_')       , Legend='PF'+legTag, Color=ROOT.kBlack)]
         del baseColl, legTag

       elif 'MatchedToPFCorr_' in key:
         baseColl = 'PFCorr'
         cfg.objLabel = cfg.objLabel.replace(baseColl, 'Reco(Corr)')
         for idx, inp in enumerate(inputList):
           legTag = ' [ '+inp['Legend']+' ]'
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)' , Color=ROOT.kPink+1) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCorr_')          , Legend='PFCorr'   +legTag, Color=ROOT.kBlack)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFCHSCorr_')       , Legend='PFCHSCorr'+legTag, Color=ROOT.kBlue)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'PFPuppiCorr_')       , Legend='PFPuppiCorr'+legTag, Color=ROOT.kRed)]
         del baseColl, legTag

    ##
    ## keyword: phase2_jme_compareTRK5
    ##
    elif keyword == 'phase2_jme_compareTRK5':

#       if ('_wrt_' not in key_basename) and (not key_basename.endswith('_eff')) and \
#          (not ('MET' in key_basename and key_basename.endswith('_pt'))) and \
#          ('pt_over' not in key_basename):
#          return

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       cfg.legXY = [0.55, 0.60, 0.95, 0.90]

       ## MET
       if 'hltCaloMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltCaloMET_', 'offlinePFMET_Raw_'), Legend='Offline (PF)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='Calo [ '+inp['Legend']+' ]')]

       elif 'hltPFMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_'), Legend='Offline (PF)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF [ '+inp['Legend']+' ]')]

       elif 'hltPFSoftKillerMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFSoftKillerMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='SoftKiller [ '+inp['Legend']+' ]')]

       elif 'hltPFCHSMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFCHSMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='CHS [ '+inp['Legend']+' ]')]

       elif 'hltPFPuppiMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFPuppi [ '+inp['Legend']+' ]')]

       ## Jets
       elif 'hltAK4PFJets_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJets_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF [ '+inp['Legend']+' ]')]

       elif 'hltAK4PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF [ '+inp['Legend']+' ]')]

       elif 'hltAK4PFCHSJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFCHSJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='CHS [ '+inp['Legend']+' ]')]

       elif 'hltAK4PFPuppiJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFPuppi [ '+inp['Legend']+' ]')]

       elif 'MatchedToPF_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PF_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PF [ '+inp['Legend']+' ]')]

       elif 'MatchedToPFCorr_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFCorr [ '+inp['Legend']+' ]')]

       elif 'MatchedToPFCHS_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCHS_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFCHS [ '+inp['Legend']+' ]')]

       elif 'MatchedToPFCHSCorr_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCHSCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFCHSCorr [ '+inp['Legend']+' ]')]

       elif 'MatchedToPFPuppi_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFPuppi_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFPuppi [ '+inp['Legend']+' ]')]

       elif 'MatchedToPFPuppiCorr_' in key:
         for idx, inp in enumerate(inputList):
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFPuppiCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)', Color=ROOT.kBlack) if idx==0 else None]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='PFPuppiCorr [ '+inp['Legend']+' ]')]

    ##
    ## keyword: phase2_jme_comparePFPuppi
    ##
    elif keyword == 'phase2_jme_comparePFPuppi':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if key.endswith('_pt_eff'):
          cfg.xMin, cfg.xMax = 0., 300.

       cfg.legXY = [0.55, 0.60, 0.95, 0.90]

       ## MET
       if 'l1tPFPuppiMET_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='L1T ('+inp['Legend']+')')]

       elif 'hltPFPuppiMET_' in key:
          for idx, inp in enumerate(inputList):
#!!            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiMET_', 'offlinePFPuppiMET_Raw_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
#           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFPuppiMET_', 'l1tPFPuppiMET_'), Legend='L1T', Color=ROOT.kGreen+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltPFMET_' in key:
          for idx, inp in enumerate(inputList):
#!!            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'offlinePFMET_Raw_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
#           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltPFMET_', 'l1tPFMET_'), Legend='L1T', Color=ROOT.kGreen+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       ## Jets
       elif 'l1tSlwPFPuppiJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='L1T ('+inp['Legend']+')')]

       elif 'MatchedTol1tPFPuppiCorr_' in key:
          for idx, inp in enumerate(inputList):
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='L1T ('+inp['Legend']+')')]

       elif 'hltAK4PFPuppiJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
#!!            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
#           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJetsCorrected_', 'l1tAK4PFPuppiJetsCorrected_'), Legend='L1T', Color=ROOT.kGreen+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK8PFPuppiJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
#!!            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJetsCorrected_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
#           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFPuppiJetsCorrected_', 'l1tAK4PFPuppiJetsCorrected_'), Legend='L1T', Color=ROOT.kGreen+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'MatchedTohltPFPuppiCorr_' in key:
          for idx, inp in enumerate(inputList):
#!!            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFPuppiCorr_', 'OfflinePFPuppiCorr_'), Legend='Offline', Color=ROOT.kPink+1) if idx==0 else None]
#           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFPuppiCorr_', 'L1TPFPuppiCorr_'), Legend='L1T', Color=ROOT.kGreen+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'hltAK4PFJetsCorrected_' in key:
          for idx, inp in enumerate(inputList):
#!!            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'offlineAK4PFJetsCorrected_'), Legend='Offline',Color=ROOT.kPink+1) if idx==0 else None]
#           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('hltAK4PFJetsCorrected_', 'l1tAK4PFJetsCorrected_'), Legend='L1T', Color=ROOT.kGreen+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

       elif 'MatchedTohltPFCorr_' in key:
          for idx, inp in enumerate(inputList):
#!!            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCorr_', 'OfflinePFCorr_'), Legend='Offline', Color=ROOT.kPink+1) if idx==0 else None]
#           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace('PFCorr_', 'L1TPFCorr_'), Legend='L1T', Color=ROOT.kGreen+1) if idx==0 else None]
            cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key, Legend='HLT ('+inp['Legend']+')')]

    ##
    ## keyword: phase2_jme_compareL1T
    ##
    elif keyword == 'phase2_jme_compareL1T':

       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return

       if 'MHT' in key:
          return

       cfg.legXY = [0.25, 0.70, 0.75, 0.95]

       if 'l1tAK4PFPuppiJetsCorrected_' in key:
         baseColl = 'l1tAK4PFPuppiJetsCorrected'
         cfg.objLabel = ''
         for idx, inp in enumerate(inputList):
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'offlineAK4PFPuppiJetsCorrected_'), Legend='Offline (PFPuppi)', Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'l1tAK4PFPuppiJetsCorrected_')  , Legend='L1T PFPuppi (AK4)'  , Color=ROOT.kRed)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'l1tSlwPFPuppiJetsCorrected_')  , Legend='L1T PFPuppi (7x7h)' , Color=ROOT.kBlue)]
         del baseColl

       elif 'MatchedToL1TPFPuppiCorr2_' in key:
         baseColl = 'PFPuppiCorr2'
         cfg.objLabel = ''
         for idx, inp in enumerate(inputList):
#          cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'OfflinePFPuppiCorr_'), Legend='Offline (PFPuppi)' , Color=ROOT.kPink+1)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'L1TPFPuppiCorr2_')   , Legend='L1T PFPuppi (AK4)' , Color=ROOT.kRed)]
           cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key.replace(baseColl+'_', 'L1TPFPuppiCorr_')    , Legend='L1T PFPuppi (7x7h)', Color=ROOT.kBlue)]
         del baseColl

    ##
    ## keyword: phase2_jme_compare
    ##
    elif keyword == 'phase2_jme_compare':
       if ('/' in key) and (not key.startswith('NoSelection/')):
          if ('_pt0' not in key_basename) or key_basename.endswith('pt0_eff') or \
             key_basename.endswith('pt0') or ('pt0_over' in key_basename):
             return
       cfg.legXY = [0.50, 0.70, 0.95, 0.90]

       for idx, inp in enumerate(inputList):
         cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

    ##
    ## keyword: jme_compare (compare each distribution across different inputs)
    ##
    elif keyword == 'jme_compare':
       if key.endswith('jet_pt'):
          cfg.logY = True
       cfg.legXY = [0.50, 0.70, 0.95, 0.90]
       for idx, inp in enumerate(inputList):
         cfg.hists += [getHistogram(plotCfg=cfg, inputDict=inp, key=key)]

    else:
       KILL('getPlotConfig(key="'+key+'", keyword="'+keyword+'") -- invalid keyword: "'+keyword+'"')

    # remove None entries
    cfg.hists = list(filter(None, cfg.hists))

    if len(cfg.hists) < 1:
       return None

    usedDivideByBinWidth = False

    if not (cfg.IsProfile or cfg.IsEfficiency):
       for cfg_h in cfg.hists:
          if cfg_h.th1.GetName().endswith('_cumul'):
             continue

          divideByBinWidth = False
          _tmpBW = None
          for _tmp in range(1, cfg_h.th1.GetNbinsX()+1):
              if _tmpBW is None:
                 _tmpBW = cfg_h.th1.GetBinWidth(_tmp)
              elif (abs(_tmpBW-cfg_h.th1.GetBinWidth(_tmp))/max(abs(_tmpBW), abs(cfg_h.th1.GetBinWidth(_tmp)))) > 1e-4:
                 divideByBinWidth = True
                 break
          if divideByBinWidth:
             cfg_h.th1.Scale(1., 'width')
             usedDivideByBinWidth = True

          normalizedToUnity = True
          if normalizedToUnity:
             cfg_h.th1.Scale(1. / cfg_h.th1.Integral())

    if usedDivideByBinWidth:
       cfg.titleY += ' / Bin width'

    return cfg

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', nargs='+', default=[], required=True,
                       help='list of input files [format: "PATH:LEGEND:LINECOLOR:LINESTYLE:MARKERSTYLE:MARKERCOLOR:MARKERSIZE"]')

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                       help='path to output directory')

   parser.add_argument('-k', '--keywords', dest='keywords', nargs='+', default=[], required=True,
                       help='keywords for plot configuration')

   parser.add_argument('-m', '--matches', dest='matches', nargs='+', default=[],
                       help='list of matching-patterns to skim input histograms (input is a match if its name matches any of the specified patterns)')

   parser.add_argument('-s', '--skip', dest='skip', nargs='+', default=[],
                       help='list of matching-patterns to skip input histograms (input is skipped if its name matches any of the specified patterns)')

   parser.add_argument('-l', '--label', dest='label', action='store', default='',
                       help='text label (displayed in top-left corner)')

   parser.add_argument('-u', '--upgrade', dest='upgrade', action='store_true', default=False,
                       help='labels for Phase-2 plots')

   parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['png'],
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

   MATCHES = sorted(list(set(opts.matches)))
   MATCHES = [_tmp.replace('\'','').replace('"','') for _tmp in MATCHES]

   SKIP = sorted(list(set(opts.skip)))
   SKIP = [_tmp.replace('\'','').replace('"','') for _tmp in SKIP]

   EXTS = list(set(opts.exts))
   ### -------------------

   inputList = []
   th1Keys = []
   for _input in opts.inputs:
       _input_pieces = _input.split(':')
       if len(_input_pieces) >= 3:
          print ('reading..', os.path.relpath(_input_pieces[0]))
          _tmp = {}
          _tmp['TH1s'] = getTH1sFromTFile(_input_pieces[0], matches=MATCHES, skip=SKIP, verbose=(opts.verbosity > 20))
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

   theStyle = get_style(0)
   theStyle.cd()

   ROOT.TGaxis.SetMaxDigits(4)

   Top = ROOT.gStyle.GetPadTopMargin()
   Rig = ROOT.gStyle.GetPadRightMargin()
   Bot = ROOT.gStyle.GetPadBottomMargin()
   Lef = ROOT.gStyle.GetPadLeftMargin()

   ROOT.TGaxis.SetExponentOffset(-Lef+.50*Lef, 0.03, 'y')

   label_sample = get_text(Lef+(1-Lef-Rig)*0.00, (1-Top)+Top*0.25, 11, .032, opts.label)

   for _hkey in th1Keys:

       for _keyw in KEYWORDS:

           _plotConfig = getPlotConfig(key=_hkey, keyword=_keyw, inputList=inputList)

           if _plotConfig is None:
              continue

           ## labels and axes titles
           label_obj = get_text(Lef+(1-Rig-Lef)*0.95, Bot+(1-Top-Bot)*0.925, 31, .035, _plotConfig.objLabel)
           _labels = [label_sample, label_obj]

           _htitle = ';'+_plotConfig.titleX+';'+_plotConfig.titleY

           ## plot
           plot(**{
             'histograms': _plotConfig.hists,
             'title': _htitle,
             'labels': _labels,
             'legXY': [Lef+(1-Rig-Lef)*_plotConfig.legXY[0], Bot+(1-Bot-Top)*_plotConfig.legXY[1], Lef+(1-Rig-Lef)*_plotConfig.legXY[2], Bot+(1-Bot-Top)*_plotConfig.legXY[3]],
             'outputs': [OUTDIR+'/'+_plotConfig.outputName+'.'+_tmp for _tmp in EXTS],
             'ratio': _plotConfig.ratio,
             'logX': _plotConfig.logX,
             'logY': _plotConfig.logY,
             'xMin': _plotConfig.xMin,
             'xMax': _plotConfig.xMax,
             'yMin': _plotConfig.yMin,
             'yMax': _plotConfig.yMax,
             'autoRangeX': _plotConfig.autoRangeX,
             'xLabelSize': _plotConfig.xLabelSize,
             'xBinLabels': _plotConfig.xBinLabels,
           })

           del _plotConfig
