#!/usr/bin/env python
import argparse
import os
import glob
import array
import copy
import math
import ROOT
import uproot

from common.utils import *

EvtSelections = [

  'NoSelection/',

#  'hltAK4PFCHS100_EtaIncl/',
#  'hltAK4PFCHS100_HB/',
#  'hltAK4PFCHS100_HE/',
#  'hltAK4PFCHS100_HF/',
#
#  'hltAK4Puppi100_EtaIncl/',
#  'hltAK4Puppi100_HB/',
#  'hltAK4Puppi100_HE/',
#  'hltAK4Puppi100_HF/',
#
#  'hltPFMET200/',
#  'hltPuppiMET200/',
#
#  'hltPFMETTypeOne200/',
#  'hltPuppiMETTypeOne200/',
]

GenJetsCollection = 'ak4GenJetsNoNu'

JetCollections = [

  GenJetsCollection,
  'hltAK4CaloJets',
  'hltAK4CaloJetsCorrected',
#  'hltAK8CaloJets',
#  'hltAK8CaloJetsCorrected',
  'hltAK4PFJets',
  'hltAK4PFJetsCorrected',
#  'hltAK8PFJets',
#  'hltAK8PFJetsCorrected',
]

JetOnlineOfflinePairs = [
]

METCollections = [

  'genMETTrue',

  'hltPFMET',
#  'hltPFMETTypeOne',
]

METOnlineOfflinePairs = [
]

def delta_phi(phi1, phi2):
    ret = phi1 - phi2
    if ret >  math.pi: ret -= math.pi*2
    if ret < -math.pi: ret += math.pi*2
    return ret

#### Histograms --------------------------------------------------------------------------------------------------------------------

def create_histograms():

    # bin-edges for TH1Ds and TH2Ds
    binEdges_1d = {}
    binEdges_2d = {}

    for i_sel in EvtSelections:

        binEdges_1d[i_sel+'hltTrimmedPixelVertices_mult'] = [10*_tmp for _tmp in range(40+1)]
        binEdges_1d[i_sel+'hltVerticesPF_mult'] = [10*_tmp for _tmp in range(40+1)]

        ### Jets
        for i_jet in JetCollections:

            for i_reg in ['_EtaIncl', '_HB', '_HE', '_HF']:

                binEdges_1d[i_sel+i_jet+i_reg+'_njets'] = [_tmp for _tmp in range(121)]
                binEdges_1d[i_sel+i_jet+i_reg+'_pt']  = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000]
                binEdges_1d[i_sel+i_jet+i_reg+'_pt0'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000]
                binEdges_1d[i_sel+i_jet+i_reg+'_eta'] = [-5.0+0.1*_tmp for _tmp in range(100)]
                binEdges_1d[i_sel+i_jet+i_reg+'_phi'] = [math.pi*(2./40*_tmp-1) for _tmp in range(40+1)]
                binEdges_1d[i_sel+i_jet+i_reg+'_mass'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600]

                binEdges_2d[i_sel+i_jet+i_reg+'_pt:'+i_jet+i_reg+'_eta'] = [binEdges_1d[i_sel+i_jet+i_reg+'_pt'], binEdges_1d[i_sel+i_jet+i_reg+'_eta']]

#                binEdges_1d[i_sel+i_jet+i_reg+'_chargedHadronEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_neutralHadronEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_electronEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_photonEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_muonEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#
#                binEdges_1d[i_sel+i_jet+i_reg+'_chargedHadronMultiplicity'] = [_tmp for _tmp in range(61)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_neutralHadronMultiplicity'] = [_tmp for _tmp in range(61)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_electronMultiplicity'] = [_tmp for _tmp in range(13)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_photonMultiplicity'] = [_tmp for _tmp in range(61)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_muonMultiplicity'] = [_tmp for _tmp in range(13)]

                if i_jet == GenJetsCollection: continue

                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_njets'] = [_tmp for _tmp in range(121)]
                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt'] = binEdges_1d[i_sel+i_jet+i_reg+'_pt']
                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt0'] = binEdges_1d[i_sel+i_jet+i_reg+'_pt0']
                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_eta'] = binEdges_1d[i_sel+i_jet+i_reg+'_eta']
                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_phi'] = binEdges_1d[i_sel+i_jet+i_reg+'_phi']
                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_mass'] = binEdges_1d[i_sel+i_jet+i_reg+'_mass']

#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_chargedHadronEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_neutralHadronEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_electronEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_photonEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_muonEnergyFraction'] = [_tmp*0.05 for _tmp in range(41)]
#
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_chargedHadronMultiplicity'] = [_tmp for _tmp in range(61)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_neutralHadronMultiplicity'] = [_tmp for _tmp in range(61)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_electronMultiplicity'] = [_tmp for _tmp in range(13)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_photonMultiplicity'] = [_tmp for _tmp in range(61)]
#                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_muonMultiplicity'] = [_tmp for _tmp in range(13)]

                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_dRmatch'] = [0.2*_tmp for _tmp in range(25+1)]

                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_mass_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]

                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
                binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt_minusGEN']  = [-250+10*_tmp for _tmp in range(50+1)]

                binEdges_1d[i_sel+i_jet+i_reg+'_NotMatchedToGEN_njets'] = [_tmp for _tmp in range(121)]
                binEdges_1d[i_sel+i_jet+i_reg+'_NotMatchedToGEN_pt'] = binEdges_1d[i_sel+i_jet+i_reg+'_pt']
                binEdges_1d[i_sel+i_jet+i_reg+'_NotMatchedToGEN_pt0'] = binEdges_1d[i_sel+i_jet+i_reg+'_pt0']
                binEdges_1d[i_sel+i_jet+i_reg+'_NotMatchedToGEN_eta'] = binEdges_1d[i_sel+i_jet+i_reg+'_eta']
                binEdges_1d[i_sel+i_jet+i_reg+'_NotMatchedToGEN_phi'] = binEdges_1d[i_sel+i_jet+i_reg+'_phi']
                binEdges_1d[i_sel+i_jet+i_reg+'_NotMatchedToGEN_mass'] = binEdges_1d[i_sel+i_jet+i_reg+'_mass']

                for v_ref in [GenJetsCollection+'_EtaIncl_pt', GenJetsCollection+'_EtaIncl_eta']:

                    if v_ref == GenJetsCollection+'_EtaIncl_pt':
                       binEdges_2d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt'], binEdges_1d[i_sel+v_ref]]
                       binEdges_2d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt0:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt0'], binEdges_1d[i_sel+v_ref]]

                    if v_ref == GenJetsCollection+'_EtaIncl_eta':
                       binEdges_2d[i_sel+i_jet+i_reg+'_MatchedToGEN_eta:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_eta'], binEdges_1d[i_sel+v_ref]]

                    binEdges_2d[i_sel+i_jet+i_reg+'_MatchedToGEN_mass_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_mass_overGEN'], binEdges_1d[i_sel+v_ref]]
                    binEdges_2d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt_overGEN'], binEdges_1d[i_sel+v_ref]]
                    binEdges_2d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt_minusGEN:'+v_ref] = [binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_pt_minusGEN'], binEdges_1d[i_sel+v_ref]]

                binEdges_2d[i_sel+i_jet+i_reg+'_MatchedToGEN_mass_overGEN:'+GenJetsCollection+'_EtaIncl_mass'] = \
                  [binEdges_1d[i_sel+i_jet+i_reg+'_MatchedToGEN_mass_overGEN'], binEdges_1d[i_sel+GenJetsCollection+'_EtaIncl_mass']]

        for [i_jet_onl, i_jet_off] in JetOnlineOfflinePairs:

            for i_reg in ['_EtaIncl', '_HB', '_HE', '_HF']:

                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_njets'] = [_tmp for _tmp in range(121)]
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt'] = binEdges_1d[i_sel+i_jet_onl+i_reg+'_pt']
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt0'] = binEdges_1d[i_sel+i_jet_onl+i_reg+'_pt0']
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_eta'] = binEdges_1d[i_sel+i_jet_onl+i_reg+'_eta']
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_phi'] = binEdges_1d[i_sel+i_jet_onl+i_reg+'_phi']
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_mass'] = binEdges_1d[i_sel+i_jet_onl+i_reg+'_mass']
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_dRmatch'] = [0.2*_tmp for _tmp in range(25+1)]

                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]
                binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt_minusOffline']  = [-250+10*_tmp for _tmp in range(50+1)]

                for v_ref in [i_jet_off+'_EtaIncl_pt', i_jet_off+'_EtaIncl_eta']:

                    if v_ref == i_jet_off+'_EtaIncl_pt':
                       binEdges_2d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt:'+v_ref] = [binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt'], binEdges_1d[i_sel+v_ref]]
                       binEdges_2d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt0:'+v_ref] = [binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt0'], binEdges_1d[i_sel+v_ref]]

                    if v_ref == i_jet_off+'_EtaIncl_eta':
                       binEdges_2d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_eta:'+v_ref] = [binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_eta'], binEdges_1d[i_sel+v_ref]]

                    binEdges_2d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt_overOffline:'+v_ref] = [binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt_overOffline'], binEdges_1d[i_sel+v_ref]]
                    binEdges_2d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt_minusOffline:'+v_ref] = [binEdges_1d[i_sel+i_jet_onl+i_reg+'_MatchedToOffline_pt_minusOffline'], binEdges_1d[i_sel+v_ref]]

        ### MET
        for i_met in METCollections:

            binEdges_1d[i_sel+i_met+'_pt'] = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000]
            binEdges_1d[i_sel+i_met+'_phi'] = [math.pi*(2./40*_tmp-1) for _tmp in range(40+1)]
            binEdges_1d[i_sel+i_met+'_sumEt'] = [0, 30, 60, 90, 120, 180, 250, 400, 600, 800, 1000, 1500, 2000, 3000]

            for i_var in ['pt', 'phi', 'sumEt']:
                binEdges_2d[i_sel+i_met+'_'+i_var+':hltTrimmedPixelVertices_mult'] = [binEdges_1d[i_sel+i_met+'_'+i_var], binEdges_1d[i_sel+'hltTrimmedPixelVertices_mult']]
                binEdges_2d[i_sel+i_met+'_'+i_var+':hltVerticesPF_mult'] = [binEdges_1d[i_sel+i_met+'_'+i_var], binEdges_1d[i_sel+'hltVerticesPF_mult']]

            if i_met == 'genMETTrue': continue

            binEdges_1d[i_sel+i_met+'_pt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met+'_phi_minusGEN'] = [math.pi/40*_tmp for _tmp in range(40+1)]
            binEdges_1d[i_sel+i_met+'_sumEt_minusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]

            binEdges_1d[i_sel+i_met+'_pt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met+'_phi_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met+'_sumEt_overGEN'] = [0.1*_tmp for _tmp in range(50+1)]

            binEdges_1d[i_sel+i_met+'_pt_paraToGEN'] = [-200+10*_tmp for _tmp in range(60+1)]
            binEdges_1d[i_sel+i_met+'_pt_paraToGENMinusGEN'] = [-250+10*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met+'_pt_perpToGEN'] = [-200+10*_tmp for _tmp in range(60+1)]

            for v_ref in ['genMETTrue_pt', 'genMETTrue_sumEt', 'hltVerticesPF_mult']:

                binEdges_2d[i_sel+i_met+'_pt:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_phi:'+v_ref] = [binEdges_1d[i_sel+i_met+'_phi'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_sumEt:'+v_ref] = [binEdges_1d[i_sel+i_met+'_sumEt'], binEdges_1d[i_sel+v_ref]]

                binEdges_2d[i_sel+i_met+'_pt_minusGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_minusGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_phi_minusGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_phi_minusGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_sumEt_minusGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_sumEt_minusGEN'], binEdges_1d[i_sel+v_ref]]

                binEdges_2d[i_sel+i_met+'_pt_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_overGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_phi_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_phi_overGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_sumEt_overGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_sumEt_overGEN'], binEdges_1d[i_sel+v_ref]]

                binEdges_2d[i_sel+i_met+'_pt_paraToGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_paraToGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_pt_paraToGENMinusGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_paraToGENMinusGEN'], binEdges_1d[i_sel+v_ref]]
                binEdges_2d[i_sel+i_met+'_pt_perpToGEN:'+v_ref] = [binEdges_1d[i_sel+i_met+'_pt_perpToGEN'], binEdges_1d[i_sel+v_ref]]

        for [i_met_onl, i_met_off] in METOnlineOfflinePairs:

            binEdges_1d[i_sel+i_met_onl+'_pt_minusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met_onl+'_phi_minusOffline'] = [math.pi/40*_tmp for _tmp in range(40+1)]
            binEdges_1d[i_sel+i_met_onl+'_sumEt_minusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]

            binEdges_1d[i_sel+i_met_onl+'_pt_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met_onl+'_phi_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met_onl+'_sumEt_overOffline'] = [0.1*_tmp for _tmp in range(50+1)]

            binEdges_1d[i_sel+i_met_onl+'_pt_paraToOffline'] = [-200+10*_tmp for _tmp in range(60+1)]
            binEdges_1d[i_sel+i_met_onl+'_pt_paraToOfflineMinusOffline'] = [-250+10*_tmp for _tmp in range(50+1)]
            binEdges_1d[i_sel+i_met_onl+'_pt_perpToOffline'] = [-200+10*_tmp for _tmp in range(60+1)]

            binEdges_2d[i_sel+i_met_onl+'_pt:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_pt_minusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_minusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_pt_overOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_overOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]

            binEdges_2d[i_sel+i_met_onl+'_sumEt:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_sumEt_minusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt_minusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_sumEt_overOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_sumEt_overOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]

            binEdges_2d[i_sel+i_met_onl+'_pt_paraToOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_paraToOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_pt_paraToOfflineMinusOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_paraToOfflineMinusOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]
            binEdges_2d[i_sel+i_met_onl+'_pt_perpToOffline:'+i_met_off+'_pt'] = [binEdges_1d[i_sel+i_met_onl+'_pt_perpToOffline'], binEdges_1d[i_sel+i_met_off+'_pt']]

    th1s = {}
    for h_name in binEdges_1d:
        th1s[h_name] = create_TH1D(h_name, binEdges_1d[h_name])

    th2s = {}
    for h_name in binEdges_2d:
        th2s[h_name] = create_TH2D(h_name, binEdges_2d[h_name])

    return th1s, th2s

def create_TH1D(name, binEdges):

    _binEdges_array = array.array('d', sorted(list(set(binEdges))))

    _th1d = ROOT.TH1D(name, name, len(_binEdges_array)-1, _binEdges_array)
    _th1d.SetDirectory(0)
    _th1d.Sumw2()

    return _th1d

def create_TH2D(name, binEdges):

    _binEdgesX_array = array.array('d', sorted(list(set(binEdges[0]))))
    _binEdgesY_array = array.array('d', sorted(list(set(binEdges[1]))))

    _th2d = ROOT.TH2D(name, name, len(_binEdgesX_array)-1, _binEdgesX_array, len(_binEdgesY_array)-1, _binEdgesY_array)
    _th2d.SetDirectory(0)
    _th2d.Sumw2()

    return _th2d

#### Event Analysis ----------------------------------------------------------------------------------------------------------------

def jetMatchingIndices(arrays, index, jetColl1, jetColl2, jetPtMin1, jetPtMin2, maxDeltaR):

    _ret = []

    maxDeltaR2 = maxDeltaR*maxDeltaR

    njets1 = len(arrays[jetColl1+'_pt'][index])
    njets2 = len(arrays[jetColl2+'_pt'][index])

    for jet1_idx in range(njets1):

        bestMatch_idx = None
        bestMatch_dR2 = -1

        jet1_pt  = arrays[jetColl1+'_pt'] [index][jet1_idx]
        jet1_eta = arrays[jetColl1+'_eta'][index][jet1_idx]
        jet1_phi = arrays[jetColl1+'_phi'][index][jet1_idx]

        if jet1_pt >= jetPtMin1:

           for jet2_idx in range(njets2):

               jet2_pt  = arrays[jetColl2+'_pt'] [index][jet2_idx]
               jet2_eta = arrays[jetColl2+'_eta'][index][jet2_idx]
               jet2_phi = arrays[jetColl2+'_phi'][index][jet2_idx]

               if jet2_pt < jetPtMin2: continue

               dEta = jet1_eta - jet2_eta
               dPhi = delta_phi(jet1_phi, jet2_phi)
               dR2 = dEta*dEta + dPhi*dPhi

               if (dR2 < maxDeltaR2):
                  if (bestMatch_idx is None) or (dR2 < bestMatch_dR2):
                     bestMatch_idx = jet2_idx
                     bestMatch_dR2 = dR2

        _ret.append(bestMatch_idx)

    return _ret

def analyze_event(arrays, index, th1s={}, th2s={}, verbose=False):

    values = {}

    GenJet_minPt = 25.
    RecoJet_minPt = 30.

    ## Event Values

    values['hltTrimmedPixelVertices_mult'] = len(arrays['hltTrimmedPixelVertices_z'][index])
    values['hltVerticesPF_mult'] = len(arrays['hltVerticesPF_z'][index])

    ## Jets

    # indeces for matching objects in different Jet collections
    jetMatchingIndices_dict = {}

    for i_jet in JetCollections:
        if i_jet == GenJetsCollection: continue

        if i_jet not in jetMatchingIndices_dict:
           jetMatchingIndices_dict[i_jet] = {}

        if GenJetsCollection in jetMatchingIndices_dict[i_jet]:
           KILL('mmm1')

        jetMatchingIndices_dict[i_jet][GenJetsCollection] = jetMatchingIndices(
          arrays=arrays, index=index, jetColl1=i_jet, jetColl2=GenJetsCollection, jetPtMin1=RecoJet_minPt, jetPtMin2=GenJet_minPt, maxDeltaR=0.1,
        )

    for [i_onlineJetColl, i_offlineJetColl] in JetOnlineOfflinePairs:

        if i_onlineJetColl not in jetMatchingIndices_dict:
           jetMatchingIndices_dict[i_onlineJetColl] = {}

        if i_offlineJetColl in jetMatchingIndices_dict[i_onlineJetColl]:
           KILL('mmm2')

        jetMatchingIndices_dict[i_onlineJetColl][i_offlineJetColl] = jetMatchingIndices(
          arrays=arrays, index=index, jetColl1=i_onlineJetColl, jetColl2=i_offlineJetColl, jetPtMin1=RecoJet_minPt, jetPtMin2=RecoJet_minPt, maxDeltaR=0.1,
        )

    # Jets: all collections + Reco-to-GEN matching
    for i_jet in JetCollections:

        # initialize value lists
        for i_reg in ['_EtaIncl', '_HB', '_HE', '_HF']:
            _tmp_vlist = [
              i_jet+i_reg+'_pt',
              i_jet+i_reg+'_eta',
              i_jet+i_reg+'_phi',
              i_jet+i_reg+'_mass',
#              i_jet+i_reg+'_chargedHadronEnergyFraction',
#              i_jet+i_reg+'_neutralHadronEnergyFraction',
#              i_jet+i_reg+'_electronEnergyFraction',
#              i_jet+i_reg+'_photonEnergyFraction',
#              i_jet+i_reg+'_muonEnergyFraction',
#              i_jet+i_reg+'_chargedHadronMultiplicity',
#              i_jet+i_reg+'_neutralHadronMultiplicity',
#              i_jet+i_reg+'_electronMultiplicity',
#              i_jet+i_reg+'_photonMultiplicity',
#              i_jet+i_reg+'_muonMultiplicity',
            ]

            if i_jet != GenJetsCollection:
               _tmp_vlist += [
                 i_jet+i_reg+'_MatchedToGEN_pt',
                 i_jet+i_reg+'_MatchedToGEN_eta',
                 i_jet+i_reg+'_MatchedToGEN_phi',
                 i_jet+i_reg+'_MatchedToGEN_mass',
                 i_jet+i_reg+'_MatchedToGEN_mass_overGEN',
                 i_jet+i_reg+'_MatchedToGEN_mass_overGEN:' +GenJetsCollection+'_EtaIncl_pt',
                 i_jet+i_reg+'_MatchedToGEN_mass_overGEN:' +GenJetsCollection+'_EtaIncl_eta',
                 i_jet+i_reg+'_MatchedToGEN_mass_overGEN:' +GenJetsCollection+'_EtaIncl_mass',
#                 i_jet+i_reg+'_MatchedToGEN_chargedHadronEnergyFraction',
#                 i_jet+i_reg+'_MatchedToGEN_neutralHadronEnergyFraction',
#                 i_jet+i_reg+'_MatchedToGEN_electronEnergyFraction',
#                 i_jet+i_reg+'_MatchedToGEN_photonEnergyFraction',
#                 i_jet+i_reg+'_MatchedToGEN_muonEnergyFraction',
#                 i_jet+i_reg+'_MatchedToGEN_chargedHadronMultiplicity',
#                 i_jet+i_reg+'_MatchedToGEN_neutralHadronMultiplicity',
#                 i_jet+i_reg+'_MatchedToGEN_electronMultiplicity',
#                 i_jet+i_reg+'_MatchedToGEN_photonMultiplicity',
#                 i_jet+i_reg+'_MatchedToGEN_muonMultiplicity',
                 i_jet+i_reg+'_MatchedToGEN_dRmatch',
                 i_jet+i_reg+'_MatchedToGEN_pt_overGEN',
                 i_jet+i_reg+'_MatchedToGEN_pt_minusGEN',
                 i_jet+i_reg+'_MatchedToGEN_pt:'         +GenJetsCollection+'_EtaIncl_pt',
                 i_jet+i_reg+'_MatchedToGEN_pt_overGEN:' +GenJetsCollection+'_EtaIncl_pt',
                 i_jet+i_reg+'_MatchedToGEN_pt_minusGEN:'+GenJetsCollection+'_EtaIncl_pt',
                 i_jet+i_reg+'_MatchedToGEN_eta:'        +GenJetsCollection+'_EtaIncl_eta',
                 i_jet+i_reg+'_MatchedToGEN_pt_overGEN:' +GenJetsCollection+'_EtaIncl_eta',
                 i_jet+i_reg+'_MatchedToGEN_pt_minusGEN:'+GenJetsCollection+'_EtaIncl_eta',
                 i_jet+i_reg+'_NotMatchedToGEN_pt',
                 i_jet+i_reg+'_NotMatchedToGEN_eta',
                 i_jet+i_reg+'_NotMatchedToGEN_phi',
                 i_jet+i_reg+'_NotMatchedToGEN_mass',
               ]

            for _tmp in _tmp_vlist:
                if _tmp in values:
                   KILL('analyze_event -- logic error: attempting to re-initialize value list: '+_tmp)
                else:
                   values[_tmp] = []

        n_jets = len(arrays[i_jet+'_pt'][index])

        for jet_idx in range(n_jets):
            jet_pt = arrays[i_jet+'_pt'][index][jet_idx]
            jet_eta = arrays[i_jet+'_eta'][index][jet_idx]
            jet_phi = arrays[i_jet+'_phi'][index][jet_idx]
            jet_mass = arrays[i_jet+'_mass'][index][jet_idx]
#            jet_chargedHadronEnergyFraction = arrays[i_jet+'_chargedHadronEnergyFraction'][index][jet_idx]
#            jet_neutralHadronEnergyFraction = arrays[i_jet+'_neutralHadronEnergyFraction'][index][jet_idx]
#            jet_electronEnergyFraction = arrays[i_jet+'_electronEnergyFraction'][index][jet_idx]
#            jet_photonEnergyFraction = arrays[i_jet+'_photonEnergyFraction'][index][jet_idx]
#            jet_muonEnergyFraction = arrays[i_jet+'_muonEnergyFraction'][index][jet_idx]
#            jet_chargedHadronMultiplicity = arrays[i_jet+'_chargedHadronMultiplicity'][index][jet_idx]
#            jet_neutralHadronMultiplicity = arrays[i_jet+'_neutralHadronMultiplicity'][index][jet_idx]
#            jet_electronMultiplicity = arrays[i_jet+'_electronMultiplicity'][index][jet_idx]
#            jet_photonMultiplicity = arrays[i_jet+'_photonMultiplicity'][index][jet_idx]
#            jet_muonMultiplicity = arrays[i_jet+'_muonMultiplicity'][index][jet_idx]

            if (jet_pt < (GenJet_minPt if (i_jet == GenJetsCollection) else RecoJet_minPt)): continue

            jet_labels = ['_EtaIncl']
            if abs(jet_eta) < 1.5: jet_labels += ['_HB']
            elif abs(jet_eta) < 3.0: jet_labels += ['_HE']
            else: jet_labels += ['_HF']

            for i_reg in jet_labels:
                values[i_jet+i_reg+'_pt'] += [jet_pt]
                values[i_jet+i_reg+'_eta'] += [jet_eta]
                values[i_jet+i_reg+'_phi'] += [jet_phi]
                values[i_jet+i_reg+'_mass'] += [jet_mass]
#                values[i_jet+i_reg+'_chargedHadronEnergyFraction'] += [jet_chargedHadronEnergyFraction]
#                values[i_jet+i_reg+'_neutralHadronEnergyFraction'] += [jet_neutralHadronEnergyFraction]
#                values[i_jet+i_reg+'_electronEnergyFraction'] += [jet_electronEnergyFraction]
#                values[i_jet+i_reg+'_photonEnergyFraction'] += [jet_photonEnergyFraction]
#                values[i_jet+i_reg+'_muonEnergyFraction'] += [jet_muonEnergyFraction]
#                values[i_jet+i_reg+'_chargedHadronMultiplicity'] += [jet_chargedHadronMultiplicity]
#                values[i_jet+i_reg+'_neutralHadronMultiplicity'] += [jet_neutralHadronMultiplicity]
#                values[i_jet+i_reg+'_electronMultiplicity'] += [jet_electronMultiplicity]
#                values[i_jet+i_reg+'_photonMultiplicity'] += [jet_photonMultiplicity]
#                values[i_jet+i_reg+'_muonMultiplicity'] += [jet_muonMultiplicity]

                if i_jet == GenJetsCollection: continue

                genJet_match = jetMatchingIndices_dict[i_jet][GenJetsCollection][jet_idx]

                if genJet_match is not None:

                   genJet_match_pt = arrays[GenJetsCollection+'_pt'][index][genJet_match]
                   genJet_match_eta = arrays[GenJetsCollection+'_eta'][index][genJet_match]
                   genJet_match_phi = arrays[GenJetsCollection+'_phi'][index][genJet_match]
                   genJet_match_mass = arrays[GenJetsCollection+'_mass'][index][genJet_match]

                   recoGen_dEta = jet_eta - genJet_match_eta
                   recoGen_dPhi = delta_phi(jet_phi, genJet_match_phi)
                   recoGen_dRmatch = math.sqrt(recoGen_dEta*recoGen_dEta + recoGen_dPhi*recoGen_dPhi)

                   values[i_jet+i_reg+'_MatchedToGEN_pt'] += [jet_pt]
                   values[i_jet+i_reg+'_MatchedToGEN_eta'] += [jet_eta]
                   values[i_jet+i_reg+'_MatchedToGEN_phi'] += [jet_phi]
                   values[i_jet+i_reg+'_MatchedToGEN_mass'] += [jet_mass]
#                   values[i_jet+i_reg+'_MatchedToGEN_chargedHadronEnergyFraction'] += [jet_chargedHadronEnergyFraction]
#                   values[i_jet+i_reg+'_MatchedToGEN_neutralHadronEnergyFraction'] += [jet_neutralHadronEnergyFraction]
#                   values[i_jet+i_reg+'_MatchedToGEN_electronEnergyFraction'] += [jet_electronEnergyFraction]
#                   values[i_jet+i_reg+'_MatchedToGEN_photonEnergyFraction'] += [jet_photonEnergyFraction]
#                   values[i_jet+i_reg+'_MatchedToGEN_muonEnergyFraction'] += [jet_muonEnergyFraction]
#                   values[i_jet+i_reg+'_MatchedToGEN_chargedHadronMultiplicity'] += [jet_chargedHadronMultiplicity]
#                   values[i_jet+i_reg+'_MatchedToGEN_neutralHadronMultiplicity'] += [jet_neutralHadronMultiplicity]
#                   values[i_jet+i_reg+'_MatchedToGEN_electronMultiplicity'] += [jet_electronMultiplicity]
#                   values[i_jet+i_reg+'_MatchedToGEN_photonMultiplicity'] += [jet_photonMultiplicity]
#                   values[i_jet+i_reg+'_MatchedToGEN_muonMultiplicity'] += [jet_muonMultiplicity]
                   values[i_jet+i_reg+'_MatchedToGEN_dRmatch'] += [recoGen_dRmatch]

                   if genJet_match_pt != 0:
                      values[i_jet+i_reg+'_MatchedToGEN_pt_overGEN']  += [jet_pt / genJet_match_pt]
                      values[i_jet+i_reg+'_MatchedToGEN_pt_minusGEN'] += [jet_pt - genJet_match_pt]

                      values[i_jet+i_reg+'_MatchedToGEN_pt:'         +GenJetsCollection+'_EtaIncl_pt'] += [(jet_pt,  genJet_match_pt)]
                      values[i_jet+i_reg+'_MatchedToGEN_pt_overGEN:' +GenJetsCollection+'_EtaIncl_pt'] += [(jet_pt / genJet_match_pt, genJet_match_pt)]
                      values[i_jet+i_reg+'_MatchedToGEN_pt_minusGEN:'+GenJetsCollection+'_EtaIncl_pt'] += [(jet_pt - genJet_match_pt, genJet_match_pt)]

                      values[i_jet+i_reg+'_MatchedToGEN_eta:'        +GenJetsCollection+'_EtaIncl_eta'] += [(jet_eta, genJet_match_eta)]
                      values[i_jet+i_reg+'_MatchedToGEN_pt_overGEN:' +GenJetsCollection+'_EtaIncl_eta'] += [(jet_pt / genJet_match_pt, genJet_match_eta)]
                      values[i_jet+i_reg+'_MatchedToGEN_pt_minusGEN:'+GenJetsCollection+'_EtaIncl_eta'] += [(jet_pt - genJet_match_pt, genJet_match_eta)]

                      values[i_jet+i_reg+'_MatchedToGEN_mass_overGEN'] += [jet_mass / genJet_match_mass]
                      values[i_jet+i_reg+'_MatchedToGEN_mass_overGEN:'+GenJetsCollection+'_EtaIncl_pt'] += [(jet_mass / genJet_match_mass, genJet_match_pt)]
                      values[i_jet+i_reg+'_MatchedToGEN_mass_overGEN:'+GenJetsCollection+'_EtaIncl_eta'] += [(jet_mass / genJet_match_mass, genJet_match_eta)]
                      values[i_jet+i_reg+'_MatchedToGEN_mass_overGEN:'+GenJetsCollection+'_EtaIncl_mass'] += [(jet_mass / genJet_match_mass, genJet_match_mass)]

                else:
                   values[i_jet+i_reg+'_NotMatchedToGEN_pt'] += [jet_pt]
                   values[i_jet+i_reg+'_NotMatchedToGEN_eta'] += [jet_eta]
                   values[i_jet+i_reg+'_NotMatchedToGEN_phi'] += [jet_phi]
                   values[i_jet+i_reg+'_NotMatchedToGEN_mass'] += [jet_mass]

        njets_tags = ['_EtaIncl', '_HB', '_HE', '_HF']
        if (i_jet != GenJetsCollection):
           njets_tags += ['_EtaIncl_MatchedToGEN', '_HB_MatchedToGEN', '_HE_MatchedToGEN', '_HF_MatchedToGEN']
           njets_tags += ['_EtaIncl_NotMatchedToGEN', '_HB_NotMatchedToGEN', '_HE_NotMatchedToGEN', '_HF_NotMatchedToGEN']

        for i_jettag in njets_tags:
            values[i_jet+i_jettag+'_njets'] = len(values[i_jet+i_jettag+'_pt']) if (i_jet+i_jettag+'_pt' in values) else 0

            if len(values[i_jet+i_jettag+'_pt']) > 0:
               values[i_jet+i_jettag+'_pt0'] = max(values[i_jet+i_jettag+'_pt'])

            if (i_jet+i_jettag+'_pt:'+GenJetsCollection+'_EtaIncl_pt' in values) and (len(values[i_jet+i_jettag+'_pt:'+GenJetsCollection+'_EtaIncl_pt']) > 0):
               values[i_jet+i_jettag+'_pt0:'+GenJetsCollection+'_EtaIncl_pt'] = sorted(values[i_jet+i_jettag+'_pt:'+GenJetsCollection+'_EtaIncl_pt'], key=lambda x : x[0], reverse=True)[0]

    # Jets: Online-to-Offline matching
    for [i_onlineJetColl, i_offlineJetColl] in JetOnlineOfflinePairs:

        # initialize value-lists
        for i_onlineJetReg in ['_EtaIncl', '_HB', '_HE', '_HF']:
            for _tmp in [
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_eta',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_phi',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_mass',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_dRmatch',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_overOffline',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_minusOffline',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt:'+i_offlineJetColl+'_EtaIncl_pt',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_eta:'+i_offlineJetColl+'_EtaIncl_eta',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_overOffline:'+i_offlineJetColl+'_EtaIncl_pt',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_overOffline:'+i_offlineJetColl+'_EtaIncl_eta',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_minusOffline:'+i_offlineJetColl+'_EtaIncl_pt',
              i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_minusOffline:'+i_offlineJetColl+'_EtaIncl_eta',
            ]:
              if _tmp in values:
                 KILL('analyze_event -- logic error: attempting to re-initialize value list: '+_tmp)
              else:
                 values[_tmp] = []

        n_onlineJets = len(arrays[i_onlineJetColl+'_pt'][index])

        for onlineJet_idx in range(n_onlineJets):
            onlineJet_pt = arrays[i_onlineJetColl+'_pt'][index][onlineJet_idx]
            onlineJet_eta = arrays[i_onlineJetColl+'_eta'][index][onlineJet_idx]
            onlineJet_phi = arrays[i_onlineJetColl+'_phi'][index][onlineJet_idx]
            onlineJet_mass = arrays[i_onlineJetColl+'_mass'][index][onlineJet_idx]

            if (onlineJet_pt < RecoJet_minPt): continue

            onlineJet_labels = ['_EtaIncl']
            if abs(onlineJet_eta) < 1.5: onlineJet_labels += ['_HB']
            elif abs(onlineJet_eta) < 3.0: onlineJet_labels += ['_HE']
            else: onlineJet_labels += ['_HF']

            for i_onlineJetReg in onlineJet_labels:

                offlineJet_match = jetMatchingIndices_dict[i_onlineJetColl][i_offlineJetColl][onlineJet_idx]

                if offlineJet_match is not None:

                   offlineJet_pt = arrays[i_offlineJetColl+'_pt'] [index][offlineJet_match]
                   offlineJet_eta = arrays[i_offlineJetColl+'_eta'][index][offlineJet_match]
                   offlineJet_phi = arrays[i_offlineJetColl+'_phi'][index][offlineJet_match]

                   onlineOffline_dEta = onlineJet_eta - offlineJet_eta
                   onlineOffline_dPhi = delta_phi(onlineJet_phi, offlineJet_phi)
                   onlineOffline_dRmatch = math.sqrt(onlineOffline_dEta*onlineOffline_dEta + onlineOffline_dPhi*onlineOffline_dPhi)

                   values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt'] += [onlineJet_pt]
                   values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_eta'] += [onlineJet_eta]
                   values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_phi'] += [onlineJet_phi]
                   values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_mass'] += [onlineJet_mass]
                   values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_dRmatch'] += [onlineOffline_dRmatch]

                   if offlineJet_pt != 0:

                      values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_overOffline'] += [onlineJet_pt / offlineJet_pt]
                      values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_minusOffline'] += [onlineJet_pt - offlineJet_pt]

                      values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt:'+i_offlineJetColl+'_EtaIncl_pt'] += [(onlineJet_pt, offlineJet_pt)]
                      values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_eta:'+i_offlineJetColl+'_EtaIncl_eta'] += [(onlineJet_eta, offlineJet_eta)]

                      values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_overOffline:'+i_offlineJetColl+'_EtaIncl_pt'] += [(onlineJet_pt / offlineJet_pt, offlineJet_pt)]
                      values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_overOffline:'+i_offlineJetColl+'_EtaIncl_eta'] += [(onlineJet_pt / offlineJet_pt, offlineJet_eta)]

                      values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_minusOffline:'+i_offlineJetColl+'_EtaIncl_pt'] += [(onlineJet_pt - offlineJet_pt, offlineJet_pt)]
                      values[i_onlineJetColl+i_onlineJetReg+'_MatchedToOffline_pt_minusOffline:'+i_offlineJetColl+'_EtaIncl_eta'] += [(onlineJet_pt - offlineJet_pt, offlineJet_eta)]

        njets_tags = ['_EtaIncl_MatchedToOffline', '_HB_MatchedToOffline', '_HE_MatchedToOffline', '_HF_MatchedToOffline']

        for i_jettag in njets_tags:
            values[i_onlineJetColl+i_jettag+'_njets'] = len(values[i_onlineJetColl+i_jettag+'_pt']) if (i_onlineJetColl+i_jettag+'_pt' in values) else 0

            if len(values[i_onlineJetColl+i_jettag+'_pt']) > 0:
               values[i_onlineJetColl+i_jettag+'_pt0'] = max(values[i_onlineJetColl+i_jettag+'_pt'])

            if (i_onlineJetColl+i_jettag+'_pt:'+i_offlineJetColl+'_EtaIncl_pt' in values) and (len(values[i_onlineJetColl+i_jettag+'_pt:'+i_offlineJetColl+'_EtaIncl_pt']) > 0):
               values[i_onlineJetColl+i_jettag+'_pt0:'+i_offlineJetColl+'_EtaIncl_pt'] = sorted(values[i_onlineJetColl+i_jettag+'_pt:'+i_offlineJetColl+'_EtaIncl_pt'], key=lambda x : x[0], reverse=True)[0]

    ## MET
    for i_met in METCollections:
        for i_var in ['pt', 'phi', 'sumEt']:
            values[i_met+'_'+i_var] = arrays[i_met+'_'+i_var][index][0]

    genMETTrue_vec2d = ROOT.TVector2()
    genMETTrue_vec2d.SetMagPhi(values['genMETTrue_pt'], values['genMETTrue_phi'])

    for i_met in METCollections:

        if i_met == 'genMETTrue': continue

        values[i_met+'_pt'], values[i_met+'_phi']

        iMET_vec2d = ROOT.TVector2()
        iMET_vec2d.SetMagPhi(values[i_met+'_pt'], values[i_met+'_phi'])

        values[i_met+'_pt_paraToGEN'] = iMET_vec2d.Mod() * math.cos(iMET_vec2d.DeltaPhi(genMETTrue_vec2d))
        values[i_met+'_pt_perpToGEN'] = iMET_vec2d.Mod() * math.sin(iMET_vec2d.DeltaPhi(genMETTrue_vec2d))

        values[i_met+'_pt_paraToGENMinusGEN'] = values[i_met+'_pt_paraToGEN'] - values['genMETTrue_pt']

        for i_var in ['pt', 'phi', 'sumEt']:

            values[i_met+'_'+i_var+'_minusGEN'] = values[i_met+'_'+i_var] - values['genMETTrue_'+i_var]
            if i_var == 'phi':
               values[i_met+'_'+i_var+'_minusGEN'] = abs(values[i_met+'_'+i_var+'_minusGEN'])
               if values[i_met+'_'+i_var+'_minusGEN'] > math.pi:
                  values[i_met+'_'+i_var+'_minusGEN'] = 2*math.pi - values[i_met+'_'+i_var+'_minusGEN']

            if values['genMETTrue_'+i_var] != 0:
               values[i_met+'_'+i_var+'_overGEN'] = values[i_met+'_'+i_var] / values['genMETTrue_'+i_var]

    for [i_met_onl, i_met_off] in METOnlineOfflinePairs:

        iMETonl_vec2d = ROOT.TVector2()
        iMETonl_vec2d.SetMagPhi(values[i_met_onl+'_pt'], values[i_met_onl+'_phi'])

        iMEToff_vec2d = ROOT.TVector2()
        iMEToff_vec2d.SetMagPhi(values[i_met_off+'_pt'], values[i_met_off+'_phi'])

        values[i_met_onl+'_pt_paraToOffline'] = iMETonl_vec2d.Mod() * math.cos(iMETonl_vec2d.DeltaPhi(iMEToff_vec2d))
        values[i_met_onl+'_pt_perpToOffline'] = iMETonl_vec2d.Mod() * math.sin(iMETonl_vec2d.DeltaPhi(iMEToff_vec2d))

        values[i_met_onl+'_pt_paraToOfflineMinusOffline'] = values[i_met_onl+'_pt_paraToOffline'] - values[i_met_off+'_pt']

        for i_var in ['pt', 'phi', 'sumEt']:

            values[i_met_onl+'_'+i_var+'_minusOffline'] = values[i_met_onl+'_'+i_var] - values[i_met_off+'_'+i_var]
            if i_var == 'phi':
               values[i_met_onl+'_'+i_var+'_minusOffline'] = abs(values[i_met_onl+'_'+i_var+'_minusOffline'])
               if values[i_met_onl+'_'+i_var+'_minusOffline'] > math.pi:
                  values[i_met_onl+'_'+i_var+'_minusOffline'] = 2*math.pi - values[i_met_onl+'_'+i_var+'_minusOffline']

            if values[i_met_off+'_'+i_var] != 0:
               values[i_met_onl+'_'+i_var+'_overOffline'] = values[i_met_onl+'_'+i_var] / values[i_met_off+'_'+i_var]

    ## copies of event values under different categories/selections
    value_keys = values.keys()

    for i_sel in EvtSelections:

        # selections
        if i_sel == 'NoSelection/': pass

        elif i_sel == 'hltAK4PFCHS100_EtaIncl/':
           if not (max([0] + values['hltAK4PFCHSJetsCorrected_EtaIncl_pt']) > 100.): continue

        elif i_sel == 'hltAK4PFCHS100_HB/':
           if not (max([0] + values['hltAK4PFCHSJetsCorrected_HB_pt']) > 100.): continue

        elif i_sel == 'hltAK4PFCHS100_HE/':
           if not (max([0] + values['hltAK4PFCHSJetsCorrected_HE_pt']) > 100.): continue

        elif i_sel == 'hltAK4PFCHS100_HF/':
           if not (max([0] + values['hltAK4PFCHSJetsCorrected_HF_pt']) > 100.): continue

        elif i_sel == 'hltAK4Puppi100_EtaIncl/':
           if not (max([0] + values['hltAK4PuppiJetsCorrected_EtaIncl_pt']) > 100.): continue

        elif i_sel == 'hltAK4Puppi100_HB/':
           if not (max([0] + values['hltAK4PuppiJetsCorrected_HB_pt']) > 100.): continue

        elif i_sel == 'hltAK4Puppi100_HE/':
           if not (max([0] + values['hltAK4PuppiJetsCorrected_HE_pt']) > 100.): continue

        elif i_sel == 'hltAK4Puppi100_HF/':
           if not (max([0] + values['hltAK4PuppiJetsCorrected_HF_pt']) > 100.): continue

        elif i_sel == 'hltPFMET200/':
           if not (values['hltPFMET_pt'] > 200.): continue

        elif i_sel == 'hltPuppiMET200/':
           if not (values['hltPuppiMET_pt'] > 200.): continue

        elif i_sel == 'hltPFMETTypeOne200/':
           if not (values['hltPFMETTypeOne_pt'] > 200.): continue

        elif i_sel == 'hltPuppiMETTypeOne200/':
           if not (values['hltPuppiMETTypeOne_pt'] > 200.): continue

        else:
           KILL('analyze_event -- invalid key for event selection: '+i_sel)

        # copies
        for _tmp in value_keys:
            if '/' in _tmp: continue

            if i_sel+_tmp in values:
               KILL(log_prx+'logic error: attempting to overwrite event value under key "'+i_sel+_tmp+'"')

            values[i_sel+_tmp] = copy.deepcopy(values[_tmp])

    ## histogram filling
    for i_hist_key in sorted(list(set(th1s.keys() + th2s.keys()))):

        if i_hist_key in th1s:

           if i_hist_key in values:

              if isinstance(values[i_hist_key], list):
                 for _tmp in values[i_hist_key]:
                     th1s[i_hist_key].Fill(_tmp)
              else:
                 th1s[i_hist_key].Fill(values[i_hist_key])

        elif i_hist_key in th2s:

           if i_hist_key in values:

              if isinstance(values[i_hist_key], list):
                 for _tmp in values[i_hist_key]:
                     if len(_tmp) != 2: KILL('xxx1 '+i_hist_key)
                     th2s[i_hist_key].Fill(_tmp[0], _tmp[1])
              else:
                 if len(values[i_hist_key]) != 2: KILL('xxx2 '+i_hist_key)
                 th2s[i_hist_key].Fill(values[i_hist_key][0], values[i_hist_key][1])

           else:
              i_hist_key_basename = os.path.basename(i_hist_key)

              i_hist_key_basename_split = i_hist_key_basename.split(':')

              if len(i_hist_key_basename_split) != 2:
                 KILL('AAA '+i_hist_key)

              i_hist_key_dirname = os.path.dirname(i_hist_key)
              if i_hist_key_dirname: i_hist_key_dirname += '/'

              i_hist_key_varX = i_hist_key_dirname+i_hist_key_basename_split[0]
              i_hist_key_varY = i_hist_key_dirname+i_hist_key_basename_split[1]

              if i_hist_key_varX not in values: continue
              if i_hist_key_varY not in values: continue

              if isinstance(values[i_hist_key_varX], list):

                 if not isinstance(values[i_hist_key_varY], list):
                    KILL('analyze_event -- 2D histograms cannot be filled from 1D values (second collection is not a list): '+i_hist_key_varX+' '+i_hist_key_varY)

                 if len(values[i_hist_key_varX]) != len(values[i_hist_key_varY]):
                    KILL('analyze_event -- 2D histograms cannot be filled from 1D values (collections of different sizes): '+i_hist_key_varX+' '+i_hist_key_varY)

                 for _tmp in range(len(values[i_hist_key_varX])):
                     th2s[i_hist_key].Fill(values[i_hist_key_varX][_tmp], values[i_hist_key_varY][_tmp])
              else:
                 th2s[i_hist_key].Fill(values[i_hist_key_varX], values[i_hist_key_varY])

    if verbose:
       for _tmp in sorted(values.keys()):
           if 'met' in _tmp.lower(): continue
           if 'jets' not in _tmp.lower(): continue
           print colored_text(_tmp, ['1','95']), values[_tmp]

#### main --------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
   ### args --------------
   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--inputs', dest='inputs', required=True, nargs='+', default=None,
                       help='path to input .root file(s)')

   parser.add_argument('-o', '--output', dest='output', required=True, action='store', default=None,
                       help='path to output .root file')

   parser.add_argument('-t', '--tree', dest='tree', action='store', default='JMETriggerNTuple/Events',
                       help='key of TTree in input file(s)')

   parser.add_argument('-e', '--every', dest='every', action='store', type=int, default=1e2,
                       help='show progress of processing every N events')

   parser.add_argument('-f', '--firstEvent', dest='firstEvent', action='store', type=int, default=0,
                       help='index of first event to be processed (inclusive)')

   parser.add_argument('-l', '--lastEvent', dest='lastEvent', action='store', type=int, default=-1,
                       help='index of last event to be processed (inclusive)')

   parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                       help='enable verbose mode')

   opts, opts_unknown = parser.parse_known_args()
   ### -------------------

   ROOT.gROOT.SetBatch()
   ROOT.gErrorIgnoreLevel = ROOT.kError #kWarning

   log_prx = os.path.basename(__file__)+' -- '

   ### args validation ---
   INPUT_FILES = []

   for i_inpf in opts.inputs:

       i_inpf_ls = glob.glob(i_inpf)

       for i_inpf_2 in i_inpf_ls:

           if os.path.isfile(i_inpf_2):
              INPUT_FILES += [os.path.abspath(os.path.realpath(i_inpf_2))]

   INPUT_FILES = sorted(list(set(INPUT_FILES)))

   if len(INPUT_FILES) == 0:
      KILL(log_prx+'empty list of input files [-i]')

   if os.path.exists(opts.output):
      KILL(log_prx+'target path to output .root file already exists [-o]: '+opts.output)

   SHOW_EVERY = opts.every
   if SHOW_EVERY <= 0:
      WARNING(log_prx+'invalid (non-positive) value for option "-e/--every" ('+str(SHOW_EVERY)+'), value will be changed to 100')
      SHOW_EVERY = 1e2

   if len(opts_unknown) > 0:
      KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))
   ### -------------------

   # convert bin-edges to TH1D
   th1s, th2s = create_histograms()

   nEvtProcessed = 0

   for i_inpf in INPUT_FILES:

       if opts.verbose: print colored_text('[input]', ['1','92']), os.path.relpath(i_inpf)

       try:
          i_ttree = uproot.open(i_inpf)[opts.tree]
       except:
          WARNING(log_prx+'target TFile does not contain a TTree named "'+opts.tree+'" (file will be ignored) [-t]: '+i_inpf)
          continue

       print 'loading content of TBranches into arrays..'
       arr_entrystart = 0 if opts.firstEvent < 0 else opts.firstEvent
       arr_entrystop = i_ttree.numentries if opts.lastEvent < 0 else min(i_ttree.numentries, opts.lastEvent + 1)

       if arr_entrystart > arr_entrystop:
          KILL(log_prx+'logic error: entry-start ('+str(arr_entrystart)+') is higher than entry-stop ('+str(arr_entrystop)+')')

       arr = i_ttree.arrays('*', entrystart=arr_entrystart, entrystop=arr_entrystop)
       print 'done'

       for evt_idx in range(arr_entrystop - arr_entrystart):

           analyze_event(arrays=arr, index=evt_idx, th1s=th1s, th2s=th2s, verbose=opts.verbose)

           nEvtProcessed += 1

           if not (evt_idx % SHOW_EVERY) and (evt_idx > 0):
              print colored_text('['+str(os.path.relpath(opts.output))+']', ['1','93']), 'events processed:', evt_idx

       print 'events processed:', (arr_entrystop - arr_entrystart)

   ### output file -------
   output_dirname = os.path.dirname(os.path.abspath(opts.output))
   if not os.path.isdir(output_dirname): EXE('mkdir -p '+output_dirname)
   del output_dirname

   output_tfile = ROOT.TFile(opts.output, 'recreate')
   if (not output_tfile) or output_tfile.IsZombie() or output_tfile.TestBit(ROOT.TFile.kRecovered):
      raise SystemExit(1)

   output_tfile.cd()

   hEvtProcessed = create_TH1D('eventsProcessed', [0,1])
   hEvtProcessed.SetBinContent(1, nEvtProcessed)
   hEvtProcessed.SetBinError(1, math.sqrt(nEvtProcessed))
   hEvtProcessed.Write()

   for i_idx in sorted(th1s.keys() + th2s.keys()):

       output_tfile.cd()

       out_key = i_idx

       while '/' in out_key:
          slash_index = out_key.find('/')
          out_dir = out_key[:slash_index]
          out_key = out_key[slash_index+1:]
          out_dir = getattr(output_tfile, 'Get' if output_tfile.Get(out_dir) else 'mkdir')(out_dir)
          out_dir.cd()

       the_dict = th1s if i_idx in th1s else th2s

       the_dict[i_idx].SetName(out_key)
       the_dict[i_idx].SetTitle(out_key)
       the_dict[i_idx].Write()

#   ROOT.gROOT.GetListOfFiles().Remove(output_tfile)
   output_tfile.Close()

   print colored_text('[output]', ['1','92']), os.path.relpath(opts.output)
   ### -------------------
