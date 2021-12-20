#!/usr/bin/env python
import argparse
import os
import fnmatch
import math
import ROOT
import array

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

def updateDictionary(dictionary, tDirectory, prefix='', matchKeys=[], skipKeys=[], verbosity=0):

    key_prefix = prefix+'/' if (len(prefix) > 0) else ''

    for j_key in tDirectory.GetListOfKeys():

        j_key_name = j_key.GetName()

        j_obj = tDirectory.Get(j_key_name)

        if j_obj.InheritsFrom('TDirectory'):
           updateDictionary(dictionary, j_obj, prefix=key_prefix+j_key_name, matchKeys=matchKeys, skipKeys=skipKeys, verbosity=verbosity)

#!!        elif j_obj.InheritsFrom('TH1') or j_obj.InheritsFrom('TGraph'):
        elif j_obj.InheritsFrom('TH3'):

           out_key = key_prefix+j_key_name

           if skipKeys:
              skip_key = False
              for _keyw in skipKeys:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip_key = True
                     break
              if skip_key:
                 continue

           if matchKeys:
              skip_key = True
              for _keyw in matchKeys:
                  if fnmatch.fnmatch(out_key, _keyw):
                     skip_key = False
                     break
              if skip_key:
                 continue

           h0 = j_obj.Clone()
           if out_key in dictionary:
              try:
                 dictionary[out_key].Add(h0)
              except:
                 KILL(log_prx+'input error -> failed to add templates under key ["'+out_key+'"]: '+tDirectory.GetName())
           else:
              dictionary[out_key] = h0
              if hasattr(dictionary[out_key], 'SetDirectory'):
                 dictionary[out_key].SetDirectory(0)

           if verbosity:
              print colored_text('[input]', ['1','92']), out_key

    return dictionary

def addTemplates(templateDict, filePath, matchKeys, skipKeys, verbosity=0):

    i_inptfile = ROOT.TFile.Open(filePath)
    if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered):
       return templateDict

    updateDictionary(templateDict, i_inptfile, prefix='', matchKeys=matchKeys, skipKeys=skipKeys, verbosity=verbosity)

    i_inptfile.Close()

    return templateDict

def plot(histograms, outputs, title, labels, legXY=[], ratio=False, ratioPadFrac=0.3, xMin=None, xMax=None, yMin=None, yMax=None, logX=False, logY=False, autoRangeX=False, xLabelSize=None, xBinLabels=None):
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

       if xLabelSize:
          h0.GetXaxis().SetLabelSize(xLabelSize)

       if xBinLabels:
          xBinLabels = xBinLabels[int(round(XMIN)):int(round(XMAX))]
          h0.GetXaxis().Set(len(xBinLabels), XMIN, XMAX)
          for tmpIdx, tmpLab in enumerate(xBinLabels):
              h0.GetXaxis().SetBinLabel(tmpIdx+1, tmpLab)

#      h0.GetXaxis().SetRangeUser(XMIN, XMAX)
#      h0.GetYaxis().SetRangeUser(YMIN, YMAX)

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

        print colored_text('[output]', ['1', '92']), os.path.relpath(output_file)

    canvas.Close()

    if ratio:
       del plot_ratios
       del denom

    return 0

#### main
if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', nargs='+', default=[], required=True,
                       help='list of input files [format: "PATH:LEGEND:LINECOLOR:LINESTYLE:MARKERSTYLE:MARKERCOLOR:MARKERSIZE"]')

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                       help='path to output directory')

   parser.add_argument('-m', '--match-keys', dest='match_keys', nargs='+', default=[],
                       help='list of matching-patterns to skim input histograms (input is a match if its name matches any of the specified patterns)')

   parser.add_argument('-s', '--skip-keys', dest='skip_keys', nargs='+', default=[],
                       help='list of matching-patterns to skip input histograms (input is skipped if its name matches any of the specified patterns)')

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

   MATCH_KEYS = sorted(list(set(opts.match_keys)))
   MATCH_KEYS = [_tmp.replace('\'','').replace('"','') for _tmp in MATCH_KEYS]

   SKIP_KEYS = sorted(list(set(opts.skip_keys)))
   SKIP_KEYS = [_tmp.replace('\'','').replace('"','') for _tmp in SKIP_KEYS]

   EXTS = list(set(opts.exts))
   ### -------------------

   th3d_dict = {}
   for _input in opts.inputs:
       addTemplates(th3d_dict, _input, matchKeys=MATCH_KEYS, skipKeys=SKIP_KEYS, verbosity=opts.verbosity)

   for th3_key in th3d_dict:

       etaBins = [_tmp for _tmp in range(1, 2+th3d_dict[th3_key].GetNbinsZ()) if _tmp%2]
#       etaBins = [1, 1+th3d_dict[th3_key].GetNbinsZ()]
       etaBins = sorted(list(set(etaBins)))

       print th3_key, th3d_dict[th3_key].GetEntries()

       for etaBinIdx in range(len(etaBins)-1):

           th3d_dict[th3_key].GetZaxis().SetRange(etaBins[etaBinIdx], etaBins[etaBinIdx+1]-1)
           th2_slice = th3d_dict[th3_key].Project3D('xy')

           ptBins = [1, th2_slice.GetNbinsX()+1]
           print '0', ptBins
           ptBinFirst = 1
           ptBinOffset = 0
           while True:
               if th2_slice.Integral(ptBinFirst, ptBinFirst+ptBinOffset, 1, th2_slice.GetNbinsY()) > 10.:
                  if ((ptBinFirst+ptBinOffset) == th2_slice.GetNbinsX()):
                     break
                  ptBinFirst = ptBinFirst+ptBinOffset+1
                  ptBins.append(ptBinFirst)
                  ptBinOffset = 0
               else:
                  if ((ptBinFirst+ptBinOffset) == th2_slice.GetNbinsX()):
                     ptBins.remove(ptBinFirst)
                     break
                  ptBinOffset += 1
           del ptBinFirst
           del ptBinOffset

           if len(ptBins) < 2:
              ptBins = []
              print 'EMPTY'
              continue
           else:
              ptBins = sorted(list(set(ptBins)))

           print '1', ptBins

           ptBinEdges = array.array('d', [th2_slice.GetXaxis().GetBinLowEdge(_tmp) for _tmp in ptBins])

           th1_prof_name = th3_key+'_'+str(etaBins[etaBinIdx])+'_'+str(etaBins[etaBinIdx+1]-1)
           th1_prof = ROOT.TH1D(th1_prof_name, th1_prof_name, len(ptBinEdges)-1, ptBinEdges)
           th1_prof.SetDirectory(0)
           th1_prof.Reset()

           for ptIdx in range(len(ptBins)-1):
               _htmp = th2_slice.ProjectionY('_htmp'+str(ptBinEdges[ptIdx])+'_'+str(ptBinEdges[ptIdx+1]), ptBins[ptIdx], ptBins[ptIdx+1]-1, 'e')
               _htmp.SetDirectory(0)
               th1_prof.SetBinContent(ptIdx+1, _htmp.GetMean())
               th1_prof.SetBinError(ptIdx+1, _htmp.GetMeanError())
               del _htmp

           canvas = ROOT.TCanvas('c','c')
           canvas.cd()
           th1_prof.Draw('lep')

#           fit_func = ROOT.TF1('fit_func','[0]+([1]/((log10(x)^[2])+[3]))', max(10., th1_prof.GetBinLowEdge(1)), min(3000., th1_prof.GetBinLowEdge(1+th1_prof.GetNbinsX())))
#           fit_func = ROOT.TF1('fit_func','[0]+[1]*(log10(x)^[2])', max(10., th1_prof.GetBinLowEdge(1)), min(3000., th1_prof.GetBinLowEdge(1+th1_prof.GetNbinsX())))
#           fit_func = ROOT.TF1('fit_func','(x>=[6])*([0]+[1]/(pow(log10(x),2)+[2])+[3]*exp(-[4]*(log10(x)-[5])*(log10(x)-[5])))+(x<[6])*[7]', max(10., th1_prof.GetBinLowEdge(1)), min(3000., th1_prof.GetBinLowEdge(1+th1_prof.GetNbinsX())))
#           fit_func = ROOT.TF1('fit_func','[0]+((x-[1])*([2]+((x-[1])*([3]+((x-[1])*([4]+((x-[1])*([5]+((x-[1])*[6])))))))))', max(10., th1_prof.GetBinLowEdge(1)), min(3000., th1_prof.GetBinLowEdge(1+th1_prof.GetNbinsX())))
           fit_func = ROOT.TF1('fit_func','[0]+([1]*TMath::Erf([2]*log10(x)-[3]))+([4]/(pow(log10(x),2)+[5]))+([6]*exp(-[7]*pow(log10(x)-[8],2)))+([9]*exp(-[10]*pow(log10(x)-[11],2)))', max(10., th1_prof.GetBinLowEdge(1)), min(3000., th1_prof.GetBinLowEdge(1+th1_prof.GetNbinsX())))

#           fit_func.SetParameter(0, 0.1)
#           fit_func.SetParameter(1, 0.1)
#           fit_func.SetParameter(2, 0.1)
#           fit_func.SetParameter(3, 0.1)

           fit_res = th1_prof.Fit(fit_func, 'qrso')

#           print th1_prof_name, fit_func.GetParameter(0), fit_func.GetParameter(1), fit_func.GetParameter(2), fit_func.GetParameter(3)

#           fit_res.Print()

           outfilePath = OUTDIR+'/'+th1_prof.GetName()+'.png'
           if not os.path.isdir(os.path.dirname(outfilePath)):
              os.makedirs(os.path.dirname(outfilePath))

           canvas.SaveAs(outfilePath)
           canvas.Close()

#       break #!!

#
#
#   inputList = []
#   th1Keys = []
#
#       _input_pieces = _input.split(':')
#       if len(_input_pieces) >= 3:
#          print('reading..', os.path.relpath(_input_pieces[0]))
#          _tmp = {}
#          _tmp['TH1s'] = getTH1sFromTFile(_input_pieces[0], matcheKeys=MATCHES, skipKeys=SKIP, verbosity=opts.verbosity)
#          th1Keys += _tmp['TH1s'].keys()
#          _tmp['Legend'] = _input_pieces[1]
#          _tmp['LineColor'] = int(_input_pieces[2])
#          _tmp['LineStyle'] = int(_input_pieces[3]) if len(_input_pieces) >= 4 else 1
#          _tmp['MarkerStyle'] = int(_input_pieces[4]) if len(_input_pieces) >= 5 else 20
#          _tmp['MarkerColor'] = int(_input_pieces[5]) if len(_input_pieces) >= 6 else int(_input_pieces[2])
#          _tmp['MarkerSize'] = float(_input_pieces[6]) if len(_input_pieces) >= 7 else 1.0
#          inputList.append(_tmp)
#       else:
#          KILL(log_prx+'argument of --inputs has invalid format: '+_input)
#
#   if not inputList:
#      raise SystemExit(0)
#
#   th1Keys = sorted(list(set(th1Keys)))
#
#   apply_style(0)
#
#   ROOT.TGaxis.SetMaxDigits(4)
#
#   Top = ROOT.gStyle.GetPadTopMargin()
#   Rig = ROOT.gStyle.GetPadRightMargin()
#   Bot = ROOT.gStyle.GetPadBottomMargin()
#   Lef = ROOT.gStyle.GetPadLeftMargin()
#
#   ROOT.TGaxis.SetExponentOffset(-Lef+.50*Lef, 0.03, 'y')
#
#   label_sample = get_text(Lef+(1-Lef-Rig)*0.00, (1-Top)+Top*0.25, 11, .035, opts.label)
#
#   for _hkey in th1Keys:
#
#       for _keyw in KEYWORDS:
#
#           _plotConfig = getPlotConfig(key=_hkey, keyword=_keyw, inputList=inputList)
#
#           if _plotConfig is None:
#              continue
#
#           ## labels and axes titles
#           label_obj = get_text(Lef+(1-Rig-Lef)*0.95, Bot+(1-Top-Bot)*0.925, 31, .035, _plotConfig.objLabel)
#           _labels = [label_sample, label_obj]
#
#           _htitle = ';'+_plotConfig.titleX+';'+_plotConfig.titleY
#
#           ## plot
#           plot(**{
#             'histograms': _plotConfig.hists,
#             'title': _htitle,
#             'labels': _labels,
#             'legXY': [Lef+(1-Rig-Lef)*_plotConfig.legXY[0], Bot+(1-Bot-Top)*_plotConfig.legXY[1], Lef+(1-Rig-Lef)*_plotConfig.legXY[2], Bot+(1-Bot-Top)*_plotConfig.legXY[3]],
#             'outputs': [OUTDIR+'/'+_plotConfig.outputName+'.'+_tmp for _tmp in EXTS],
#             'ratio': _plotConfig.ratio,
#             'logY': _plotConfig.logY,
#             'autoRangeX': _plotConfig.autoRangeX,
#             'xLabelSize': _plotConfig.xLabelSize,
#             'xBinLabels': _plotConfig.xBinLabels,
#           })
#
#           del _plotConfig
