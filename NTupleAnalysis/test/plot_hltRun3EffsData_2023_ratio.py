#!/usr/bin/env python3
import os
import sys
import argparse
import ROOT
import math

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

COUNTER = 0
def tmpName(increment=True):
  global COUNTER
  COUNTER += 1
  return 'tmp'+str(COUNTER)

def getHistogram(tfile, key):
  h0 = tfile.Get(key)
  if not h0:
    return None

  hret = h0.Clone()
  hret.SetDirectory(0)
  hret.UseCurrentStyle()

  return hret

def getJetEfficiencies(fpath, hltThreshold_SingleJet):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)

  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'Offline',
  ]

  # SingleJet
  binEdges_pT = array.array('d', [_tmp*20 for _tmp in range(35)] + [700+_tmp*50 for _tmp in range(6+1)])
  for _tmpRef in _tmpRefs:
    jetRefCollection = 'offlineAK4PFPuppiJetsCorrected' if _tmpRef == 'Offline' else 'ak4GenJetsNoNu'
    _tmp_num = _tfile.Get('HLT_PFJet'+hltThreshold_SingleJet+'/'+jetRefCollection+'_BPix_pt0')

    _tmp_den = _tfile.Get('NoSelection/'+jetRefCollection+'_BPix_pt0')

    ret['Puppi_SingleJet_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['Puppi_SingleJet_wrt_'+_tmpRef].SetName('Puppi_SingleJet_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getHTEfficiencies(fpath, hltThreshold_HT):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'Offline',
  ]

  # HT
  binEdges_HT = array.array('d', [50.*_tmpIdx for _tmpIdx in range(44+1)])

  for _tmpRef in _tmpRefs:

    _tmp_num = _tfile.Get('HLT_PFHT'+hltThreshold_HT+'/offlineAK4PFPuppiJetsCorrected_Eta2p5_HT')

    _tmp_den = _tfile.Get('NoSelection/offlineAK4PFPuppiJetsCorrected_Eta2p5_HT')

    ret['Puppi_HT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['Puppi_HT_wrt_'+_tmpRef].SetName('Puppi_HT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getMETEfficiencies(fpath, hltThreshold_MET):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'Offline',
  ]

  for _tmpRef in _tmpRefs:

#     _tmp_num = _tfile.Get('HLT_PFMET'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFPuppiMET_Raw_pt')

#     _tmp_den = _tfile.Get('NoSelection/offlinePFPuppiMET_Raw_pt')

# #    _tmp_num = _tfile.Get('20to40_HLT/offlinePFPuppiMET_Raw_pt')
# #    _tmp_den = _tfile.Get('20to40/offlinePFPuppiMET_Raw_pt')

#     ret['PuppiMET_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
#     ret['PuppiMET_wrt_'+_tmpRef].SetName('PuppiMET_wrt_'+_tmpRef)

#     _tmp_num = _tfile.Get('HLT_PFMET'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFMET_Raw_pt')

#     _tmp_den = _tfile.Get('NoSelection/offlinePFMET_Raw_pt')

# #    _tmp_num = _tfile.Get('20to40_HLT/offlinePFMET_Raw_pt')
# #    _tmp_den = _tfile.Get('20to40/offlinePFMET_Raw_pt')

#     ret['PFMET_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
#     ret['PFMET_wrt_'+_tmpRef].SetName('PFMET_wrt_'+_tmpRef)
    
    metRefCollection = 'offlinePFPuppiMET_' if _tmpRef == 'Offline' else 'genMETTrue'
    
    # _tmp_num = _tfile.Get('HLT_PFMET'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/'+metRefCollection+'_pt')

    # _tmp_den = _tfile.Get('NoSelection/'+metRefCollection+'_pt')
    _tmp_num = _tfile.Get('HLT_PFMET'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight/'+'offlinePFPuppiMET_pt')

    _tmp_den = _tfile.Get('NoSelection/'+'offlinePFPuppiMET_pt')

    # _tmp_num = _tfile.Get('HLT_PFMETTypeOne'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFPuppiMET_Type1_pt')

    # _tmp_den = _tfile.Get('NoSelection/offlinePFPuppiMET_Type1_pt')

#    _tmp_num = _tfile.Get('20to40_HLT_TypeOne/offlinePFPuppiMET_Raw_pt')
#    _tmp_den = _tfile.Get('20to40/offlinePFPuppiMET_Raw_pt')

    ret['PuppiMETTypeOne_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PuppiMETTypeOne_wrt_'+_tmpRef].SetName('PuppiMETTypeOne_wrt_'+_tmpRef)

#     _tmp_num = _tfile.Get('HLT_PFMETTypeOne'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFMET_Type1_pt')

#     _tmp_den = _tfile.Get('NoSelection/offlinePFMET_Type1_pt')


# #    _tmp_num = _tfile.Get('20to40_HLT_TypeOne/offlinePFMET_Raw_pt')
# #    _tmp_den = _tfile.Get('20to40/offlinePFMET_Raw_pt')

#     ret['PFMETTypeOne_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
#     ret['PFMETTypeOne_wrt_'+_tmpRef].SetName('PFMETTypeOne_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

#### main
if __name__ == '__main__':
  ### args ---------------
  parser = argparse.ArgumentParser(description=__doc__)

  parser.add_argument('-i', '--input', dest='inputDir', required=True, action='store', default=None,
                      help='path to input harvesting/ directory')

  parser.add_argument('-o', '--output', dest='output', action='store', default='.',
                      help='path to output directory')

  parser.add_argument('--no-plots', dest='no_plots', action='store_true',
                      help='do not create output plots')

  parser.add_argument('--no-qcd-weighted', dest='no_qcd_weighted', action='store_true',
                      help='input histograms do not include weights for MB+QCD merging')

  parser.add_argument('--minCountsForValidRate', dest='minCountsForValidRate', action='store', type=float, default=-1.0,
                      help='minimum number of counts to consider a sample valid for trigger rate estimates')

  parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf', 'png', 'C', 'root'],
                      help='list of extension(s) for output file(s)')

  parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                      help='verbosity level')

  parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                      help='enable dry-run mode')

  opts, opts_unknown = parser.parse_known_args()
  ### --------------------

  log_prx = os.path.basename(__file__)+' -- '

  ROOT.gROOT.SetBatch() # disable interactive graphics
  ROOT.gErrorIgnoreLevel = ROOT.kError # do not display ROOT warnings

#  ROOT.TH1.AddDirectory(False)

  theStyle = get_style(0)
  theStyle.cd()

  EXTS = list(set(opts.exts))

  ### args validation ---

  inputDir = opts.inputDir
  
  recosList = ['default_eraC', 'default_eraD', 'option5_eraD']
  outputDir = opts.output
  MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

  ## SingleJet

  for _tmpJetThresh in ['60','140', '320', '500']:
    print ('='*110)
    print ('\033[1m'+_tmpJetThresh+'\033[0m')
    print ('='*110)
    print ('\033[1m'+'Jet Efficiency Plots'+'\033[0m')
    print ('='*110)

    effysJet = {}

    effysJet[_tmpJetThresh] = {}
    
    effysJet[_tmpJetThresh]['default_eraC'] = getJetEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraC/default/harvesting/data.root',
    hltThreshold_SingleJet = _tmpJetThresh,
    )

    effysJet[_tmpJetThresh]['default_eraD'] = getJetEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraD/default/harvesting/data.root',
    hltThreshold_SingleJet = _tmpJetThresh,
    )

    effysJet[_tmpJetThresh]['option5_eraD'] = getJetEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraD/option5/harvesting/data.root',
    hltThreshold_SingleJet = _tmpJetThresh,
    )

    # for _tmpReco in recosList:
    #   effysJet[_tmpJetThresh][_tmpReco] = getJetEfficiencies(
    #     fpath = inputDir+'/test_muon_data/'+_tmpReco+'/harvesting/data.root',
    #     hltThreshold_SingleJet = _tmpJetThresh,
    #   )

    for _tmpRef in [
      'Offline',
    ]:

      for _tmpType in [
        'Puppi',
      ]:
        
        XMIN = 0.2*float(_tmpJetThresh)
        XMAX = min(4.0*float(_tmpJetThresh),1000.)
        YMIN = 0.0001
        YMAX = 1.19

        canvas = ROOT.TCanvas(tmpName(), tmpName(False))
        canvas.cd()

        
        #h0 = canvas.DrawFrame(0.0*float(_tmpJetThresh), 0.0001, 1000., 1.19)

        

        #### code with ratio
        ratioPadFrac = 0.3
        pad1H = max(0.01, 1.-ratioPadFrac)

        pad1 = ROOT.TPad('pad1', 'pad1', 0, 1-pad1H, 1, 1)

        pad1.SetTopMargin(pad1.GetTopMargin()/pad1H)
        pad1.SetBottomMargin(0.02)
        pad1.SetGrid(1,1)
        pad1.SetTickx()
        pad1.SetTicky()
        #pad1.SetLogx(logX)
        #pad1.SetLogy(logY)
        pad1.Draw()

        ROOT.SetOwnership(pad1, False)

        pad1.cd()
        
        h0 = canvas.DrawFrame(XMIN, YMIN, XMAX, YMAX)

        topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
        topLabel.SetFillColor(0)
        topLabel.SetFillStyle(1001)
        topLabel.SetTextColor(ROOT.kBlack)
        topLabel.SetTextAlign(12)
        topLabel.SetTextFont(42)
        topLabel.SetTextSize(0.035)
        topLabel.SetBorderSize(0)
        topLabel.AddText('#font[61]{CMS} #font[52]{Run-3 Data} 2023')
        topLabel.Draw('same')

        objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
        objLabel.SetFillColor(0)
        objLabel.SetFillStyle(1001)
        objLabel.SetTextColor(ROOT.kBlack)
        objLabel.SetTextAlign(32)
        objLabel.SetTextFont(42)
        objLabel.SetTextSize(0.035)
        objLabel.SetBorderSize(0)
        objLabel.AddText('13.6 TeV')
        objLabel.Draw('same')

        l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.70, 0.88, 'NDC')
        l1tRateLabel.SetFillColor(0)
        l1tRateLabel.SetFillStyle(1001)
        l1tRateLabel.SetTextColor(ROOT.kBlack)
        l1tRateLabel.SetTextAlign(12)
        l1tRateLabel.SetTextFont(42)
        l1tRateLabel.SetTextSize(0.035)
        l1tRateLabel.SetBorderSize(0)
        l1tRateLabel.AddText('SingleJet'+_tmpJetThresh)
        l1tRateLabel.Draw('same')
        
        h0.GetXaxis().SetRangeUser(XMIN, XMAX)

        h0.GetYaxis().SetTitleSize(h0.GetYaxis().GetTitleSize()/pad1H)
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset()*pad1H)
        h0.GetXaxis().SetLabelSize(0)
        h0.GetYaxis().SetLabelSize(h0.GetYaxis().GetLabelSize()/pad1H)
        h0.GetXaxis().SetTickLength(h0.GetXaxis().GetTickLength()/pad1H)

        h0.SetTitle(';'+_tmpRef+' Leading Jet p_{T} [GeV];Efficiency')
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)
        
        h0.GetYaxis().SetRangeUser(YMIN, YMAX)

        try:
          effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(1)
          effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(1)
          effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerStyle(8)
          effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1.0)
          effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('ep')

          effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(2)
          effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(2)
          effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerStyle(8)
          effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1.0)
          effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('ep')

          effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(4)
          effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(4)
          effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerStyle(8)
          effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1.0)
          effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('ep')
        except: pass

        leg1 = ROOT.TLegend(0.50, 0.20, 0.84, 0.44)
        leg1.SetFillStyle(0)
        leg1.SetLineWidth(0)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.05)
        leg1.SetEntrySeparation(0.2) 
        
        
        try:
          leg1.AddEntry(effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'No BPix', 'lp')
          leg1.AddEntry(effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'BPix', 'lp')
          leg1.AddEntry(effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'BPix + doublet recovery', 'lp')
        except: pass
        leg1.Draw('same')
  
        pad1.Update()

        canvas.cd()

        pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, 1-pad1H)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(pad2.GetBottomMargin()/(1-pad1H))
        pad2.SetGrid(1,1)
        pad2.SetTickx()
        pad2.SetTicky()
        pad2.Draw()
        
        h11 = effysJet[_tmpJetThresh]['default_eraC'][_tmpType+'_SingleJet_wrt_'+_tmpRef]
        denom = h11.Clone()
        # if hasattr(denom, 'GetNbinsX'):
        #   for _tmp in range(0, denom.GetNbinsX()+2): denom.SetBinError(_tmp, 0.)
        # else:
        #    for _tmp in range(denom.GetN()):
        #        denom.SetPointEYhigh(_tmp, 0.)
        #        denom.SetPointEYlow(_tmp, 0.)

        h12 = effysJet[_tmpJetThresh]['default_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef]
        h13 = effysJet[_tmpJetThresh]['option5_eraD'][_tmpType+'_SingleJet_wrt_'+_tmpRef]
        
        #ratio_h11_h11 = h11.Clone()
        ratio_h11_h11 = get_ratio_graph(h11,denom)

        #ratio_h12_h11 = h12.Clone()
        ratio_h12_h11 = get_ratio_graph(h12,denom)

        #ratio_h13_h11 = h13.Clone()
        ratio_h13_h11 = get_ratio_graph(h13,denom)

        ROOT.SetOwnership(pad2, False)

        pad2.cd()

        h21 = pad2.DrawFrame(XMIN, 0.75, XMAX, 1.1)

        h21.SetFillStyle(3017)
        h21.SetFillColor(16)

        #h21.GetXaxis().SetTitle(title.split(';')[1])
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
        
        ratio_h11_h11.Draw('ep')
        ratio_h12_h11.Draw('same ep')
        ratio_h13_h11.Draw('same ep')
      #  h2max, h2min = None, None
      #  for _tmp in plot_ratios:
      #      if _tmp.th1 is None: continue
      #      if hasattr(_tmp.th1, 'GetNbinsX'):
      #         for _tmpb in range(1, _tmp.th1.GetNbinsX()+1):
      #             if (abs(_tmp.th1.GetBinContent(_tmpb)) > 1e-7) and (abs(_tmp.th1.GetBinError(_tmpb)) > 1e-7):
      #                h2max = max(h2max, _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)) if (h2max is not None) else _tmp.th1.GetBinContent(_tmpb)+_tmp.th1.GetBinError(_tmpb)
      #                h2min = min(h2min, _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)) if (h2min is not None) else _tmp.th1.GetBinContent(_tmpb)-_tmp.th1.GetBinError(_tmpb)
      #      else:
      #         _tmp_xyMinMax = get_xyminmax_from_graph(_tmp.th1)
      #         h2min = min(h2min, _tmp_xyMinMax[1]) if (h2min is not None) else _tmp_xyMinMax[1]
      #         h2max = max(h2max, _tmp_xyMinMax[3]) if (h2max is not None) else _tmp_xyMinMax[3]

      #  if (h2max is not None) and (h2min is not None):
      #     h2min = min(int(h2min*105.)/100., int(h2min*95.)/100.)
      #     h2max = max(int(h2max*105.)/100., int(h2max*95.)/100.)

      #     h2min = max(h2min, -5)
      #     h2max = min(h2max, 5)

      #     h21.GetYaxis().SetRangeUser(h2min, h2max)

      #  for _tmp in plot_ratios:
      #      if _tmp.th1 is not None:
      #         _tmp.th1.Draw(_tmp.draw)
      #  h21.Draw('axis,same')

        canvas.cd()
        canvas.Update()
        ###
        

        for _tmpExt in EXTS:
          canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+'_SingleJet_wrt'+_tmpRef+'_'+_tmpJetThresh+'.'+_tmpExt)

        canvas.Close()

        print ('\033[1m'+outputDir+'/triggerEff_'+_tmpType+'_SingleJet_wrt'+_tmpRef+'_'+_tmpJetThresh+'\033[0m')     
    

  ## HT
  for _tmpHTThresh in ['780', '890', '1050']:
    print ('='*110)
    print ('\033[1m'+_tmpHTThresh+'\033[0m')
    print ('='*110)
    print ('\033[1m'+'HT Efficiency Plots'+'\033[0m')
    print ('='*110)

    effysHT = {}

    effysHT[_tmpHTThresh] = {}
    
    effysHT[_tmpHTThresh]['default_eraC'] = getHTEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraC/default/harvesting/data.root',
    hltThreshold_HT = _tmpHTThresh,
    )

    effysHT[_tmpHTThresh]['default_eraD'] = getHTEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraD/default/harvesting/data.root',
    hltThreshold_HT = _tmpHTThresh,
    )

    effysHT[_tmpHTThresh]['option5_eraD'] = getHTEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraD/option5/harvesting/data.root',
    hltThreshold_HT = _tmpHTThresh,
    )

    # for _tmpReco in recosList:
    #   effysHT[_tmpHTThresh][_tmpReco] = getHTEfficiencies(
    #    fpath = inputDir+'/test_muon_data/'+_tmpReco+'/harvesting/data.root',
    #       hltThreshold_HT = _tmpHTThresh,
    #   )

    for _tmpRef in [
      'Offline',
    ]:

      for _tmpType in [
        'Puppi',
      ]:

        canvas = ROOT.TCanvas(tmpName(), tmpName(False))
        canvas.cd()

        h0 = canvas.DrawFrame(0.0*float(_tmpHTThresh), 0.0001, 1500., 1.19)

        try:
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(1)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(1)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerStyle(8)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1.0)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('ep')

  
          effysHT[_tmpHTThresh]['default_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT[_tmpHTThresh]['default_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT[_tmpHTThresh]['default_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(2)
          effysHT[_tmpHTThresh]['default_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(2)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerStyle(8)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1.0)
          effysHT[_tmpHTThresh]['default_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT[_tmpHTThresh]['default_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('ep')

          effysHT[_tmpHTThresh]['option5_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT[_tmpHTThresh]['option5_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT[_tmpHTThresh]['option5_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(4)
          effysHT[_tmpHTThresh]['option5_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(4)
          effysHT[_tmpHTThresh]['option5_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerStyle(8)
          effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1.0)
          effysHT[_tmpHTThresh]['option5_eraD'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('ep')
  
        except: pass

        topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
        topLabel.SetFillColor(0)
        topLabel.SetFillStyle(1001)
        topLabel.SetTextColor(ROOT.kBlack)
        topLabel.SetTextAlign(12)
        topLabel.SetTextFont(42)
        topLabel.SetTextSize(0.035)
        topLabel.SetBorderSize(0)
        topLabel.AddText('#font[61]{CMS} #font[52]{Run-3 Data} 2023')
        topLabel.Draw('same')

        objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
        objLabel.SetFillColor(0)
        objLabel.SetFillStyle(1001)
        objLabel.SetTextColor(ROOT.kBlack)
        objLabel.SetTextAlign(32)
        objLabel.SetTextFont(42)
        objLabel.SetTextSize(0.035)
        objLabel.SetBorderSize(0)
        objLabel.AddText('13.6 TeV')
        objLabel.Draw('same')

        l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.70, 0.88, 'NDC')
        l1tRateLabel.SetFillColor(0)
        l1tRateLabel.SetFillStyle(1001)
        l1tRateLabel.SetTextColor(ROOT.kBlack)
        l1tRateLabel.SetTextAlign(12)
        l1tRateLabel.SetTextFont(42)
        l1tRateLabel.SetTextSize(0.035)
        l1tRateLabel.SetBorderSize(0)
        l1tRateLabel.AddText('HT'+_tmpHTThresh)
        l1tRateLabel.Draw('same')

        leg1 = ROOT.TLegend(0.50, 0.20, 0.84, 0.44)
        leg1.SetFillStyle(0)
        leg1.SetLineWidth(0)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.05)
        leg1.SetEntrySeparation(0.2)
        try:
          leg1.AddEntry(effysHT[_tmpHTThresh]['default_eraC'][_tmpType+'_HT_wrt_'+_tmpRef], 'No BPix', 'lp')
          leg1.AddEntry(effysHT[_tmpHTThresh]['default_eraD'][_tmpType+'_HT_wrt_'+_tmpRef], 'BPix', 'lp')
          leg1.AddEntry(effysHT[_tmpHTThresh]['option5_eraD'][_tmpType+'_HT_wrt_'+_tmpRef], 'BPix + doublet recovery', 'lp')
          #leg1.AddEntry(effysHT[_tmpHTThresh]['test_wrongJECs'][_tmpType+'_HT_wrt_'+_tmpRef], 'HCAL update+condDB Calibs', 'lp')
          #leg1.AddEntry(effysHT[_tmpHTThresh]['default_eraD'][_tmpType+'_HT_wrt_'+_tmpRef], 'HCAL update+fixed Calibs', 'lp')
        except: pass
        leg1.Draw('same')

        h0.SetTitle(';'+_tmpRef+' H_{T} [GeV];Efficiency')
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)

        for _tmpExt in EXTS:
          canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+'_HT_wrt'+_tmpRef+'_'+_tmpHTThresh+'.'+_tmpExt)

        canvas.Close()

        print ('\033[1m'+outputDir+'/triggerEff_'+_tmpType+'_HT_wrt'+_tmpRef+'_'+_tmpHTThresh+'\033[0m')


  ## MET
  
  for _tmpMETThresh in ['120','140']:
    print ('='*110)
    print ('\033[1m'+_tmpMETThresh+'\033[0m')
    print ('='*110)
    print ('\033[1m'+'MET Efficiency Plots'+'\033[0m')
    print ('='*110)

    effysMET = {}

    effysMET[_tmpMETThresh] = {}
    
    effysMET[_tmpMETThresh]['default_eraC'] = getMETEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraC/default/harvesting/data.root',
    hltThreshold_MET = _tmpMETThresh,
    )

    effysMET[_tmpMETThresh]['default_eraD'] = getMETEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraD/default/harvesting/data.root',
    hltThreshold_MET = _tmpMETThresh,
    )

    effysMET[_tmpMETThresh]['option5_eraD'] = getMETEfficiencies(
    fpath = inputDir+'/data_BPixIssue_eraD/option5/harvesting/data.root',
    hltThreshold_MET = _tmpMETThresh,
    )

    # for _tmpReco in recosList:
    #   effysMET[_tmpMETThresh][_tmpReco] = getMETEfficiencies(
    #     fpath = inputDir+'/test_muon_data/'+_tmpReco+'/harvesting/data.root',
    #       hltThreshold_MET = _tmpMETThresh,
    #   )

    for _tmpRef in [
      'Offline',
    ]:

      for _tmpType in [
        'Puppi',
      ]:

        for _tmpAlgo in [
          'MET',
        ]:

          # MET
          canvas = ROOT.TCanvas(tmpName(), tmpName(False))
          canvas.cd()
  
          h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)
  
          try:
            effysMET[_tmpMETThresh]['default_eraC'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET[_tmpMETThresh]['default_eraC'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpMETThresh]['default_eraC'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerColor(1)
            effysMET[_tmpMETThresh]['default_eraC'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineColor(1)
            effysMET[_tmpMETThresh]['default_eraC'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET[_tmpMETThresh]['default_eraC'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].Draw('lepz')
    

            effysMET[_tmpMETThresh]['default_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET[_tmpMETThresh]['default_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpMETThresh]['default_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerColor(2)
            effysMET[_tmpMETThresh]['default_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineColor(2)
            effysMET[_tmpMETThresh]['default_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET[_tmpMETThresh]['default_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].Draw('lepz')

            effysMET[_tmpMETThresh]['option5_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET[_tmpMETThresh]['option5_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpMETThresh]['option5_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerColor(4)
            effysMET[_tmpMETThresh]['option5_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineColor(4)
            effysMET[_tmpMETThresh]['option5_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET[_tmpMETThresh]['option5_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].Draw('lepz')
    
          except: pass
  
          topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
          topLabel.SetFillColor(0)
          topLabel.SetFillStyle(1001)
          topLabel.SetTextColor(ROOT.kBlack)
          topLabel.SetTextAlign(12)
          topLabel.SetTextFont(42)
          topLabel.SetTextSize(0.035)
          topLabel.SetBorderSize(0)
          topLabel.AddText('#font[61]{CMS} #font[52]{Run-3 Data} 2023')
          topLabel.Draw('same')
  
          objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
          objLabel.SetFillColor(0)
          objLabel.SetFillStyle(1001)
          objLabel.SetTextColor(ROOT.kBlack)
          objLabel.SetTextAlign(32)
          objLabel.SetTextFont(42)
          objLabel.SetTextSize(0.035)
          objLabel.SetBorderSize(0)
          objLabel.AddText('13.6 TeV')
          objLabel.Draw('same') 

          l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.70, 0.88, 'NDC')
          l1tRateLabel.SetFillColor(0)
          l1tRateLabel.SetFillStyle(1001)
          l1tRateLabel.SetTextColor(ROOT.kBlack)
          l1tRateLabel.SetTextAlign(12)
          l1tRateLabel.SetTextFont(42)
          l1tRateLabel.SetTextSize(0.035)
          l1tRateLabel.SetBorderSize(0)
          l1tRateLabel.AddText('HLT_PF'+_tmpAlgo+_tmpMETThresh+'_PFMHT'+_tmpMETThresh+'_IDTight')
          l1tRateLabel.Draw('same')

          leg1 = ROOT.TLegend(0.50, 0.20, 0.84, 0.44)
          leg1.SetFillStyle(0)
          leg1.SetLineWidth(0)
          leg1.SetNColumns(1)
          leg1.SetTextFont(42)
          leg1.SetTextSize(0.05)
          leg1.SetEntrySeparation(0.2)
          try:
            leg1.AddEntry(effysMET[_tmpMETThresh]['default_eraC'][_tmpType+'_MET_wrt_'+_tmpRef], 'No BPix', 'lp')
            leg1.AddEntry(effysMET[_tmpMETThresh]['default_eraD'][_tmpType+'_MET_wrt_'+_tmpRef], 'BPix', 'lp')
            leg1.AddEntry(effysMET[_tmpMETThresh]['option5_eraD'][_tmpType+'_MET_wrt_'+_tmpRef], 'BPix + doublet recovery', 'lp')
            #leg1.AddEntry(effysMET[_tmpMETThresh]['test_wrongJECs'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef], 'HCAL update+condDB Calibs', 'lp')
            #leg1.AddEntry(effysMET[_tmpMETThresh]['default_eraD'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef], 'HCAL update+fixed Calibs', 'lp')
          except: pass
          leg1.Draw('same')
  
          h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];Efficiency')
          h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
  
          canvas.SetLogy(0)
          canvas.SetGrid(1, 1)
  
          for _tmpExt in EXTS:
            canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+_tmpAlgo+'_wrt'+_tmpRef+'_'+_tmpMETThresh+'.'+_tmpExt)
  
          canvas.Close()
  
          print ('\033[1m'+outputDir+'/triggerEff_'+_tmpType+_tmpAlgo+'_wrt'+_tmpRef+'_'+_tmpMETThresh+'\033[0m')
  
 