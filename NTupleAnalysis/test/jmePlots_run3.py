#!/usr/bin/env python3
import argparse
import os
import ROOT

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

JET_CATEGORIES = [
  '_EtaIncl',
  '_HB',
  '_HE1',
  '_HE2',
  '_HF',
]

def clone_histogram(histograms, tag1, tag2, setters={}):

    if tag1 not in histograms:
       return None

    if tag2 not in histograms[tag1]:
       return None

    h0 = histograms[tag1][tag2].Clone()
    h0.UseCurrentStyle()
    h0.SetDirectory(0)

    h0 = th1_mergeUnderflowBinIntoFirstBin(h0)
    h0 = th1_mergeOverflowBinIntoLastBin(h0)

    # defaults
    h0.SetMarkerSize(0)
    h0.SetLineWidth(2)

    for i_set in setters:
        if hasattr(h0, 'Set'+i_set):
           getattr(h0, 'Set'+i_set)(setters[i_set])

    return h0

def clone_graph(graphs, tag1, tag2, setters={}, verbose=False):

    if tag1 not in graphs:
       if verbose: WARNING('clone_graph -- will skip graphs["'+tag1+'"]["'+tag2+'"] (key "'+tag1+'" not found')
       return None

    if tag2 not in graphs[tag1]:
       if verbose: WARNING('clone_graph -- will skip graphs["'+tag1+'"]["'+tag2+'"] (key "'+tag2+'" not found')
       return None

    g0 = graphs[tag1][tag2].Clone()
    g0.UseCurrentStyle()
#    g0.SetDirectory(0)

    g0.SetMarkerSize(0)

    for i_set in setters:
        if hasattr(g0, 'Set'+i_set):
           getattr(g0, 'Set'+i_set)(setters[i_set])

    return g0

def updateDictionary(dictionary, TDirectory, prefix='', verbose=False):

    key_prefix = ''
    if len(prefix) > 0: key_prefix = prefix+'/'

    for j_key in TDirectory.GetListOfKeys():

        j_key_name = j_key.GetName()

        j_obj = TDirectory.Get(j_key_name)

        if j_obj.InheritsFrom('TDirectory'):

           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name, verbose=verbose)

        elif j_obj.InheritsFrom('TH1'):

           out_key = key_prefix+j_key_name

           if out_key in dictionary:
              KILL(log_prx+'input error -> found duplicate of template ["'+out_key+'"] in input file: '+TDirectory.GetName())

           dictionary[out_key] = j_obj.Clone()
           dictionary[out_key].SetDirectory(0)

           if verbose:
              print (colored_text('[input]', ['1','92']), out_key)

    return dictionary

def getTH1sFromTFile(path, verbose=False):

    input_histos_dict = {}

    i_inptfile = ROOT.TFile.Open(path)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return input_histos_dict

    updateDictionary(input_histos_dict, i_inptfile, prefix='', verbose=verbose)

    i_inptfile.Close()

    return input_histos_dict

class Histogram:
    def __init__(self):
        self.th1 = None
        self.draw = ''
        self.legendName = ''
        self.legendDraw = ''

def plot(canvas, output_extensions, stickers, output, templates, title, legXY=[], divideByBinWidth=False, normalizedToUnity=False, xMin=None, xMax=None, yMin=None, yMax=None, logX=False, logY=False,ratio=False):

    h0 = None

    plot_histograms = []

    nvalid_histograms = 0

    for _tmp in templates:

        histo = Histogram()
        histo.th1 = _tmp['TH1']
        histo.draw = _tmp['draw']
        histo.legendName = _tmp['legendName']
        histo.legendDraw = _tmp['legendDraw']

        if histo.th1 is not None:

           nvalid_histograms += 1

           histo.draw = histo.draw + bool(histo.th1.InheritsFrom('TH1'))*',same'

           if h0 is None: h0 = histo.th1

           histo.th1.SetBit(ROOT.TH1.kNoTitle)

           if hasattr(histo.th1, 'SetStats'):
              histo.th1.SetStats(0)

           if divideByBinWidth:
              histo.th1.Scale(1., 'width')

           if normalizedToUnity:
              histo.th1.Scale(1. / histo.th1.Integral())

        plot_histograms += [histo]

    if h0 is None:
       return 1

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
       for _tmp in plot_histograms:
           if _tmp.th1 is not None:
              leg.AddEntry(_tmp.th1, _tmp.legendName, _tmp.legendDraw)

    canvas.cd()

    XMIN, XMAX = xMin, xMax
    if XMIN is None: XMIN = h0.GetBinLowEdge(1)
    if XMAX is None: XMAX = h0.GetBinLowEdge(1+h0.GetNbinsX())

    HMAX = 0.0
    for _tmp in plot_histograms:
        if (_tmp.th1 is not None) and hasattr(_tmp.th1, 'GetNbinsX'):
           for i_bin in range(1, _tmp.th1.GetNbinsX()+1):
               HMAX = max(HMAX, (_tmp.th1.GetBinContent(i_bin) + _tmp.th1.GetBinError(i_bin)))

    YMIN, YMAX = yMin, yMax
    if YMIN is None: YMIN = .0003 if logY else .0001
    if YMAX is None: YMAX = .0003*((HMAX/.0003)**(1./.85)) if logY else .0001+((HMAX-.0001) *(1./.85))

    h0 = canvas.DrawFrame(XMIN, YMIN, XMAX, YMAX)

    if not ratio or (nvalid_histograms == 1):

       canvas.SetTickx()
       canvas.SetTicky()

       canvas.SetLogx(logX)
       canvas.SetLogy(logY)

       for _tmp in plot_histograms:
           if _tmp.th1 is not None:
              _tmp.th1.Draw(_tmp.draw)

       h0.Draw('axis,same')
       h0.SetTitle(title)
#       h0.GetXaxis().SetRangeUser(XMIN, XMAX)
#       h0.GetYaxis().SetRangeUser(YMIN, YMAX)

       if leg: leg.Draw('same')

       for _tmp in stickers:
           if hasattr(_tmp, 'Draw'):
              _tmp.Draw('same')

    else:
       pad1H = 0.7

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

       h11 = None
       for _tmp in plot_histograms:
           if _tmp.th1 is not None:
              if h11 is None: h11 = _tmp.th1
              _tmp.th1.Draw(_tmp.draw)

       if not h11: return 1

       h11.Draw('axis,same')
       h11.GetXaxis().SetTitle('')
       h11.GetYaxis().SetTitle(title.split(';')[2])
       h11.GetXaxis().SetRangeUser(XMIN, XMAX)

       h11.GetYaxis().SetTitleSize(h11.GetYaxis().GetTitleSize()/pad1H)
       h11.GetYaxis().SetTitleOffset(h11.GetYaxis().GetTitleOffset()*pad1H)
       h11.GetXaxis().SetLabelSize(0)
       h11.GetYaxis().SetLabelSize (h11.GetYaxis().GetLabelSize() /pad1H)
       h11.GetXaxis().SetTickLength(h11.GetXaxis().GetTickLength()/pad1H)

       if YMIN is None: YMIN = .0003 if logY else .0001
       if YMAX is None: YMAX = .0003*((HMAX/.0003)**(1./.85)) if logY else .0001+((HMAX-.0001) *(1./.85))

       h11.GetYaxis().SetRangeUser(YMIN, YMAX)

       if leg:
          leg.Draw('same')
          pad1.Update()
          leg.SetY1NDC(1.-(1.-leg.GetY1NDC())/pad1H)
          leg.SetY2NDC(1.-(1.-leg.GetY2NDC())/pad1H)

       stickers2 = []
       for _tmp in stickers:
           if hasattr(_tmp, 'Clone'):
              _tmp2 = _tmp.Clone()
              stickers2 += [_tmp2]

       for _tmp in stickers2:
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
       for _tmp in range(0, denom.GetNbinsX()+2): denom.SetBinError(_tmp, 0.)

       h21 = None

       plot_ratios = []

       for _tmp in plot_histograms:

           histo = Histogram()
           if _tmp.th1 is not None:
              histo.th1 = _tmp.th1.Clone()
              histo.th1.Divide(denom)

           histo.draw = _tmp.draw
           if 'same' not in histo.draw: histo.draw += ',same'

           histo.legendName = _tmp.legendName
           histo.legendDraw = _tmp.legendDraw

           if hasattr(histo.th1, 'SetStats'):
              histo.th1.SetStats(0)

           if h21 is None: h21 = histo.th1

           plot_ratios += [histo]

       ROOT.SetOwnership(pad2, False)

       pad2.cd()

       h21.SetFillStyle(3017)
       h21.SetFillColor(16)

       h21.GetXaxis().SetTitle(title.split(';')[1])
       h21.GetYaxis().SetTitle('Ratio')
       h21.GetYaxis().CenterTitle()
       h21.GetXaxis().SetTitleSize(h21.GetXaxis().GetTitleSize()/(1-pad1H))
       h21.GetYaxis().SetTitleSize(h21.GetYaxis().GetTitleSize()/(1-pad1H)*pad1H)
       h21.GetXaxis().SetTitleOffset(h21.GetXaxis().GetTitleOffset())
       h21.GetYaxis().SetTitleOffset(h21.GetYaxis().GetTitleOffset()*(1-pad1H)/pad1H)
       h21.GetXaxis().SetLabelSize(h21.GetYaxis().GetLabelSize()/(1-pad1H)*pad1H)
       h21.GetYaxis().SetLabelSize(h21.GetYaxis().GetLabelSize()/(1-pad1H)*pad1H)
       h21.GetXaxis().SetTickLength(h21.GetXaxis().GetTickLength()/(1-pad1H)*pad1H)
       h21.GetXaxis().SetLabelOffset(h21.GetXaxis().GetLabelOffset()/(1-pad1H))
       h21.GetYaxis().SetLabelOffset(h21.GetYaxis().GetLabelOffset())
       h21.GetYaxis().SetNdivisions(404)

       h21.GetXaxis().SetRangeUser(XMIN, XMAX)

       h2max, h2min = None, None
       for _tmp in plot_ratios:

           if _tmp.th1 is None: continue

           for _tmpb in range(1, _tmp.th1.GetNbinsX()+1):

               h2max = max(h2max, _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)) if h2max is not None else _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)
               h2min = min(h2min, _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)) if h2min is not None else _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)

       if (h2max is not None) and (h2min is not None):
          h2min = min(int(h2min*101.)/100., int(h2min*99.)/100.)
          h2max = max(int(h2max*101.)/100., int(h2max*99.)/100.)

          h21.GetYaxis().SetRangeUser(h2min, h2max)

       h21.Draw('e2')
       for _tmp in plot_ratios:
           if _tmp.th1 == h21: continue
           if _tmp.th1 is not None:
              _tmp.th1.Draw(_tmp.draw)
       h21.Draw('axis,same')

    canvas.cd()
    canvas.Update()

    output_basename_woExt = str(output)

    output_dirname = os.path.dirname(output_basename_woExt)
    if not os.path.isdir(output_dirname):
       EXE('mkdir -p '+output_dirname)

    for i_ext in output_extensions:
        out_file = output_basename_woExt+'.'+i_ext
        canvas.SaveAs(out_file)

        print colored_text('[file]', ['1','95']), os.path.relpath(out_file))

    canvas.Close()

    return 0

def get_templates_PU(key, histograms, var, skipGEN=False):

    the_templates = []

    if key == '3PU':
       the_templates += [
         {'TH1': clone_histogram(histograms, 'NoPU' , var, {'LineColor': 1}), 'draw': 'hist,e0', 'legendName': 'NoPU' , 'legendDraw': 'l'},
         {'TH1': clone_histogram(histograms, 'PU140', var, {'LineColor': 4}), 'draw': 'hist,e0', 'legendName': 'PU140', 'legendDraw': 'l'},
         {'TH1': clone_histogram(histograms, 'PU200', var, {'LineColor': 2}), 'draw': 'hist,e0', 'legendName': 'PU200', 'legendDraw': 'l'},
       ]

    elif key == '3PU_p':
       the_templates += [
         {'TH1': clone_histogram(histograms, 'NoPU' , var, {'MarkerSize': 1.5, 'MarkerStyle': 20, 'MarkerColor': 1, 'LineColor': 1}), 'draw': 'ep', 'legendName': 'NoPU' , 'legendDraw': 'ep'},
         {'TH1': clone_histogram(histograms, 'PU140', var, {'MarkerSize': 1.5, 'MarkerStyle': 22, 'MarkerColor': 4, 'LineColor': 4}), 'draw': 'ep', 'legendName': 'PU140', 'legendDraw': 'ep'},
         {'TH1': clone_histogram(histograms, 'PU200', var, {'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': 2, 'LineColor': 2}), 'draw': 'ep', 'legendName': 'PU200', 'legendDraw': 'ep'},
       ]

    the_templates_skimmed = []
    for _tmp in the_templates:
        if skipGEN and (_tmp['TH1'] is not None):
           if 'gen' in _tmp['TH1'].GetName().lower():
              continue
        the_templates_skimmed += [_tmp]

    return the_templates_skimmed

def get_templates(key, histograms, PU_tag, directory, var, skipGEN=False):

    the_templates = []

    if key.endswith('_p'):

       opt_draw = 'ep'
       opt_legDraw = 'ep'

       style_dict = {

         'ak4GenJetsNoNu': {'LineColor': 1, 'MarkerSize': 1.5, 'MarkerStyle': 27, 'MarkerColor': 1},
         'hltAK4PFJetsCorrected': {'LineColor': ROOT.kBlue, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kBlue},
         'hltAK4PFCHSJetsCorrected': {'LineColor': ROOT.kOrange+1, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kOrange+1},
         'hltAK4PuppiJetsCorrected': {'LineColor': ROOT.kViolet, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kViolet},
         'offlineAK4PFCHSJetsCorrected': {'LineColor': ROOT.kOrange+1, 'MarkerSize': 1.5, 'MarkerStyle': 20, 'MarkerColor': ROOT.kOrange+1},
         'offlineAK4PuppiJetsCorrected': {'LineColor': ROOT.kViolet, 'MarkerSize': 1.5, 'MarkerStyle': 20, 'MarkerColor': ROOT.kViolet},

         'ak8GenJetsNoNu': {'LineColor': 1, 'MarkerSize': 1.5, 'MarkerStyle': 27, 'MarkerColor': 1},
         'hltAK8PFJetsCorrected': {'LineColor': ROOT.kBlue, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kBlue},
         'hltAK8PFCHSJetsCorrected': {'LineColor': ROOT.kOrange+1, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kOrange+1},
         'hltAK8PuppiJetsCorrected': {'LineColor': ROOT.kViolet, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kViolet},
         'offlineAK8PuppiJetsCorrected': {'LineColor': ROOT.kViolet, 'MarkerSize': 1.5, 'MarkerStyle': 20, 'MarkerColor': ROOT.kViolet},

         'genMETCalo': {'LineColor': 1, 'MarkerSize': 1.5, 'MarkerStyle': 27, 'MarkerColor': 1},
         'genMETTrue': {'LineColor': 1, 'MarkerSize': 1.5, 'MarkerStyle': 27, 'MarkerColor': 1},
         'hltPFMET': {'LineColor': ROOT.kOrange+1, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kOrange+1},
         'hltPFMETNoMu': {'LineColor': ROOT.kOrange+1, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kOrange+1},
         'hltPFMETTypeOne': {'LineColor': ROOT.kRed, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kRed},
         'hltPuppiMET': {'LineColor': ROOT.kAzure, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kAzure},
         'hltPuppiMETNoMu': {'LineColor': ROOT.kAzure, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kAzure},
         'hltPuppiMETTypeOne': {'LineColor': ROOT.kViolet, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kViolet},
         'hltPuppiMETWithPuppiForJets': {'LineColor': ROOT.kCyan, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kCyan},
         'hltPFMETCHS': {'LineColor': ROOT.kGray+1, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kGray+1},
         'hltPFMETSoftKiller': {'LineColor': ROOT.kPink+1, 'LineStyle': 2, 'MarkerSize': 1.5, 'MarkerStyle': 24, 'MarkerColor': ROOT.kPink+1},
         'offlineMETs_Raw': {'LineColor': ROOT.kOrange+1, 'MarkerSize': 1.5, 'MarkerStyle': 20, 'MarkerColor': ROOT.kOrange+1},
         'offlineMETs_Type1': {'LineColor': ROOT.kRed, 'MarkerSize': 1.5, 'MarkerStyle': 20, 'MarkerColor': ROOT.kRed},
         'offlineMETsPuppi_Raw': {'LineColor': ROOT.kAzure, 'MarkerSize': 1.5, 'MarkerStyle': 20, 'MarkerColor': ROOT.kAzure},
         'offlineMETsPuppi_Type1': {'LineColor': ROOT.kViolet, 'MarkerSize': 1.5, 'MarkerStyle': 20, 'MarkerColor': ROOT.kViolet},
       }

    else:

       opt_draw = 'hist,e0'
       opt_legDraw = 'l'

       style_dict = {

         'ak4GenJetsNoNu': {'LineColor': 1},
         'hltAK4PFJetsCorrected': {'LineColor': ROOT.kBlue, 'LineStyle': 2},
         'hltAK4PFCHSJetsCorrected': {'LineColor': ROOT.kOrange+1, 'LineStyle': 2},
         'hltAK4PuppiJetsCorrected': {'LineColor': ROOT.kViolet, 'LineStyle': 2},
         'offlineAK4PFCHSJetsCorrected': {'LineColor': ROOT.kOrange+1},
         'offlineAK4PuppiJetsCorrected': {'LineColor': ROOT.kViolet},

         'ak8GenJetsNoNu': {'LineColor': 1},
         'hltAK8PFJetsCorrected': {'LineColor': ROOT.kBlue, 'LineStyle': 2},
         'hltAK8PFCHSJetsCorrected': {'LineColor': ROOT.kOrange+1, 'LineStyle': 2},
         'hltAK8PuppiJetsCorrected': {'LineColor': ROOT.kViolet, 'LineStyle': 2},
         'offlineAK8PuppiJetsCorrected': {'LineColor': ROOT.kViolet},

         'genMETCalo': {'LineColor': 1},
         'genMETTrue': {'LineColor': 1},
         'hltPFMET': {'LineColor': ROOT.kOrange+1, 'LineStyle': 2},
         'hltPFMETNoMu': {'LineColor': ROOT.kOrange+1, 'LineStyle': 2},
         'hltPFMETTypeOne': {'LineColor': ROOT.kRed, 'LineStyle': 2},
         'hltPuppiMET': {'LineColor': ROOT.kAzure, 'LineStyle': 2},
         'hltPuppiMETNoMu': {'LineColor': ROOT.kAzure, 'LineStyle': 2},
         'hltPuppiMETTypeOne': {'LineColor': ROOT.kViolet, 'LineStyle': 2},
         'hltPuppiMETWithPuppiForJets': {'LineColor': ROOT.kCyan, 'LineStyle': 2},
         'hltPFMETCHS': {'LineColor': ROOT.kGray+1, 'LineStyle': 2},
         'hltPFMETSoftKiller': {'LineColor': ROOT.kPink+1, 'LineStyle': 2},
         'offlineMETs_Raw': {'LineColor': ROOT.kOrange+1},
         'offlineMETs_Type1': {'LineColor': ROOT.kRed},
         'offlineMETsPuppi_Raw': {'LineColor': ROOT.kAzure},
         'offlineMETsPuppi_Type1': {'LineColor': ROOT.kViolet},
       }

    if key in ['AK4Jets_PFCHS', 'AK4Jets_PFCHS_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'ak4GenJetsNoNu'+var, style_dict['ak4GenJetsNoNu']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK4PFCHSJetsCorrected'+var, style_dict['hltAK4PFCHSJetsCorrected']), 'draw': opt_draw, 'legendName': 'HLT PF+CHS', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineAK4PFCHSJetsCorrected'+var, style_dict['offlineAK4PFCHSJetsCorrected']), 'draw': opt_draw, 'legendName': 'Offline PF+CHS', 'legendDraw': opt_legDraw},
       ]

    elif key in ['AK4Jets_Puppi', 'AK4Jets_Puppi_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'ak4GenJetsNoNu'+var, style_dict['ak4GenJetsNoNu']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK4PuppiJetsCorrected'+var, style_dict['hltAK4PuppiJetsCorrected']), 'draw': opt_draw, 'legendName': 'HLT AK4 Puppi','legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineAK4PuppiJetsCorrected'+var, style_dict['offlineAK4PuppiJetsCorrected']), 'draw': opt_draw, 'legendName': 'Offline AK4 Puppi', 'legendDraw': opt_legDraw},
       ]

    elif key in ['AK4Jets_HLT', 'AK4Jets_HLT_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'ak4GenJetsNoNu'+var, style_dict['ak4GenJetsNoNu']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK4PFJetsCorrected'+var, style_dict['hltAK4PFJetsCorrected']), 'draw': opt_draw,'legendName': 'HLT AK4 PF','legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK4PFCHSJetsCorrected'+var, style_dict['hltAK4PFCHSJetsCorrected']), 'draw': opt_draw,'legendName': 'HLT AK4 PF+CHS','legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK4PuppiJetsCorrected'+var, style_dict['hltAK4PuppiJetsCorrected']), 'draw': opt_draw,'legendName': 'HLT AK4 Puppi','legendDraw': opt_legDraw},
       ]

    elif key in ['AK4Jets_Offline', 'AK4Jets_Offline_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'ak4GenJetsNoNu'+var, style_dict['ak4GenJetsNoNu']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineAK4PFCHSJetsCorrected'+var, style_dict['offlineAK4PFCHSJetsCorrected']), 'draw': opt_draw, 'legendName': 'Offline AK4 PF+CHS', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineAK4PuppiJetsCorrected'+var, style_dict['offlineAK4PuppiJetsCorrected']), 'draw': opt_draw, 'legendName': 'Offline AK4 Puppi', 'legendDraw': opt_legDraw},
       ]

    elif key in ['AK8Jets_Puppi', 'AK8Jets_Puppi_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'ak8GenJetsNoNu'+var, style_dict['ak8GenJetsNoNu']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK8PuppiJetsCorrected'+var, style_dict['hltAK8PuppiJetsCorrected']), 'draw': opt_draw, 'legendName': 'HLT AK8 Puppi','legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineAK8PuppiJetsCorrected'+var, style_dict['offlineAK8PuppiJetsCorrected']), 'draw': opt_draw, 'legendName': 'Offline AK8 Puppi', 'legendDraw': opt_legDraw},
       ]

    elif key in ['AK8Jets_HLT', 'AK8Jets_HLT_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'ak8GenJetsNoNu'+var, style_dict['ak8GenJetsNoNu']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK8PFJetsCorrected'+var, style_dict['hltAK8PFJetsCorrected']), 'draw': opt_draw,'legendName': 'HLT AK8 PF','legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK8PFCHSJetsCorrected'+var, style_dict['hltAK8PFCHSJetsCorrected']), 'draw': opt_draw,'legendName': 'HLT AK8 PF+CHS','legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltAK8PuppiJetsCorrected'+var, style_dict['hltAK8PuppiJetsCorrected']), 'draw': opt_draw,'legendName': 'HLT AK8 Puppi','legendDraw': opt_legDraw},
       ]

    elif key in ['AK8Jets_Offline', 'AK8Jets_Offline_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'ak8GenJetsNoNu'+var, style_dict['ak8GenJetsNoNu']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineAK8PuppiJetsCorrected'+var, style_dict['offlineAK8PuppiJetsCorrected']), 'draw': opt_draw, 'legendName': 'Offline AK8 Puppi', 'legendDraw': opt_legDraw},
       ]

    elif key in ['MET_PF', 'MET_PF_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMET_'+var, style_dict['hltPFMET']), 'draw': opt_draw, 'legendName': 'HLT PF-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETs_Raw_'+var, style_dict['offlineMETs_Raw']), 'draw': opt_draw, 'legendName': 'Offline PF-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMETTypeOne_'+var, style_dict['hltPFMETTypeOne']), 'draw': opt_draw, 'legendName': 'HLT PF-MET Type-1', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETs_Type1_'+var, style_dict['offlineMETs_Type1']), 'draw': opt_draw, 'legendName': 'Offline PF-MET Type-1', 'legendDraw': opt_legDraw},
       ]

    elif key in ['MET_PFRaw', 'MET_PFRaw_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMET_'+var, style_dict['hltPFMET']), 'draw': opt_draw, 'legendName': 'HLT PF-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETs_Raw_'+var, style_dict['offlineMETs_Raw']), 'draw': opt_draw, 'legendName': 'Offline PF-MET Raw', 'legendDraw': opt_legDraw},
       ]

    elif key in ['MET_PFType1', 'MET_PFType1_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMETTypeOne_'+var, style_dict['hltPFMETTypeOne']), 'draw': opt_draw, 'legendName': 'HLT PF-MET Type-1', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETs_Type1_'+var, style_dict['offlineMETs_Type1']), 'draw': opt_draw, 'legendName': 'Offline PF-MET Type-1', 'legendDraw': opt_legDraw},
       ]

    elif key in ['MET_Puppi', 'MET_Puppi_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPuppiMET_'+var, style_dict['hltPuppiMET']), 'draw': opt_draw, 'legendName': 'HLT Puppi-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETsPuppi_Raw_'+var, style_dict['offlineMETsPuppi_Raw']), 'draw': opt_draw,'legendName': 'Offline Puppi-MET Raw','legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPuppiMETTypeOne_'+var, style_dict['hltPuppiMETTypeOne']), 'draw': opt_draw, 'legendName': 'HLT Puppi-MET Type-1', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETsPuppi_Type1_'+var, style_dict['offlineMETsPuppi_Type1']), 'draw': opt_draw, 'legendName': 'Offline Puppi-MET Type-1', 'legendDraw': opt_legDraw},
       ]

    elif key in ['MET_PuppiRaw', 'MET_PuppiRaw_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPuppiMET_'+var, style_dict['hltPuppiMET']), 'draw': opt_draw, 'legendName': 'HLT Puppi-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETsPuppi_Raw_'+var, style_dict['offlineMETsPuppi_Raw']), 'draw': opt_draw,'legendName': 'Offline Puppi-MET Raw','legendDraw': opt_legDraw},
       ]

    elif key in ['MET_PuppiType1', 'MET_PuppiType1_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPuppiMETTypeOne_'+var, style_dict['hltPuppiMETTypeOne']), 'draw': opt_draw, 'legendName': 'HLT Puppi-MET Type-1', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETsPuppi_Type1_'+var, style_dict['offlineMETsPuppi_Type1']), 'draw': opt_draw, 'legendName': 'Offline Puppi-MET Type-1', 'legendDraw': opt_legDraw},
       ]

    elif key in ['MET_Raw_HLT', 'MET_Raw_HLT_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMET_'+var, style_dict['hltPFMET']), 'draw': opt_draw, 'legendName': 'HLT PF-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPuppiMET_'+var, style_dict['hltPuppiMET']), 'draw': opt_draw, 'legendName': 'HLT Puppi-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMETCHS_'+var, style_dict['hltPFMETCHS']), 'draw': opt_draw, 'legendName': 'HLT CHS-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMETSoftKiller_'+var, style_dict['hltPFMETSoftKiller']), 'draw': opt_draw, 'legendName': 'HLT SoftKiller-MET Raw','legendDraw': opt_legDraw},
       ]

    elif key in ['METNoMu_Raw_HLT', 'METNoMu_Raw_HLT_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETCalo_'+var, style_dict['genMETCalo']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMETNoMu_'+var, style_dict['hltPFMETNoMu']), 'draw': opt_draw, 'legendName': 'HLT PF-MET(no #mu) Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPuppiMETNoMu_'+var, style_dict['hltPuppiMETNoMu']), 'draw': opt_draw, 'legendName': 'HLT Puppi-MET(no #mu) Raw', 'legendDraw': opt_legDraw},
       ]

    elif key in ['MET_Type1_HLT', 'MET_Type1_HLT_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPFMETTypeOne_'+var, style_dict['hltPFMETTypeOne']), 'draw': opt_draw, 'legendName': 'HLT PF-MET Type-1', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'hltPuppiMETTypeOne_'+var, style_dict['hltPuppiMETTypeOne']), 'draw': opt_draw, 'legendName': 'HLT Puppi-MET Type-1','legendDraw': opt_legDraw},
       ]

    elif key in ['MET_Raw_Offline', 'MET_Raw_Offline_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETs_Raw_'+var, style_dict['offlineMETs_Raw']), 'draw': opt_draw, 'legendName': 'Offline PF-MET Raw', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETsPuppi_Raw_'+var, style_dict['offlineMETsPuppi_Raw']), 'draw': opt_draw, 'legendName': 'Offline Puppi-MET Raw', 'legendDraw': opt_legDraw},
       ]

    elif key in ['MET_Type1_Offline', 'MET_Type1_Offline_p']:
       the_templates += [
         {'TH1': clone_histogram(histograms, PU_tag, directory+'genMETTrue_'+var, style_dict['genMETTrue']), 'draw': opt_draw, 'legendName': 'GEN', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETs_Type1_'+var, style_dict['offlineMETs_Type1']), 'draw': opt_draw, 'legendName': 'Offline PF-MET Type-1', 'legendDraw': opt_legDraw},
         {'TH1': clone_histogram(histograms, PU_tag, directory+'offlineMETsPuppi_Type1_'+var, style_dict['offlineMETsPuppi_Type1']), 'draw': opt_draw, 'legendName': 'Offline Puppi-MET Type-1', 'legendDraw': opt_legDraw},
       ]

    the_templates_skimmed = []
    for _tmp in the_templates:
        if skipGEN and (_tmp['TH1'] is not None):
           if 'gen' in _tmp['TH1'].GetName().lower():
              continue
        the_templates_skimmed += [_tmp]

    return the_templates_skimmed

#### main --------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('--NoPU', dest='NoPU', action='store', default=None,
                       help='path to input .root file for NoPU')

   parser.add_argument('--PU140', dest='PU140', action='store', default=None,
                       help='path to input .root file for PU140')

   parser.add_argument('--PU200', dest='PU200', action='store', default=None,
                       help='path to input .root file for PU200')

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                       help='path to output directory')

   parser.add_argument('-l', '--label', dest='label', action='store', default='',
                       help='text label (displayed in top-left corner)')

   parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf', 'png'],
                       help='list of extension(s) for output file(s)')

   parser.add_argument('--skip-GenJets', dest='skip_GenJets', action='store_true', default=False,
                       help='skip distributions related to Gen-Jets collection(s)')

   parser.add_argument('--skip-GenMET', dest='skip_GenMET', action='store_true', default=False,
                       help='skip distributions related to Gen-MET collection')

   parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                       help='verbosity level')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   ROOT.gROOT.SetBatch()
   ROOT.gErrorIgnoreLevel = ROOT.kWarning

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation ---
   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output directory already exists [-o]: '+opts.output)

   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))

   EXTS = list(set(opts.exts))
   ### -------------------

   histograms = {}

   if opts.NoPU is not None:
      if os.path.isfile(opts.NoPU):
         histograms['NoPU'] = getTH1sFromTFile(opts.NoPU, verbose=(opts.verbosity > 20))
      else:
         WARNING(log_prx+' invalid path to input file [--NoPU]: '+opts.NoPU)

   if opts.PU140 is not None:
      if os.path.isfile(opts.PU140):
         histograms['PU140'] = getTH1sFromTFile(opts.PU140, verbose=(opts.verbosity > 20))
      else:
         WARNING(log_prx+' invalid path to input file [--PU140]: '+opts.PU140)

   if opts.PU200 is not None:
      if os.path.isfile(opts.PU200):
         histograms['PU200'] = getTH1sFromTFile(opts.PU200, verbose=(opts.verbosity > 20))
      else:
         WARNING(log_prx+' invalid path to input file [--PU200]: '+opts.PU200)

   # Histogram Aliases:
   #  - clone histograms to have under different name
   #    (to aid some of the plotting)
   histogramAliases = {}

   onlineToOffline_dict = {

     'hltAK4PFCHSJetsCorrected_': 'offlineAK4PFCHSJetsCorrected',
     'hltAK4PuppiJetsCorrected_': 'offlineAK4PuppiJetsCorrected',

     'hltAK8PuppiJetsCorrected_': 'offlineAK8PuppiJetsCorrected',

     'hltPFMET_': 'offlineMETs_Raw',
     'hltPFMETTypeOne_': 'offlineMETs_Type1',

     'hltPuppiMET_': 'offlineMETsPuppi_Raw',
     'hltPuppiMETTypeOne_': 'offlineMETsPuppi_Type1',
   }

   for tag1 in sorted(histograms.keys()):
       for tag2 in sorted(histograms[tag1].keys()):
           tag2_basename = os.path.basename(tag2)
           for _tmp in onlineToOffline_dict:
              if (_tmp in tag2_basename) and (onlineToOffline_dict[_tmp] in tag2_basename):
                 tag2_dirname = os.path.dirname(tag2)
                 tag2_copy = tag2_dirname+'/'+tag2_basename.replace(onlineToOffline_dict[_tmp], 'Offline')
                 if tag2_copy in histograms[tag1]:
                    KILL(log_prx+'logic error: attempting to redefine entry in histogramAliases dictionary under keys "'+tag1+'":"'+tag2_copy+'"')

                 histograms[tag1][tag2_copy] = histograms[tag1][tag2].Clone()

   apply_style(0)

   ROOT.TGaxis.SetMaxDigits(4)

   Top = ROOT.gStyle.GetPadTopMargin()
   Rig = ROOT.gStyle.GetPadRightMargin()
   Bot = ROOT.gStyle.GetPadBottomMargin()
   Lef = ROOT.gStyle.GetPadLeftMargin()

   ROOT.TGaxis.SetExponentOffset(-Lef+.50*Lef, 0.03, 'y')

   label_sample = get_text(Lef+(1-Lef-Rig)*0.00, (1-Top)+Top*0.25, 11, .035, opts.label)

   GENJetCollections = [
     'ak4GenJetsNoNu',
     'ak8GenJetsNoNu',
   ]

   JetCollections = GENJetCollections + [

     'hltAK4PFJetsCorrected',
     'hltAK4PFCHSJetsCorrected',
     'hltAK4PuppiJetsCorrected',
     'offlineAK4PFCHSJetsCorrected',
     'offlineAK4PuppiJetsCorrected',

     'hltAK8PFJetsCorrected',
     'hltAK8PFCHSJetsCorrected',
     'hltAK8PuppiJetsCorrected',
     'offlineAK8PuppiJetsCorrected',
   ]

   METCollections = [
     'genMETCalo',
     'genMETTrue',
     'hltPFMET',
     'hltPFMETNoMu',
     'hltPFMETTypeOne',
     'hltPFMETCHS',
     'hltPFMETSoftKiller',
     'hltPuppiMET',
     'hltPuppiMETNoMu',
     'hltPuppiMETTypeOne',
     'hltPuppiMETWithPuppiForJets',
     'offlineMETs_Raw',
     'offlineMETs_Type1',
     'offlineMETsPuppi_Raw',
     'offlineMETsPuppi_Type1',
   ]

   ### 1D Comparisons
   for i_sel in ['NoSelection/']:

       ## ----------------------------------------------------------------------------------------------------
       ## [Jets]: comparisons of different PU scenarios
       ## ----------------------------------------------------------------------------------------------------
       for i_jet in JetCollections:

           if opts.skip_GenJets and (i_jet in GENJetCollections): continue

           jetCategories = JET_CATEGORIES[:]
           if i_jet not in GENJetCollections:
              jetCategories += [_tmp+'_MatchedToGEN' for _tmp in JET_CATEGORIES]
              jetCategories += [_tmp+'_MatchedToOffline' for _tmp in JET_CATEGORIES]

           for i_jetcat in jetCategories:

               label_var = get_text((1-Lef-Rig)+Lef*1.00, (1-Top)+Top*0.25, 31, .030, i_jet+i_jetcat)

               # N-jets
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_jet+i_jetcat+'_njets',

                 templates = get_templates_PU('3PU', histograms, i_sel+i_jet+i_jetcat+'_njets', skipGEN=opts.skip_GenJets),

                 logY = True,

                 ratio = True,

                 normalizedToUnity = True,

                 title = ';number of jets;Fraction Of Events',
               )

               # pT
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_jet+i_jetcat+'_pt',

                 templates = get_templates_PU('3PU', histograms, i_sel+i_jet+i_jetcat+'_pt', skipGEN=opts.skip_GenJets),

                 logX = True,

                 logY = True,

                 ratio = True,

                 xMin = 10,

                 divideByBinWidth = True,

                 normalizedToUnity = True,

                 title = ';Jet p_{T} [GeV];a.u.',
               )

               # eta
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_jet+i_jetcat+'_eta',

                 templates = get_templates_PU('3PU', histograms, i_sel+i_jet+i_jetcat+'_eta', skipGEN=opts.skip_GenJets),

                 ratio = True,

                 divideByBinWidth = True,

                 normalizedToUnity = True,

                 title = ';Jet #eta;a.u.',
               )

               # phi
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_jet+i_jetcat+'_phi',

                 templates = get_templates_PU('3PU', histograms, i_sel+i_jet+i_jetcat+'_phi', skipGEN=opts.skip_GenJets),

                 ratio = True,

                 normalizedToUnity = True,

                 title = ';Jet #phi;a.u.',
               )

               # mass
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_jet+i_jetcat+'_mass',

                 templates = get_templates_PU('3PU', histograms, i_sel+i_jet+i_jetcat+'_mass', skipGEN=opts.skip_GenJets),

                 logX = True,

                 logY = True,

                 ratio = True,

                 xMin = 10,

                 divideByBinWidth = True,

                 normalizedToUnity = True,

                 title = ';Jet mass [GeV];a.u.',
               )

               for i_ref in ['GEN', 'Offline']:

                   # pT response (Ratio wrt {REF})
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_jet+i_jetcat+'_pt_over'+i_ref,

                     templates = get_templates_PU('3PU', histograms, i_sel+i_jet+i_jetcat+'_pt_over'+i_ref, skipGEN=opts.skip_GenJets),

                     normalizedToUnity = True,

                     title = ';Jet p_{T} response (Ratio wrt '+i_ref+');a.u.',
                   )

                   # pT Delta {REF} (X - {REF})
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_jet+i_jetcat+'_pt_minus'+i_ref,

                     templates = get_templates_PU('3PU', histograms, i_sel+i_jet+i_jetcat+'_pt_minus'+i_ref, skipGEN=opts.skip_GenJets),

                     normalizedToUnity = True,

                     title = ';Jet #Deltap_{T} (X - '+i_ref+');a.u.',
                   )

               # pT Response wrt GEN pT/eta
               for (i_key, i_title, i_ymin, i_ymax) in [
                 ('pt_overGEN_Mean_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];Response <Reco/GEN>', 0.1, 3.0),
                 ('pt_overGEN_Mean_wrt_GEN_eta', ';GEN Jet #eta;Response <Reco/GEN>', 0.1, 3.0),
                 ('pt_minusGEN_Mean_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];<Reco#minus GEN> [GeV]', -200, 200),
                 ('pt_minusGEN_Mean_wrt_GEN_eta', ';GEN Jet #eta;<Reco#minus GEN> [GeV]', -200, 200),

                 ('pt_overOffline_Mean_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];Response <HLT/Offline>', 0.1, 3.0),
                 ('pt_overOffline_Mean_wrt_Offline_eta', ';Offline Jet #eta;Response <HLT/Offline>', 0.1, 3.0),
                 ('pt_minusOffline_Mean_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];<HLT#minus Offline> [GeV]', -200, 200),
                 ('pt_minusOffline_Mean_wrt_Offline_eta', ';Offline Jet #eta;<HLT#minus Offline> [GeV]', -200, 200),
               ]:
                 tmp_name = i_jet+i_jetcat+'_'+i_key

                 plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.10, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.30, Bot+(1-Bot-Top)*0.95],

                   stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+tmp_name,

                   templates = get_templates_PU('3PU_p', histograms, i_sel+tmp_name, skipGEN=opts.skip_GenJets),

                   yMin = i_ymin,
                   yMax = i_ymax,

                   title = i_title,
                 )
                 del tmp_name

               # pT Resolution (RMS) wrt GEN pT/eta
               for (i_key, i_title) in [
#                 ('pt_minusGEN_RMS_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];RMS(Reco#minus GEN) [GeV]'),
#                 ('pt_minusGEN_RMS_wrt_GEN_eta', ';GEN Jet #eta;RMS(Reco#minus GEN) [GeV]'),
#                 ('pt_minusGEN_RMSOverMean_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];RMS(Reco#minus GEN) / Response [GeV]'),
#                 ('pt_minusGEN_RMSOverMean_wrt_GEN_eta', ';GEN Jet #eta;RMS(Reco#minus GEN) / Response [GeV]'),

                 ('pt_overGEN_RMS_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];#sigma(p_{T}/p^{GEN}_{T})'),
                 ('pt_overGEN_RMS_wrt_GEN_eta', ';GEN Jet #eta;#sigma(p_{T}/p^{GEN}_{T})'),
                 ('pt_overGEN_RMSOverMean_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];#sigma(p_{T}/p^{GEN}_{T})/<p_{T}/p^{GEN}_{T}>'),
                 ('pt_overGEN_RMSOverMean_wrt_GEN_eta', ';GEN Jet #eta;#sigma(p_{T}/p^{GEN}_{T})/<p_{T}/p^{GEN}_{T}>'),

#                 ('pt_minusOffline_RMS_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];RMS(HLT#minus Offline) [GeV]'),
#                 ('pt_minusOffline_RMS_wrt_Offline_eta', ';Offline Jet #eta;RMS(HLT#minus Offline) [GeV]'),
#                 ('pt_minusOffline_RMSOverMean_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];RMS(HLT#minus Offline) / Response [GeV]'),
#                 ('pt_minusOffline_RMSOverMean_wrt_Offline_eta', ';Offline Jet #eta;RMS(HLT#minus Offline) / Response [GeV]'),

                 ('pt_overOffline_RMS_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];#sigma(p_{T}/p^{Offline}_{T})'),
                 ('pt_overOffline_RMS_wrt_Offline_eta', ';Offline Jet #eta;#sigma(p_{T}/p^{Offline}_{T})'),
                 ('pt_overOffline_RMSOverMean_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];#sigma(p_{T}/p^{Offline}_{T})/<p_{T}/p^{Offline}_{T}>'),
                 ('pt_overOffline_RMSOverMean_wrt_Offline_eta', ';Offline Jet #eta;#sigma(p_{T}/p^{Offline}_{T})/<p_{T}/p^{Offline}_{T}>'),
               ]:
                 tmp_name = i_jet+i_jetcat+'_'+i_key

                 plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.05, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.25, Bot+(1-Bot-Top)*0.95],

                   stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+tmp_name,

                   templates = get_templates_PU('3PU_p', histograms, i_sel+tmp_name, skipGEN=opts.skip_GenJets),

                   yMin = (0.001 if (('overGEN_RMS' in i_key) or ('overOffline_RMS' in i_key)) else 0.1),
                   yMax = (0.800 if (('overGEN_RMS' in i_key) or ('overOffline_RMS' in i_key)) else 200),

                   title = i_title,
                 )
                 del tmp_name

       ## ----------------------------------------------------------------------------------------------------
       ## [MET] comparisons of different PU scenarios
       ## ----------------------------------------------------------------------------------------------------
       for i_met in METCollections:

           if opts.skip_GenMET and (i_met == 'genMETTrue'): continue

           label_var = get_text((1-Lef-Rig)+Lef*1.00, (1-Top)+Top*0.25, 31, .040, i_met)

           # pT
           plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

             stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_pt',

             templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_pt', skipGEN=opts.skip_GenMET),

             logX = True,
    
             ratio = True,
    
             xMin = 10,
    
             divideByBinWidth = True,
    
             normalizedToUnity = True,
    
             title = ';MET [GeV];Fraction Of Events',
           )
    
           # phi
           plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.05, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.35],
    
             stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_phi',
    
             templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_phi', skipGEN=opts.skip_GenMET),

             logX = False,

             ratio = True,

             divideByBinWidth = False,

             normalizedToUnity = True,

             title = ';MET #phi [GeV];Fraction Of Events',
           )

           for i_ref in ['GEN', 'Offline']:

               # pT response (Ratio wrt {REF})
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_pt_over'+i_ref,

                 templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_pt_over'+i_ref, skipGEN=opts.skip_GenMET),

                 logX = False,

                 ratio = False,
    
                 divideByBinWidth = False,
    
                 normalizedToUnity = True,
    
                 title = ';MET response (Ratio wrt '+i_ref+');Fraction Of Events',
               )
        
               # pT Delta {REF} (X - {REF})
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],
        
                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_pt_minus'+i_ref,
    
                 templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_pt_minus'+i_ref, skipGEN=opts.skip_GenMET),
    
                 logX = False,
        
                 ratio = False,
        
                 divideByBinWidth = False,
        
                 normalizedToUnity = True,
    
                 title = ';MET #Deltap_{T} (X - '+i_ref+');Fraction Of Events',
               )

               # pT component parallel to {REF}
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],
    
                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_pt_paraTo'+i_ref,
    
                 templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_pt_paraTo'+i_ref, skipGEN=opts.skip_GenMET),
    
                 logX = False,
    
                 ratio = False,
    
                 divideByBinWidth = False,
    
                 normalizedToUnity = True,
    
                 title = ';MET_{#scale[0.75]{#parallel '+i_ref+'}} [GeV];Fraction Of Events',
               )
    
               # pT component parallel to {REF}, - {REF}
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],
    
                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_pt_paraTo'+i_ref+'Minus'+i_ref,

                 templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_pt_paraTo'+i_ref+'Minus'+i_ref, skipGEN=opts.skip_GenMET),

                 logX = False,

                 ratio = False,
    
                 divideByBinWidth = False,
    
                 normalizedToUnity = True,

                 title = ';MET_{#scale[0.75]{#parallel '+i_ref+'}} - '+i_ref+' [GeV];Fraction Of Events',
               )
    
               # pT component perpendicular to {REF}
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],
    
                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_pt_perpTo'+i_ref,
    
                 templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_pt_perpTo'+i_ref, skipGEN=opts.skip_GenMET),
    
                 logX = False,
    
                 ratio = False,
    
                 divideByBinWidth = False,
    
                 normalizedToUnity = True,
    
                 title = ';MET_{#scale[0.75]{#perp '+i_ref+'}} [GeV];Fraction Of Events',
               )
    
               # phi response (Ratio wrt {REF})
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],
        
                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_phi_over'+i_ref,
    
                 templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_phi_over'+i_ref, skipGEN=opts.skip_GenMET),
    
                 logX = False,
        
                 ratio = False,
        
                 divideByBinWidth = False,
        
                 normalizedToUnity = True,
        
                 title = ';MET #phi response (Ratio wrt '+i_ref+');Fraction Of Events',
               )
        
               # phi Delta {REF} (X - {REF})
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],
        
                 stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+i_met+'_phi_minus'+i_ref,
    
                 templates = get_templates_PU('3PU', histograms, i_sel+i_met+'_phi_minus'+i_ref, skipGEN=opts.skip_GenMET),
        
                 logX = False,
        
                 ratio = False,
        
                 divideByBinWidth = False,
        
                 normalizedToUnity = True,
        
                 title = ';MET #Delta#phi (X - '+i_ref+');Fraction Of Events',
               )

           # pT Response: RECO/{REF}
           for (i_key, i_title, i_ymin, i_ymax) in [
             ('pt_overGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];Response <Reco/GEN>', 0.1, 3.0),
             ('pt_minusGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<Reco #minus GEN> [GeV]', -200, 200),
             ('pt_paraToGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<MET#scale[0.75]{(Reco #parallel GEN)}> [GeV]', -200, 400),
             ('pt_paraToGENMinusGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<MET#scale[0.75]{(Reco #parallel GEN)}#minus GEN> [GeV]', -250, 250),
             ('pt_perpToGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<MET#scale[0.75]{(Reco#perp GEN)} > [GeV]', -30, 30),

             ('pt_overOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];Response <HLT/Offline>', 0.1, 3.0),
             ('pt_minusOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];<HLT#minus Offline> [GeV]', -200, 200),
             ('pt_paraToOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];<MET#scale[0.75]{(HLT #parallel Offline)}> [GeV]', -200, 400),
             ('pt_paraToOfflineMinusOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];<MET#scale[0.75]{(HLT #parallel Offline)}#minus Offline> [GeV]', -250, 250),
             ('pt_perpToOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];<MET#scale[0.75]{(HLT#perp Offline)} > [GeV]', -30, 30),
           ]:
             tmp_name = i_met+'_'+i_key

             plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.10, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.30, Bot+(1-Bot-Top)*0.95],

               stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+tmp_name,

               templates = get_templates_PU('3PU_p', histograms, i_sel+tmp_name, skipGEN=opts.skip_GenMET),

               yMin = i_ymin,
               yMax = i_ymax,

               xMax = 500,

               title = i_title,
             )
             del tmp_name

           # pT Resolution (RMS)
           for (i_key, i_title) in [
             ('pt_minusGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];RMS(Reco#minus GEN) [GeV]'),
             ('pt_overGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];#sigma(p_{T}/p^{GEN}_{T})'),
             ('pt_paraToGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco #parallel GEN)} [GeV]'),
             ('pt_paraToGENMinusGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco_{#parallel GEN}#minus GEN)} [GeV]'),
             ('pt_perpToGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco#perp GEN)}  [GeV]'),
             ('pt_minusGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];RMS(Reco#minus GEN) / Response [GeV]'),
             ('pt_overGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];#sigma(p_{T}/p^{GEN}_{T})/<p_{T}/p^{GEN}_{T}>'),
             ('pt_paraToGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco #parallel GEN)} / Response [GeV]'),
             ('pt_paraToGENMinusGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco_{#parallel GEN}#minus GEN)} / Response [GeV]'),
             ('pt_perpToGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco#perp GEN)}  / Response [GeV]'),

             ('pt_minusOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];RMS(HLT#minus Offline) [GeV]'),
             ('pt_overOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];#sigma(p_{T}/p^{Offline}_{T})'),
             ('pt_paraToOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT #parallel Offline)} [GeV]'),
             ('pt_paraToOfflineMinusOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT_{#parallel Offline}#minus Offline)} [GeV]'),
             ('pt_perpToOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT#perp Offline)}  [GeV]'),
             ('pt_minusOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];RMS(HLT#minus Offline) / Response [GeV]'),
             ('pt_overOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];#sigma(p_{T}/p^{Offline}_{T})/<p_{T}/p^{Offline}_{T}>'),
             ('pt_paraToOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT #parallel Offline)} / Response [GeV]'),
             ('pt_paraToOfflineMinusOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT_{#parallel Offline}#minus Offline)} / Response [GeV]'),
             ('pt_perpToOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT#perp Offline)}  / Response [GeV]'),
           ]:
             tmp_name = i_met+'_'+i_key

             plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.05, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.25, Bot+(1-Bot-Top)*0.95],

               stickers=[label_sample, label_var], output=opts.output+'/'+i_sel+'/vsPU/'+tmp_name,

               templates = get_templates_PU('3PU_p', histograms, i_sel+tmp_name, skipGEN=opts.skip_GenMET),

               yMin = (0.001 if (('overGEN_RMS' in i_key) or ('overOffline_RMS' in i_key)) else 0.1),
               yMax = (0.800 if (('overGEN_RMS' in i_key) or ('overOffline_RMS' in i_key)) else 200),

               xMax = 500,

               title = i_title,
             )
             del tmp_name

       ## ----------------------------------------------------------------------------------------------------
       ## [Jets] Compare collections in different input samples
       ## ----------------------------------------------------------------------------------------------------
       for pu_tag in ['NoPU', 'PU140', 'PU200']:

           label_PU = get_text((1-Lef-Rig)+Lef*1.00, (1-Top)+Top*0.25, 31, .050, '') #!! pu_tag)

           for comp_tag in ['AK4Jets_PFCHS', 'AK4Jets_Puppi', 'AK4Jets_HLT', 'AK4Jets_Offline']:

               jetCategories = JET_CATEGORIES[:]
               jetCategories += [_tmp+'_MatchedToGEN' for _tmp in JET_CATEGORIES]
               jetCategories += [_tmp+'_MatchedToOffline' for _tmp in JET_CATEGORIES]

               for i_jetcat in jetCategories:

                   # N-jets
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_njets_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, i_jetcat+'_njets', skipGEN=opts.skip_GenJets),

                     logY = True,

                     ratio = True,

                     normalizedToUnity = True,

                     title = ';number of jets;Fraction Of Events',
                   )

                   # pT
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_pt_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, i_jetcat+'_pt', skipGEN=opts.skip_GenJets),

                     logX = True,

                     logY = True,

                     ratio = True,

                     xMin = 10,

                     divideByBinWidth = True,

                     normalizedToUnity = True,

                     title = ';Jet p_{T} [GeV];a.u.',
                   )

                   # eta
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_eta_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, i_jetcat+'_eta', skipGEN=opts.skip_GenJets),

                     ratio = True,

                     divideByBinWidth = True,

                     normalizedToUnity = True,

                     title = ';Jet #eta;a.u.',
                   )

                   # phi
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_phi_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, i_jetcat+'_phi', skipGEN=opts.skip_GenJets),

                     logX = False,

                     ratio = True,

                     divideByBinWidth = False,

                     normalizedToUnity = True,

                     title = ';Jet #phi;a.u.',
                   )

                   # mass
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_mass_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, i_jetcat+'_mass', skipGEN=opts.skip_GenJets),

                     logX = True,

                     logY = True,

                     ratio = True,

                     xMin = 10,

                     divideByBinWidth = True,

                     normalizedToUnity = True,

                     title = ';Jet mass [GeV];a.u.',
                   )

                   for i_ref in ['GEN', 'Offline']:

                       # pT response (Ratio wrt {REF})
                       plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                         stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_pt_over'+i_ref+'_at'+pu_tag,

                         templates = get_templates(comp_tag, histograms, pu_tag, i_sel, i_jetcat+'_pt_over'+i_ref, skipGEN=opts.skip_GenJets),

                         normalizedToUnity = True,

                         title = ';Jet p_{T} response (Ratio wrt '+i_ref+');a.u.',
                       )

                       # pT Delta (Diff wrt {REF})
                       plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                         stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_pt_minus'+i_ref+'_at'+pu_tag,

                         templates = get_templates(comp_tag, histograms, pu_tag, i_sel, i_jetcat+'_pt_minus'+i_ref, skipGEN=opts.skip_GenJets),

                         normalizedToUnity = True,

                         title = ';Jet #Deltap_{T} (X - '+i_ref+') [GeV];a.u.',
                       )

                   # pT Response: RECO/{REF}
                   for (i_key, i_title, i_ymin, i_ymax) in [
                     ('pt_overGEN_Mean_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];Response <Reco/GEN>', 0.1, 3.0),
                     ('pt_overGEN_Mean_wrt_GEN_eta', ';GEN Jet #eta;Response <Reco/GEN>', 0.1, 3.0),
                     ('pt_minusGEN_Mean_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];<Reco#minus GEN> [GeV]', -200, 200),
                     ('pt_minusGEN_Mean_wrt_GEN_eta', ';GEN Jet #eta;<Reco#minus GEN> [GeV]', -200, 200),

                     ('pt_overOffline_Mean_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];Response <HLT/Offline>', 0.1, 3.0),
                     ('pt_overOffline_Mean_wrt_Offline_eta', ';Offline Jet #eta;Response <HLT/Offline>', 0.1, 3.0),
                     ('pt_minusOffline_Mean_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];<HLT#minus Offline> [GeV]', -200, 200),
                     ('pt_minusOffline_Mean_wrt_Offline_eta', ';Offline Jet #eta;<HLT#minus Offline> [GeV]', -200, 200),
                   ]:
                     plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.10, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.50, Bot+(1-Bot-Top)*0.95],

                       stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_'+i_key+'_at'+pu_tag,

                       templates = get_templates(comp_tag+'_p', histograms, pu_tag, i_sel, i_jetcat+'_'+i_key, skipGEN=opts.skip_GenJets),

                       yMin = i_ymin,
                       yMax = i_ymax,

                       title = i_title,
                     )

                   # pT Resolution (RMS)
                   for (i_key, i_title) in [
                     ('pt_minusGEN_RMS_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];RMS(Reco#minus GEN) [GeV]'),
                     ('pt_minusGEN_RMS_wrt_GEN_eta', ';GEN Jet #eta;RMS(Reco#minus GEN) [GeV]'),
                     ('pt_minusGEN_RMSOverMean_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];RMS(Reco#minus GEN) / Response [GeV]'),
                     ('pt_minusGEN_RMSOverMean_wrt_GEN_eta', ';GEN Jet #eta;RMS(Reco#minus GEN) / Response [GeV]'),

                     ('pt_overGEN_RMS_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];#sigma(p_{T}/p^{GEN}_{T})'),
                     ('pt_overGEN_RMS_wrt_GEN_eta', ';GEN Jet #eta;#sigma(p_{T}/p^{GEN}_{T})'),
                     ('pt_overGEN_RMSOverMean_wrt_GEN_pt', ';GEN Jet p_{T} [GeV];#sigma(p_{T}/p^{GEN}_{T})/<p_{T}/p^{GEN}_{T}>'),
                     ('pt_overGEN_RMSOverMean_wrt_GEN_eta', ';GEN Jet #eta;#sigma(p_{T}/p^{GEN}_{T})/<p_{T}/p^{GEN}_{T}>'),

                     ('pt_minusOffline_RMS_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];RMS(HLT#minus Offline) [GeV]'),
                     ('pt_minusOffline_RMS_wrt_Offline_eta', ';Offline Jet #eta;RMS(HLT#minus Offline) [GeV]'),
                     ('pt_minusOffline_RMSOverMean_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];RMS(HLT#minus Offline) / Response [GeV]'),
                     ('pt_minusOffline_RMSOverMean_wrt_Offline_eta', ';Offline Jet #eta;RMS(HLT#minus Offline) / Response [GeV]'),

                     ('pt_overOffline_RMS_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];#sigma(p_{T}/p^{Offline}_{T})'),
                     ('pt_overOffline_RMS_wrt_Offline_eta', ';Offline Jet #eta;#sigma(p_{T}/p^{Offline}_{T})/'),
                     ('pt_overOffline_RMSOverMean_wrt_Offline_pt', ';Offline Jet p_{T} [GeV];#sigma(p_{T}/p^{Offline}_{T})/<p_{T}/p^{Offline}_{T}>'),
                     ('pt_overOffline_RMSOverMean_wrt_Offline_eta', ';Offline Jet #eta;#sigma(p_{T}/p^{Offline}_{T})/<p_{T}/p^{Offline}_{T}>'),
                   ]:
                     plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.10, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.50, Bot+(1-Bot-Top)*0.95],

                       stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/Jet'+i_jetcat+'_'+i_key+'_at'+pu_tag,

                       templates = get_templates(comp_tag+'_p', histograms, pu_tag, i_sel, i_jetcat+'_'+i_key, skipGEN=opts.skip_GenJets),

                       yMin = (0.001 if (('overGEN_RMS' in i_key) or ('overOffline_RMS' in i_key)) else 0.1),
                       yMax = (0.800 if (('overGEN_RMS' in i_key) or ('overOffline_RMS' in i_key)) else 200),

                       title = i_title,
                     )

       ## ----------------------------------------------------------------------------------------------------
       ## [MET] Compare collections in different input samples
       ## ----------------------------------------------------------------------------------------------------
       for pu_tag in ['NoPU', 'PU140', 'PU200']:

           label_PU = get_text((1-Lef-Rig)+Lef*1.00, (1-Top)+Top*0.25, 31, .050, '') #!!pu_tag)

           for comp_tag in ['MET_PF', 'MET_PFRaw', 'MET_PFType1', 'MET_Puppi', 'MET_PuppiRaw', 'MET_PuppiType1', 'MET_Raw_HLT', 'METNoMu_Raw_HLT', 'MET_Type1_HLT', 'MET_Raw_Offline', 'MET_Type1_Offline']:

               # pT
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                 stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_pt_at'+pu_tag,

                 templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'pt', skipGEN=opts.skip_GenMET),

                 logX = True,

                 ratio = True,

                 xMin = 10,

                 divideByBinWidth = True,

                 normalizedToUnity = True,

                 title = ';MET [GeV];Fraction Of Events',
               )

               # phi
               plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                 stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_phi_at'+pu_tag,

                 templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'phi', skipGEN=opts.skip_GenMET),

                 logX = False,

                 ratio = True,

                 divideByBinWidth = False,

                 normalizedToUnity = True,

                 title = ';MET #phi;Fraction Of Events',
               )

               for i_ref in ['GEN', 'Offline']:

                   # pT response (Ratio wrt {REF})
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_pt_over'+i_ref+'_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'pt_over'+i_ref, skipGEN=opts.skip_GenMET),

                     normalizedToUnity = True,

                     title = ';MET response (Ratio wrt '+i_ref+');Fraction Of Events',
                   )

                   # pT Delta {REF}
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_pt_minus'+i_ref+'_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'pt_minus'+i_ref, skipGEN=opts.skip_GenMET),

                     normalizedToUnity = True,

                     title = ';MET #Deltap_{T} (X - '+i_ref+') [GeV];Fraction Of Events',
                   )

                   # pT component parallel to {REF}
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_pt_paraTo'+i_ref+'_at'+pu_tag,
        
                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'pt_paraTo'+i_ref, skipGEN=opts.skip_GenMET),

                     normalizedToUnity = True,

                     title = ';MET_{#scale[0.75]{#parallel '+i_ref+'}} [GeV];Fraction Of Events',
                   )

                   # pT component parallel to {REF}, - {REF}
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_pt_paraTo'+i_ref+'Minus'+i_ref+'_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'pt_paraTo'+i_ref+'Minus'+i_ref, skipGEN=opts.skip_GenMET),

                     normalizedToUnity = True,

                     title = ';MET_{#scale[0.75]{#parallel '+i_ref+'}}#minus '+i_ref+' [GeV];Fraction Of Events',
                   )

                   # pT component perpendicular to {REF}
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],

                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_pt_perpTo'+i_ref+'_at'+pu_tag,

                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'pt_perpTo'+i_ref, skipGEN=opts.skip_GenMET),

                     normalizedToUnity = True,

                     title = ';MET_{#scale[0.75]{#perp '+i_ref+'}} [GeV];Fraction Of Events',
                   )

                   # Phi response (Ratio wrt {REF})
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],
            
                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_phi_over'+i_ref+'_at'+pu_tag,
            
                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'phi_over'+i_ref, skipGEN=opts.skip_GenMET),
        
                     normalizedToUnity = True,
            
                     title = ';MET #phi response (Ratio wrt '+i_ref+');Fraction Of Events',
                   )

                   # Phi Delta {REF}
                   plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.55, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.95],
    
                     stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_phi_minus'+i_ref+'_at'+pu_tag,
    
                     templates = get_templates(comp_tag, histograms, pu_tag, i_sel, 'phi_minus'+i_ref, skipGEN=opts.skip_GenMET),
    
                     normalizedToUnity = True,
    
                     title = ';MET #Delta#phi (X - '+i_ref+');Fraction Of Events',
                   )

               # pT Response: RECO/{REF}
               for (i_key, i_title, i_ymin, i_ymax) in [
                 ('pt_overGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];Response <Reco/GEN>', 0.1, 3.0),
                 ('pt_minusGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<Reco#minus GEN> [GeV]', -200, 200),
                 ('pt_paraToGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<MET#scale[0.75]{(Reco #parallel GEN)}> [GeV]', -200, 400),
                 ('pt_paraToGENMinusGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<MET#scale[0.75]{(Reco #parallel GEN)}#minus GEN> [GeV]', -250, 250),
                 ('pt_perpToGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<MET#scale[0.75]{(Reco#perp GEN)} > [GeV]', -30, 30),

                 ('pt_overOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];Response <HLT/Offline>', 0.1, 3.0),
                 ('pt_minusOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];<HLT#minus Offline> [GeV]', -200, 200),
                 ('pt_paraToOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];<MET#scale[0.75]{(HLT #parallel Offline)}> [GeV]', -200, 400),
                 ('pt_paraToOfflineMinusOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];<MET#scale[0.75]{(HLT #parallel Offline)}#minus Offline> [GeV]', -250, 250),
                 ('pt_perpToOffline_Mean_wrt_Offline_pt', ';Offline MET [GeV];<MET#scale[0.75]{(HLT#perp Offline)} > [GeV]', -30, 30),
               ]:
                 plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.10, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.50, Bot+(1-Bot-Top)*0.95],

                   stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_'+i_key+'_at'+pu_tag,

                   templates = get_templates(comp_tag+'_p', histograms, pu_tag, i_sel, i_key, skipGEN=opts.skip_GenMET),

                   yMin = i_ymin,
                   yMax = i_ymax,

                   title = i_title,
                 )

               # pT Resolution (RMS)
               for (i_key, i_title) in [
                 ('pt_minusGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];RMS(Reco#minus GEN) [GeV]'),
                 ('pt_overGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];#sigma(p_{T}/p^{GEN}_{T})'),
                 ('pt_paraToGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco #parallel GEN)} [GeV]'),
                 ('pt_paraToGENMinusGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco_{#parallel GEN}#minus GEN)} [GeV]'),
                 ('pt_perpToGEN_RMS_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco#perp GEN)}  [GeV]'),
                 ('pt_minusGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];RMS(Reco#minus GEN) / Response [GeV]'),
                 ('pt_overGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];#sigma(p_{T}/p^{GEN}_{T})/<p_{T}/p^{GEN}_{T}>'),
                 ('pt_paraToGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco #parallel GEN)} / Response [GeV]'),
                 ('pt_paraToGENMinusGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco_{#parallel GEN}#minus GEN)} / Response [GeV]'),
                 ('pt_perpToGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];RMS#scale[0.75]{(Reco#perp GEN)}  / Response [GeV]'),

                 ('pt_minusOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];RMS(HLT#minus Offline) [GeV]'),
                 ('pt_overOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];#sigma(p_{T}/p^{Offline}_{T})'),
                 ('pt_paraToOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT #parallel Offline)} [GeV]'),
                 ('pt_paraToOfflineMinusOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT_{#parallel Offline}#minus Offline)} [GeV]'),
                 ('pt_perpToOffline_RMS_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT#perp Offline)}  [GeV]'),
                 ('pt_minusOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];RMS(HLT#minus Offline) / Response [GeV]'),
                 ('pt_overOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];#sigma(p_{T}/p^{Offline}_{T})/<p_{T}/p^{Offline}_{T}>'),
                 ('pt_paraToOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT #parallel Offline)} / Response [GeV]'),
                 ('pt_paraToOfflineMinusOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT_{#parallel Offline}#minus Offline)} / Response [GeV]'),
                 ('pt_perpToOffline_RMSOverMean_wrt_Offline_pt', ';Offline MET [GeV];RMS#scale[0.75]{(HLT#perp Offline)}  / Response [GeV]'),
               ]:
                 plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.10, Bot+(1-Bot-Top)*0.65, Lef+(1-Rig-Lef)*0.50, Bot+(1-Bot-Top)*0.95],

                   stickers=[label_sample, label_PU], output=opts.output+'/'+i_sel+'/'+comp_tag+'/MET_'+i_key+'_at'+pu_tag,

                   templates = get_templates(comp_tag+'_p', histograms, pu_tag, i_sel, i_key, skipGEN=opts.skip_GenMET),

                   yMin = (0.001 if (('overGEN_RMS' in i_key) or ('overOffline_RMS' in i_key)) else 0.1),
                   yMax = (0.800 if (('overGEN_RMS' in i_key) or ('overOffline_RMS' in i_key)) else 200),

                   xMax = 500,

                   title = i_title,
                 )

   ### Efficiencies

   # [Jets] Efficiencies
   effJets_dict = {

#     'hltAK4PFCHS100_EtaIncl': {
#       'label': 'HLT AK4 PF+CHS, p_{T} > 100 GeV',
#       'wrt': ['hltAK4PFCHSJetsCorrected_EtaIncl_MatchedToGEN_pt0:ak4GenJetsNoNu_EtaIncl_pt', 'hltAK4PFCHSJetsCorrected_EtaIncl_MatchedToOffline_pt0:Offline_pt'],
#     },
#
#     'hltAK4PFCHS100_HB': {
#       'label': 'HLT AK4 PF+CHS, p_{T} > 100 GeV (HB)',
#       'wrt': ['hltAK4PFCHSJetsCorrected_HB_MatchedToGEN_pt0:ak4GenJetsNoNu_EtaIncl_pt', 'hltAK4PFCHSJetsCorrected_HB_MatchedToOffline_pt0:Offline_pt'],
#     },
#
#     'hltAK4PFCHS100_HGCal': {
#       'label': 'HLT AK4 PF+CHS, p_{T} > 100 GeV (HGCal)',
#       'wrt': ['hltAK4PFCHSJetsCorrected_HGCal_MatchedToGEN_pt0:ak4GenJetsNoNu_EtaIncl_pt', 'hltAK4PFCHSJetsCorrected_HGCal_MatchedToOffline_pt0:Offline_pt'],
#     },
#
#     'hltAK4PFCHS100_HF': {
#       'label': 'HLT AK4 PF+CHS, p_{T} > 100 GeV (HF)',
#       'wrt': ['hltAK4PFCHSJetsCorrected_HF_MatchedToGEN_pt0:ak4GenJetsNoNu_EtaIncl_pt', 'hltAK4PFCHSJetsCorrected_HF_MatchedToOffline_pt0:Offline_pt'],
#     },
#
#     'hltAK4Puppi100_EtaIncl': {
#       'label': 'HLT AK4 Puppi, p_{T} > 100 GeV',
#       'wrt': ['hltAK4PuppiJetsCorrected_EtaIncl_MatchedToGEN_pt0:ak4GenJetsNoNu_EtaIncl_pt', 'hltAK4PuppiJetsCorrected_EtaIncl_MatchedToOffline_pt0:Offline_pt'],
#     },
#
#     'hltAK4Puppi100_HB': {
#       'label': 'HLT AK4 Puppi, p_{T} > 100 GeV (HB)',
#       'wrt': ['hltAK4PuppiJetsCorrected_HB_MatchedToGEN_pt0:ak4GenJetsNoNu_EtaIncl_pt', 'hltAK4PuppiJetsCorrected_HB_MatchedToOffline_pt0:Offline_pt'],
#     },
#
#     'hltAK4Puppi100_HGCal': {
#       'label': 'HLT AK4 Puppi, p_{T} > 100 GeV (HGCal)',
#       'wrt': ['hltAK4PuppiJetsCorrected_HGCal_MatchedToGEN_pt0:ak4GenJetsNoNu_EtaIncl_pt', 'hltAK4PuppiJetsCorrected_HGCal_MatchedToOffline_pt0:Offline_pt'],
#     },
#
#     'hltAK4Puppi100_HF': {
#       'label': 'HLT AK4 Puppi, p_{T} > 100 GeV (HF)',
#       'wrt': ['hltAK4PuppiJetsCorrected_HF_MatchedToGEN_pt0:ak4GenJetsNoNu_EtaIncl_pt', 'hltAK4PuppiJetsCorrected_HF_MatchedToOffline_pt0:Offline_pt'],
#     },
   }

   for i_eff in sorted(effJets_dict.keys()):

       efficiencies = {}

       pt_binEdges = [20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500] #, 600, 700, 800, 1000]

       for pu_tag in ['NoPU', 'PU140', 'PU200']:

           efficiencies[pu_tag] = {}

           for i_jetv in effJets_dict[i_eff]['wrt']:

               hNum_0 = clone_histogram(histograms, pu_tag, i_eff+'/'+i_jetv)
               hDen_0 = clone_histogram(histograms, pu_tag, 'NoSelection/'+i_jetv)

               if (hNum_0 is None) or (hDen_0 is None): continue

               hNum_1 = hNum_0.ProjectionY('tmp1', 1, hNum_0.GetNbinsX())
               hDen_1 = hDen_0.ProjectionY('tmp2', 1, hDen_0.GetNbinsX())

               hNum = get_rebinned_histo(hNum_1, pt_binEdges)
               hDen = get_rebinned_histo(hDen_1, pt_binEdges)

               efficiencies[pu_tag][i_jetv] = get_efficiency_graph(hNum, hDen)

       label_eff_str = effJets_dict[i_eff]['label']

       label_eff = get_pavetext(Lef+(1-Lef-Rig)*0.05, Bot+(1-Bot-Top)*0.85, Lef+(1-Lef-Rig)*0.55, Bot+(1-Bot-Top)*0.95, 0.030, label_eff_str)
       label_eff.SetFillColor(ROOT.kWhite)

       for i_jetv in effJets_dict[i_eff]['wrt']:

           if opts.skip_GenJets and i_jetv.startswith('akGenJetsNoNu_'): continue

           label_var = None #get_text(Lef+(1-Lef-Rig)*1.00, (1-Top)+Top*0.25, 31, .040, i_jetv)

           plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.05, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.35],

             stickers=[label_sample, label_var, label_eff], output=opts.output+'/Eff_'+i_eff+'/'+i_jetv.replace(':', '_'),

             templates=[
               {'TH1': clone_graph(efficiencies, 'NoPU' , i_jetv, {'LineColor': 1, 'LineWidth': 3}, verbose=(opts.verbosity > 10)), 'draw': 'lepz', 'legendName': 'NoPU' , 'legendDraw': 'l'},
               {'TH1': clone_graph(efficiencies, 'PU140', i_jetv, {'LineColor': 4, 'LineWidth': 3}, verbose=(opts.verbosity > 10)), 'draw': 'lepz', 'legendName': 'PU140', 'legendDraw': 'l'},
               {'TH1': clone_graph(efficiencies, 'PU200', i_jetv, {'LineColor': 2, 'LineWidth': 3}, verbose=(opts.verbosity > 10)), 'draw': 'lepz', 'legendName': 'PU200', 'legendDraw': 'l'},
             ],

             ratio = False,

             xMin = 40,
             xMax = 500,

             yMin = 0.0,
             yMax = 1.25,

             title = ';'+i_jetv.split(':')[1]+' [GeV];Efficiency',
           )

   # [MET] Efficiencies
   effMET_dict = {

     'hltPFMET200': {'label': 'HLT PF-MET Raw > 200 GeV', 'wrt': ['genMETTrue_pt', 'offlineMETs_Raw_pt', 'offlineMETs_Type1_pt']},
     'hltPFMETTypeOne200': {'label': 'HLT PF-MET Type-1 > 200 GeV', 'wrt': ['genMETTrue_pt', 'offlineMETs_Raw_pt', 'offlineMETs_Type1_pt']},

     'hltPuppiMET200': {'label': 'HLT Puppi-MET Raw > 200 GeV', 'wrt': ['genMETTrue_pt', 'offlineMETsPuppi_Raw_pt', 'offlineMETsPuppi_Type1_pt']},
     'hltPuppiMETTypeOne200': {'label': 'HLT Puppi-MET Type-1 > 200 GeV', 'wrt': ['genMETTrue_pt', 'offlineMETsPuppi_Raw_pt', 'offlineMETsPuppi_Type1_pt']},
   }

   for i_eff in sorted(effMET_dict.keys()):

       efficiencies = {}

       pt_binEdges = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000]

       for pu_tag in ['NoPU', 'PU140', 'PU200']:

           efficiencies[pu_tag] = {}

           for i_metv in effMET_dict[i_eff]['wrt']:

               hNum_0 = clone_histogram(histograms, pu_tag, i_eff+'/'+i_metv)
               hDen_0 = clone_histogram(histograms, pu_tag, 'NoSelection/'+i_metv)

               if (hNum_0 is None) or (hDen_0 is None): continue

               hNum = get_rebinned_histo(hNum_0, pt_binEdges)
               hDen = get_rebinned_histo(hDen_0, pt_binEdges)

               efficiencies[pu_tag][i_metv] = get_efficiency_graph(hNum, hDen)

       label_eff_str = effMET_dict[i_eff]['label']

       label_eff = get_pavetext(Lef+(1-Lef-Rig)*0.05, Bot+(1-Bot-Top)*0.85, Lef+(1-Lef-Rig)*0.55, Bot+(1-Bot-Top)*0.95, 0.030, label_eff_str)
       label_eff.SetFillColor(ROOT.kWhite)

       for i_metv in effMET_dict[i_eff]['wrt']:

           if opts.skip_GenMET and (i_metv.startswith('genMETTrue')): continue

           label_var = None #get_text(Lef+(1-Lef-Rig)*1.00, (1-Top)+Top*0.25, 31, .040, i_metv)

           plot(output_extensions=EXTS, legXY=[Lef+(1-Rig-Lef)*0.75, Bot+(1-Bot-Top)*0.05, Lef+(1-Rig-Lef)*0.95, Bot+(1-Bot-Top)*0.35],

             stickers=[label_sample, label_var, label_eff], output=opts.output+'/Eff_'+i_eff+'/'+i_metv,

             templates=[
               {'TH1': clone_graph(efficiencies, 'NoPU' , i_metv, {'LineColor': 1, 'LineWidth': 3}, verbose=(opts.verbosity > 10)), 'draw': 'lepz', 'legendName': 'NoPU' , 'legendDraw': 'l'},
               {'TH1': clone_graph(efficiencies, 'PU140', i_metv, {'LineColor': 4, 'LineWidth': 3}, verbose=(opts.verbosity > 10)), 'draw': 'lepz', 'legendName': 'PU140', 'legendDraw': 'l'},
               {'TH1': clone_graph(efficiencies, 'PU200', i_metv, {'LineColor': 2, 'LineWidth': 3}, verbose=(opts.verbosity > 10)), 'draw': 'lepz', 'legendName': 'PU200', 'legendDraw': 'l'},
             ],

             ratio = False,

             xMin = 40,
             xMax = 800,

             yMin = 0.0,
             yMax = 1.25,

             title = ';'+i_metv+' [GeV];Efficiency',
           )

   print colored_text('[output]', ['1','92']), os.path.relpath(opts.output)
