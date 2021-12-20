#!/usr/bin/env python
import argparse
import os
import fnmatch
import math
import ROOT
import sys

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

apply_style(0)

iTFile = ROOT.TFile.Open(sys.argv[1])
iTFile.cd()

oTFile = ROOT.TFile('tmp.root', 'recreate')
oTFile.cd()

for jetType in [
  'l1tAK4PF',
  'l1tAK4Puppi',
  'hltAK4PF',
  'hltAK4PFCHS',
  'hltAK4Puppi',
]:
  for jetEtaBin in [
    'EtaIncl',
    'HB',
    'HGCal',
    'HF1',
    'HF2',
  ]:
    oDirName = jetType+'_'+jetEtaBin
    oTDir = oTFile.mkdir(oDirName)
    oTDir.cd()

    pt0cumul_key = 'NoSelection/'+jetType+'JetsCorrected_'+jetEtaBin+'_pt0_cumul'
    pt0cumul0 = iTFile.Get(pt0cumul_key)
    if not pt0cumul0:
      print pt0cumul_key
      raise RuntimeError(pt0cumul_key)

    pt0cumul = pt0cumul0.Clone()
    pt0cumul.SetName('pt0_cumul')
    pt0cumul.Write()

    for jetMatchType in [
      'GEN',
    ]:
      h2map_key = 'NoSelection/'+jetType+'JetsCorrected_'+jetEtaBin+'_MatchedTo'+jetMatchType+'_pt0__vs__'+jetMatchType+'_pt'
      h2map0 = iTFile.Get(h2map_key)
      if not h2map0:
        print h2map_key

      h2map = h2map0.Clone()
      h2map.SetName(jetMatchType+'_pt2dmap')

      eff_den = h2map.ProjectionY(jetMatchType+'_eff_den', 0, -1)

      eff_num120 = h2map.ProjectionY(jetMatchType+'_eff_num120', h2map.GetXaxis().FindBin(120.), -1)
      eff_num160 = h2map.ProjectionY(jetMatchType+'_eff_num160', h2map.GetXaxis().FindBin(160.), -1)
      eff_num200 = h2map.ProjectionY(jetMatchType+'_eff_num200', h2map.GetXaxis().FindBin(200.), -1)

      eff120 = get_efficiency_graph(eff_num120, eff_den)
      eff160 = get_efficiency_graph(eff_num160, eff_den)
      eff200 = get_efficiency_graph(eff_num200, eff_den)

      eff120.SetName(jetMatchType+'_eff120')
      eff160.SetName(jetMatchType+'_eff160')
      eff200.SetName(jetMatchType+'_eff200')

      eff_num120.SetLineColor(1)
      eff_num160.SetLineColor(2)
      eff_num200.SetLineColor(4)

      eff120.SetLineColor(1)
      eff120.SetLineWidth(2)

      eff160.SetLineColor(2)
      eff160.SetLineWidth(2)

      eff200.SetLineColor(4)
      eff200.SetLineWidth(2)

      oTDir.cd()
      h2map.Write()
      eff_den.Write()
      eff_num120.Write()
      eff_num160.Write()
      eff_num200.Write()
      eff120.Write()
      eff160.Write()
      eff200.Write()
      oTDir.Close()

iTFile.Close()
oTFile.Close()
