#!/usr/bin/env python
import os
import ROOT

from common.plot_style import get_style

inputDir = 'output_hltPhase2_201209_tdrDraft2_deltaR02_v2/harvesting/HLT_TRKv06p1_TICL'

outputDir = 'plots_tmp'

ROOT.gROOT.SetBatch()

theStyle = get_style(0)
theStyle.cd()

os.makedirs(outputDir)

EXTS = ['pdf']

plots = [
  {
    'output': outputDir+'/hltAK4PFPuppiJetsCorrected_EtaIncl_NotMatchedToGEN_eta',
    'templates': [
      {
        'file': inputDir+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_NoPU.root',
        'key': 'NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_NotMatchedToGEN_eta',
        'lineColor': 1,
        'lineWidth': 2,
        'drawOpt': 'hist,e0',
        'legendOpt': 'le',
        'legendName': 'NoPU',
      },
      {
        'file': inputDir+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU140.root',
        'key': 'NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_NotMatchedToGEN_eta',
        'lineColor': 2,
        'lineWidth': 2,
        'drawOpt': 'hist,e0',
        'legendOpt': 'le',
        'legendName': 'PU140',
      },
      {
        'file': inputDir+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
        'key': 'NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_NotMatchedToGEN_eta',
        'lineColor': 4,
        'lineWidth': 2,
        'drawOpt': 'hist,e0',
        'legendOpt': 'le',
        'legendName': 'PU200',
      },
    ],
    'xmin': -5,
    'xmax':  5,
    'title': ';Jet #eta;Number of jets',
    'labelTopLeft': 'QCD Flat-#hat{p}_{T} (15-3000 GeV)',
    'labelTopLeftInternal': 'HLT AK4 PF+PUPPI Jets (not Matched to GEN)',
    'labelTopRight': '14 TeV',
    'legend': [0.40, 0.50, 0.75, 0.75],
    'outputExts': EXTS,
  },
]

for _tmpPU in ['140', '200']:
  for (_tmpName1, _tmpName2) in [
    ('chargedHadronMultiplicity', 'CH-Multiplicity'),
    ('neutralHadronMultiplicity', 'NH-Multiplicity'),
    ('electronMultiplicity', 'Electron-Multiplicity'),
    ('photonMultiplicity', 'Photon-Multiplicity'),
    ('muonMultiplicity', 'Muon-Multiplicity'),
  ]:
    plots += [
      {
        'output': outputDir+'/hltAK4PFPuppiJetsCorrected_HGCalToHF_'+_tmpName1+'_PU'+_tmpPU,
        'templates': [
          {
            'file': inputDir+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU'+_tmpPU+'.root',
            'key': 'NoSelection/hltAK4PFPuppiJetsCorrected_HGCalToHF_MatchedToGEN_'+_tmpName1,
            'lineColor': 4,
            'lineWidth': 2,
            'drawOpt': 'hist,e0',
            'legendOpt': 'le',
            'legendName': 'Matched to GEN',
          },
          {
            'file': inputDir+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU'+_tmpPU+'.root',
            'key': 'NoSelection/hltAK4PFPuppiJetsCorrected_HGCalToHF_NotMatchedToGEN_'+_tmpName1,
            'lineColor': 2,
            'lineWidth': 2,
            'drawOpt': 'hist,e0',
            'legendOpt': 'le',
            'legendName': 'Not Matched to GEN',
          },
        ],
        'xmin': 0,
        'xmax': 40,
        'title': ';Jet '+_tmpName2+';Number of jets',
        'labelTopLeft': 'QCD Flat-#hat{p}_{T} (15-3000 GeV)',
        'labelTopLeftInternal': 'HLT AK4 PF+PUPPI Jets (2.8<|#eta|<3.2)',
        'labelTopRight': _tmpPU+' PU (14 TeV)',
        'legend': [0.25, 0.70, 0.85, 0.80],
        'legendColumns': 2,
        'outputExts': EXTS,
        'logY': True,
      },
    ]
  for (_tmpName1, _tmpName2) in [
    ('chargedHadronEnergyFraction', 'CH-Energy Fraction'),
    ('neutralHadronEnergyFraction', 'NH-Energy Fraction'),
    ('electronEnergyFraction', 'Electron-Energy Fraction'),
    ('photonEnergyFraction', 'Photon-Energy Fraction'),
    ('muonEnergyFraction', 'Muon-Energy Fraction'),
  ]:
    plots += [
      {
        'output': outputDir+'/hltAK4PFPuppiJetsCorrected_HGCalToHF_'+_tmpName1+'_PU'+_tmpPU,
        'templates': [
          {
            'file': inputDir+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU'+_tmpPU+'.root',
            'key': 'NoSelection/hltAK4PFPuppiJetsCorrected_HGCalToHF_MatchedToGEN_'+_tmpName1,
            'lineColor': 4,
            'lineWidth': 2,
            'drawOpt': 'hist,e0',
            'legendOpt': 'le',
            'legendName': 'Matched to GEN',
          },
          {
            'file': inputDir+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU'+_tmpPU+'.root',
            'key': 'NoSelection/hltAK4PFPuppiJetsCorrected_HGCalToHF_NotMatchedToGEN_'+_tmpName1,
            'lineColor': 2,
            'lineWidth': 2,
            'drawOpt': 'hist,e0',
            'legendOpt': 'le',
            'legendName': 'Not Matched to GEN',
          },
        ],
        'xmin': 0,
        'xmax': 1,
        'title': ';Jet '+_tmpName2+';Number of jets',
        'labelTopLeft': 'QCD Flat-#hat{p}_{T} (15-3000 GeV)',
        'labelTopLeftInternal': 'HLT AK4 PF+PUPPI Jets (2.8<|#eta|<3.2)',
        'labelTopRight': _tmpPU+' PU (14 TeV)',
        'legend': [0.25, 0.70, 0.85, 0.80],
        'legendColumns': 2,
        'outputExts': EXTS,
        'logY': True,
      },
    ]

for thePlot in plots:
  hmax = None 
  templates = []
  for theTemplate in thePlot['templates']:

    _tmpTFile = ROOT.TFile.Open(theTemplate['file'])
    if not _tmpTFile:
      templates += [None]
      continue

    _tmpKey = _tmpTFile.Get(theTemplate['key'])
    if not _tmpKey:
      templates += [None]
      continue

    _tmpKey = _tmpKey.Clone()
    _tmpKey.SetDirectory(0)
    _tmpKey.UseCurrentStyle()
    _tmpKey.SetLineColor(theTemplate.get('lineColor', 1))
    _tmpKey.SetLineStyle(theTemplate.get('lineStyle', 1))
    _tmpKey.SetLineWidth(theTemplate.get('lineWidth', 2))
    _tmpKey.SetMarkerColor(theTemplate.get('markerColor', 1))
    _tmpKey.SetMarkerStyle(theTemplate.get('markerStyle', 20))
    _tmpKey.SetMarkerSize(theTemplate.get('markerSize', 0))

    hmax = max(hmax, _tmpKey.GetMaximum()) if hmax is not None else _tmpKey.GetMaximum()

    templates += [_tmpKey]

    _tmpTFile.Close()

  if len(templates) == 0: continue

  theCanvas = ROOT.TCanvas()
  theCanvas.cd()

  h0 = theCanvas.DrawFrame(thePlot['xmin'], 1e-5, thePlot['xmax'], 1.20*hmax)

  for _tmpTemplateIdx, _tmpTemplate in enumerate(templates):
    if _tmpTemplate is None: continue
    _tmpTemplate.Draw('same,'+thePlot['templates'][_tmpTemplateIdx]['drawOpt'])

  topLabel = ROOT.TPaveText(0.14, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
# topLabel.SetFillStyle(3000)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText(thePlot['labelTopLeft'])
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.20, 0.82, 0.90, 0.88, 'NDC')
  objLabel.SetFillColor(0)
# objLabel.SetFillStyle(3000)
  objLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(11)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.0325)
  objLabel.SetBorderSize(0)
  objLabel.AddText(thePlot['labelTopLeftInternal'])
  objLabel.Draw('same')

  objLabel2 = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel2.SetFillColor(0)
# objLabel2.SetFillStyle(3000)
  objLabel2.SetTextColor(ROOT.kBlack)
  objLabel2.SetTextAlign(32)
  objLabel2.SetTextFont(42)
  objLabel2.SetTextSize(0.035)
  objLabel2.SetBorderSize(0)
  objLabel2.AddText(thePlot['labelTopRight'])
  objLabel2.Draw('same')

  leg = ROOT.TLegend(thePlot['legend'][0], thePlot['legend'][1], thePlot['legend'][2], thePlot['legend'][3])
  leg.SetNColumns(thePlot.get('legendColumns', 1))
  leg.SetTextFont(42)
  for _tmpTemplateIdx, _tmpTemplate in enumerate(templates):
    if _tmpTemplate is None: continue
    leg.AddEntry(_tmpTemplate, thePlot['templates'][_tmpTemplateIdx]['legendName'], thePlot['templates'][_tmpTemplateIdx]['legendOpt'])
  leg.Draw('same')

  h0.SetTitle(thePlot['title'])
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.1)

  if thePlot.get('logY', False):
    theCanvas.SetLogy(1)
    h0.GetYaxis().SetRangeUser(1e+0, hmax**(1./0.6))
  else:
    h0.GetYaxis().SetRangeUser(1e-4, hmax* (1./0.8))

  theCanvas.SetGrid(1, 1)

  for _ext in thePlot['outputExts']:
    theCanvas.SaveAs(thePlot['output']+'.'+_ext)

  theCanvas.Close()
