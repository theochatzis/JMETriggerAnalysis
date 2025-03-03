#!/usr/bin/env python
import argparse
import os
import json
import ROOT

from common.utils import *

from common.plot_style import apply_style as load_plot_style

def TH1_keys(tdirectory, prefix='', contains_all=[], contains_one=[]):

    th1_keys = []

    for k_key in tdirectory.GetListOfKeys():
        k_key_name = k_key.GetName()

        k_obj = tdirectory.Get(k_key_name)
        if not k_obj: continue

        if k_obj.InheritsFrom('TDirectory'):

           th1_keys += TH1_keys(k_obj, prefix=prefix+k_obj.GetName()+'/', contains_all=contains_all, contains_one=contains_one)

        elif k_obj.InheritsFrom('TH1'):

           h_name = prefix+k_obj.GetName()

           if len(contains_all) > 0:
              skip = False
              for _tmp in contains_all:
                  if _tmp not in h_name: skip = True; break;
              if skip: continue

           if len(contains_one) > 0:
              skip = True
              for _tmp in contains_one:
                  if _tmp in h_name: skip = False; break;
              if skip: continue

           th1_keys += [prefix+k_obj.GetName()]

    return th1_keys

def add_TH1_objects(filelist, contains_all):

    th1_dict = {}

    for i_inputf_path in filelist:

        i_inptfile = ROOT.TFile.Open(i_inputf_path)
        if (not i_inptfile) or i_inptfile.IsZombie() or i_inptfile.TestBit(ROOT.TFile.kRecovered): raise SystemExit(1)

        for h_key in TH1_keys(i_inptfile, contains_all=contains_all):

            if h_key in th1_dict:
               KILL(log_prx+'input error -> key "'+h_key+'" already exists in histogram-dictionary')

            h0 = i_inptfile.Get(h_key)
            if not (h0 and h0.InheritsFrom('TH1')):
               KILL(log_prc+'input error -- key "'+h_key+'" not associated to a TH1 object: '+opts.input)

            h_key_dict = h_key
#            h_key_dict = '/'.join(h_key.split('/')[2:])

            if h_key_dict in th1_dict: th1_dict[h_key_dict].Add(h0)
            else                     : th1_dict[h_key_dict] =   h0.Clone(); th1_dict[h_key_dict].SetDirectory(0);

            if opts.verbose: print '\033[1m'+'\033[92m'+'[input]'+'\033[0m', h_key

        ROOT.gROOT.GetListOfFiles().Remove(i_inptfile)
        i_inptfile.Close()

    return th1_dict

def get_text(x1ndc_, y1ndc_, talign_, tsize_, text_):
    txt = ROOT.TLatex(x1ndc_, y1ndc_, text_)
    txt.SetTextAlign(talign_)
    txt.SetTextSize(tsize_)
    txt.SetTextFont(42)
    txt.SetNDC()

    return txt

def plot_canvas(key, target, reference, target_legend, reference_legend, output, output_extensions, config):

#    if 'met' not in key.lower(): return

    plot_conf = {}
    key0 = key
    while key0 not in plot_conf:
       if '/' in key0:
          key0 = key0[key0.find('/')+1:]
       else:
          break

    if key0 in config:
       plot_conf = config[key0]
    else:
       plot_conf = {
         'titleX': '',
         'titleY': '',
         'Label': key0,
         'MarkerSize': 0.,
         'PlotRatio': 1,
         'Draw': 'hist,e0',
         'DrawLegend': 'l',
       }

    if (target != None) and (reference != None):
       if target.ClassName() != reference.ClassName():
          WARNING(output)
          return 1

    if   (target is not None) and (reference is not None): h_refe = reference.Clone(); h_targ = target   .Clone();
    elif (target is     None) and (reference is not None): h_refe = reference.Clone(); h_targ = reference.Clone(); h_targ.Reset();
    elif (target is not None) and (reference is     None): h_targ = target   .Clone(); h_refe = target   .Clone(); h_refe.Reset();
    elif (target is     None) and (reference is     None):
       return 1

    if not (h_targ.InheritsFrom('TH1F') or h_targ.InheritsFrom('TH1D')):
       return 1

#    if (h_targ.GetNbinsX() == h_refe.GetNbinsX()) and (h_targ.GetNbinsY() == h_refe.GetNbinsY()):
#       for i_bin in range(0, 2+(h_targ.GetNbinsX() * h_targ.GetNbinsY())):
#           i_bin_targ = h_targ.GetBinContent(i_bin)
#           i_bin_refe = h_refe.GetBinContent(i_bin)
#           if abs(i_bin_targ - i_bin_refe) > 1e-8:
#              print 'differs', output
#              break
#    else:
#       print 'differs', output

#    binwidth_nonconst, binw = False, None
#    for i_bin in range(1, 1+(h_targ.GetNbinsX() * h_targ.GetNbinsY())):
#        if binw is None:
#           binw = h_targ.GetBinWidth(i_bin)
#        elif binw != h_targ.GetBinWidth(i_bin):
#           binwidth_nonconst = True
#           break

##!!!!!!!
#    output_basename_woExt = str(output)
#    output_dirname = os.path.dirname(output_basename_woExt)
#    if not os.path.isdir(output_dirname): EXE('mkdir -p '+output_dirname)
#    print os.path.relpath(output_basename_woExt)
#    return
##!!!!!!!

    titleX = str(plot_conf['titleX'])
    titleY = str(plot_conf['titleY'])
    markerColor = [1, 2]
    markerSize = [plot_conf['MarkerSize'], plot_conf['MarkerSize']]
    markerStyle = [20, 24]
    lineColor = [1, 2]
    lineWidth = [2, 2]
    draw_opt = str(plot_conf['Draw'])
    legendDraw_opt = str(plot_conf['DrawLegend'])

    if plot_conf['DivideByBinWidth']:
       titleY += ' / Bin width'
       h_targ.Scale(1, 'width')
       h_refe.Scale(1, 'width')

    h_refe.SetBit(ROOT.TH1.kNoTitle)
    h_targ.SetBit(ROOT.TH1.kNoTitle)

    h_refe.UseCurrentStyle()
    h_targ.UseCurrentStyle()

    h_refe.SetMarkerColor(markerColor[0])
    h_refe.SetMarkerSize(markerSize[0])
    h_refe.SetMarkerStyle(markerStyle[0])
    h_refe.SetLineColor(lineColor[0])
    h_refe.SetLineWidth(lineWidth[0])

    h_targ.SetMarkerColor(markerColor[1])
    h_targ.SetMarkerSize(markerSize[1])
    h_targ.SetMarkerStyle(markerStyle[1])
    h_targ.SetLineColor(lineColor[1])
    h_targ.SetLineWidth(lineWidth[1])

#    opt_draw, opt_legd = 'hist,e', 'lep'
#    if h_refe.GetName().startswith('effic_'): opt_draw, opt_legd = 'pex0', 'pex0'

    ratio = plot_conf['PlotRatio']

    logY = False

#    histo_type = None
#    if   'numerator'   in h_refe.GetTitle(): histo_type = 'NUM'
#    elif 'denominator' in h_refe.GetTitle(): histo_type = 'DEN'
#
#    # normalize (numerator, denominator) histograms to unity
#    if histo_type in ['NUM', 'DEN']:
#       if h_refe.Integral() != 0.: h_refe.Scale(1. / h_refe.Integral())
#       if h_targ.Integral() != 0.: h_targ.Scale(1. / h_targ.Integral())

    canvas = ROOT.TCanvas(key, key)
    canvas.SetGrid(1,1)
    canvas.SetTickx()
    canvas.SetTicky()

    T = canvas.GetTopMargin()
    R = canvas.GetRightMargin()
    B = canvas.GetBottomMargin()
    L = canvas.GetLeftMargin()

    ROOT.TGaxis.SetExponentOffset(0.65*L, 0.03, 'y')

    leg = ROOT.TLegend(L+(1-R-L)*0.00, (1-T)+T*0.05, L+(1-R-L)*1.00, (1-T)+T*0.95)
    leg.SetBorderSize(2)
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.AddEntry(h_targ, '#bf{Target}: '   +target_legend   , legendDraw_opt)
    leg.AddEntry(h_refe, '#bf{Reference}: '+reference_legend, legendDraw_opt)

    txt1 = get_text(L+(1-R-L)*0.95, B+(1-T-B)*0.925, 31, .035, str(plot_conf['Label']))
#    if   histo_type == 'NUM': txt1 = get_text((1-R)+R*0.25, (1-T), 11, .025, '[Numerator]');   txt1.SetTextAngle(-90);
#    elif histo_type == 'DEN': txt1 = get_text((1-R)+R*0.25, (1-T), 11, .025, '[Denominator]'); txt1.SetTextAngle(-90);

    txt2 = None # get_text(L+(1-R-L)*0.05, B+(1-B-T)*.77, 13, .040, '')

    canvas.cd()

    hmax, hmin = 0.0, 0.0
    for _tmp in [h_targ, h_refe]:
        for i_bin in range(1, _tmp.GetNbinsX()+1):
            hmax = max(hmax, (_tmp.GetBinContent(i_bin) + _tmp.GetBinError(i_bin)))
            hmin = min(hmin, (_tmp.GetBinContent(i_bin) - _tmp.GetBinError(i_bin)))

    if not ratio:

       canvas.SetTickx()
       canvas.SetTicky()

       canvas.SetLogy(logY)

       h_refe.SetStats(0)

       h_refe.SetYTitle(titleX)
       h_refe.SetYTitle(titleY)

       h_refe.Draw(draw_opt)
       h_targ.Draw(draw_opt+',same')
       h_refe.Draw('axis,same')
       if leg: leg.Draw('same')

       if txt1: txt1.Draw('same')
       if txt2: txt2.Draw('same')

#       h_refe.GetXaxis().SetRangeUser(xmin_, xmax_)

#       if histo_type in ['NUM', 'DEN']:
#          h_refe.GetYaxis().SetTitle('a.u.')

       if hmin > 0:
          if logY: h_refe.GetYaxis().SetRangeUser(.0003, .0003*((hmax/.0003)**(1./.85)))
          else   : h_refe.GetYaxis().SetRangeUser(.0001, .0001+((hmax-.0001) *(1./.85)))
       else:
          h_refe.GetYaxis().SetRangeUser(1.05*hmin, .0001+((hmax-.0001) *(1./.85)))

    else:

        canvas.cd()

        pad1H = 0.7

        pad1 = ROOT.TPad('pad1', 'pad1', 0, 1-pad1H, 1, 1)

        pad1.SetTopMargin(pad1.GetTopMargin()/pad1H)
        pad1.SetBottomMargin(0.02)
        pad1.SetGrid(1,1)
        pad1.SetTickx()
        pad1.SetTicky()
        pad1.Draw()

        ROOT.SetOwnership(pad1, False)

        pad1.cd()
        h11 = h_refe.DrawCopy(draw_opt)
        h11.SetBit(ROOT.TH1.kNoTitle)
        h11.SetStats(0)
        h11.SetXTitle('')
        h11.SetYTitle(titleY)

#        if histo_type in ['NUM', 'DEN']:
#           h11.GetYaxis().SetTitle('a.u.')

        h11.GetYaxis().SetTitleSize(h11.GetYaxis().GetTitleSize()/pad1H)
        h11.GetYaxis().SetTitleOffset(h11.GetYaxis().GetTitleOffset()*pad1H)
        h11.GetXaxis().SetLabelSize(0)
        h11.GetYaxis().SetLabelSize (h11.GetYaxis().GetLabelSize() /pad1H)
        h11.GetXaxis().SetTickLength(h11.GetXaxis().GetTickLength()/pad1H)

        h_targ.Draw(draw_opt+',same')
        h11.Draw('axis,same')
        if leg: leg.Draw('same')

#        h11.GetXaxis().SetRangeUser(xmin_, xmax_)

        pad1.SetLogy(logY)

        if hmin > 0:
           if logY: h11.GetYaxis().SetRangeUser(.0003, .0003*((hmax/.0003)**(1./.85)))
           else   : h11.GetYaxis().SetRangeUser(.0001, .0001+((hmax-.0001) *(1./.85)))
        else:
           h11.GetYaxis().SetRangeUser(1.05*hmin, .0001+((hmax-.0001) *(1./.85)))

        if txt1: txt1.SetTextSize(txt1.GetTextSize()/pad1H); txt1.Draw('same');
        if txt2: txt2.SetTextSize(txt2.GetTextSize()/pad1H); txt2.Draw('same');

        pad1.Update()

        if txt1: txt1.SetY(1.-(1.-txt1.GetY())/pad1H)
        if txt2: txt2.SetY(1.-(1.-txt2.GetY())/pad1H)

        if leg:
           leg.SetY1NDC(1.-(1.-leg.GetY1NDC())/pad1H)
           leg.SetY2NDC(1.-(1.-leg.GetY2NDC())/pad1H)
#           leg.SetY1NDC((leg.GetY1NDC()-canvas.GetBottomMargin()+pad1.GetBottomMargin())/pad1H)
#           leg.SetY2NDC((leg.GetY2NDC()-canvas.GetBottomMargin()+pad1.GetBottomMargin())/pad1H)

        canvas.cd()

        pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, 1-pad1H)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(pad2.GetBottomMargin()/(1-pad1H))
        pad2.SetGrid(1,1)
        pad2.SetTickx()
        pad2.SetTicky()
        pad2.Draw()

        denom = h_refe.Clone()
        for _tmp in range(0, denom.GetNbinsX()+2): denom.SetBinError(_tmp, 0.)

        h21 = h_refe.Clone()
        h22 = h_targ.Clone()

        h21.Divide(denom)
        h22.Divide(denom)

#        for h0 in [h21, h22]:
#            for _tmp in range(0, h0.GetNbinsX()+2):
#                h0.SetBinContent(_tmp, h0.GetBinContent(b)-1.)

        ROOT.SetOwnership(pad2, False)

        pad2.cd()
        h21.SetStats(0)
#        h21.SetTitle(title_)
        h21.SetMarkerSize(0)

        h21.SetFillStyle(3017)
        h21.SetFillColor(16)

        h21.GetYaxis().SetTitle('Tar/Ref')
        h21.GetXaxis().SetTitle(titleX)
        h21.GetYaxis().CenterTitle()
        h21.GetXaxis().SetTitleSize  (h21.GetXaxis().GetTitleSize()   /(1-pad1H))
        h21.GetYaxis().SetTitleSize  (h21.GetYaxis().GetTitleSize()   /(1-pad1H))
        h21.GetXaxis().SetTitleOffset(h21.GetXaxis().GetTitleOffset()           )
        h21.GetYaxis().SetTitleOffset(h21.GetYaxis().GetTitleOffset() *(1-pad1H))
        h21.GetXaxis().SetLabelSize  (h21.GetXaxis().GetLabelSize()   /(1-pad1H))
        h21.GetYaxis().SetLabelSize  (h21.GetYaxis().GetLabelSize()   /(1-pad1H))
        h21.GetXaxis().SetLabelOffset(h21.GetXaxis().GetLabelOffset() /(1-pad1H))
        h21.GetYaxis().SetLabelOffset(h21.GetYaxis().GetLabelOffset()           )
        h21.GetXaxis().SetTickLength (h21.GetXaxis().GetTickLength()  /(1-pad1H))
        h21.GetYaxis().SetNdivisions(304)

#        h21.GetXaxis().SetRangeUser(xmin_, xmax_)

        h2max, h2min = None, None
        for h_tmp in [h21, h22]:
            for _tmp in range(1, h_tmp.GetNbinsX()+1):

                if (h21.GetBinContent(_tmp) == 0.) and (h21.GetBinLowEdge(_tmp) == h22.GetBinLowEdge(_tmp)) and (h22.GetBinContent(_tmp) == 0.): continue

                h2max = max(h2max, h_tmp.GetBinContent(_tmp)+h_tmp.GetBinError(_tmp)) if h2max is not None else h_tmp.GetBinContent(_tmp)+h_tmp.GetBinError(_tmp)
                h2min = min(h2min, h_tmp.GetBinContent(_tmp)-h_tmp.GetBinError(_tmp)) if h2min is not None else h_tmp.GetBinContent(_tmp)-h_tmp.GetBinError(_tmp)

        if (h2max is not None) and (h2min is not None):

#           h2min = min(int(h2min*101.)/100., int(h2min*99.)/100.)
#           h2max = max(int(h2max*101.)/100., int(h2max*99.)/100.)

           h21.GetYaxis().SetRangeUser(h2min, h2max)

        h21.GetYaxis().SetNdivisions(404)

        h21.Draw('e2')
        h22.Draw(draw_opt+',same')
        h21.Draw('axis,same')

    canvas.cd()
    canvas.Update()

    output_basename_woExt = str(output)

    output_dirname = os.path.dirname(output_basename_woExt)
    if not os.path.isdir(output_dirname): EXE('mkdir -p '+output_dirname)

    for i_ext in output_extensions:

        out_file = output_basename_woExt+'.'+i_ext

        canvas.SaveAs(out_file)

        print '\033[1m'+'\033[92m'+'[output]'+'\033[0m', os.path.relpath(out_file)

    canvas.Close()

    return 0
#### ----

#### main
if __name__ == '__main__':
    ### args --------------
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--target', dest='target', required=True, nargs='+', default=[],
                        help='path to input DQM .root file')

    parser.add_argument('-r', '--reference', dest='reference', required=True, nargs='+', default=[],
                        help='path to input DQM .root file')

    parser.add_argument('--t-leg', dest='target_legend', action='store', default='Target',
                        help='text describing target file (text in legend entry)')

    parser.add_argument('--r-leg', dest='reference_legend', action='store', default='Reference',
                        help='text describing reference file (text in legend entry)')

    parser.add_argument('-o', '--output', dest='output', required=True, action='store', default=None,
                        help='path to output directory')

    parser.add_argument('--only-keys', dest='only_keys', nargs='+', default=[], #!!['NoSelection/'],
                        help='list of strings required to be in histogram key')

    parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['png'],
                        help='list of extension(s) for output file(s)')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                        help='enable verbose mode')

    opts, opts_unknown = parser.parse_known_args()
    ### -------------------

    ROOT.gROOT.SetBatch()
    ROOT.gErrorIgnoreLevel = ROOT.kWarning

    log_prx = os.path.basename(__file__)+' -- '

    ### args validation ---
#    if not os.path.isfile(opts.target):
#       KILL(log_prx+'invalid path to input .root file for "target" [-t]: '+opts.target)
#
#    if not os.path.isfile(opts.reference):
#       KILL(log_prx+'invalid path to input .root file for "reference" [-r]: '+opts.reference)

    if os.path.exists(opts.output):
       KILL(log_prx+'target path to output directory already exists [-o]: '+opts.output)

    EXTS = list(set(opts.exts))

    ONLY_KEYS = list(set(opts.only_keys))

    if len(ONLY_KEYS):
       print '\n >>> will plot only TH1 objects containing all of the following strings in their internal path:', ONLY_KEYS, '\n'

    if len(opts_unknown) > 0:
       KILL(log_prx+'unrecognized command-line arguments: '+str(opts_unknown))
    ### -------------------

    ### input histograms --
    histo_dict_target = add_TH1_objects(filelist=opts.target   , contains_all=ONLY_KEYS)
    histo_dict_refern = add_TH1_objects(filelist=opts.reference, contains_all=ONLY_KEYS)

    # normalize each input to number of processed events
    for _tmp_dict in [histo_dict_target, histo_dict_refern]:
        if 'eventsProcessed' in _tmp_dict:
           _tmp_norm = _tmp_dict['eventsProcessed'].GetBinContent(1)
           for _tmp_h in _tmp_dict:
               if '_wrt_' not in _tmp_h:
                  _tmp_dict[_tmp_h].Scale(1. / _tmp_norm)
        else:
           raise RuntimeError('AAA')

    tags = {
      'hltAK4PFJetsUncorrected_EtaIncl_MatchedToGEN': 'HLT AK4-PF(NoJECs) matched-to-GEN',
      'hltAK4PFJetsUncorrected_HB_MatchedToGEN': 'HLT AK4-PF(NoJECs), |#eta|<1.5, matched-to-GEN',
      'hltAK4PFJetsUncorrected_HGCal_MatchedToGEN': 'HLT AK4-PF(NoJECs), 1.5<|#eta|<3.0, matched-to-GEN',
      'hltAK4PFJetsUncorrected_HF1_MatchedToGEN': 'HLT AK4-PF(NoJECs), 3.0<|#eta|<4.0, matched-to-GEN',
      'hltAK4PFJetsUncorrected_HF2_MatchedToGEN': 'HLT AK4-PF(NoJECs), 4.0<|#eta|<5.0, matched-to-GEN',

      'hltAK4PFJetsUncorrected_EtaIncl_MatchedToOffline': 'HLT AK4-PF(NoJECs) matched-to-Offline',
      'hltAK4PFJetsUncorrected_HB_MatchedToOffline': 'HLT AK4-PF(NoJECs), |#eta|<1.5, matched-to-Offline',
      'hltAK4PFJetsUncorrected_HGCal_MatchedToOffline': 'HLT AK4-PF(NoJECs), 1.5<|#eta|<3.0, matched-to-Offline',
      'hltAK4PFJetsUncorrected_HF1_MatchedToOffline': 'HLT AK4-PF(NoJECs), 3.0<|#eta|<4.0, matched-to-Offline',
      'hltAK4PFJetsUncorrected_HF2_MatchedToOffline': 'HLT AK4-PF(NoJECs), 4.0<|#eta|<5.0, matched-to-Offline',

      'hltAK4PFJetsCorrected_EtaIncl_MatchedToGEN': 'HLT AK4-PF matched-to-GEN',
      'hltAK4PFJetsCorrected_HB_MatchedToGEN': 'HLT AK4-PF, |#eta|<1.5, matched-to-GEN',
      'hltAK4PFJetsCorrected_HGCal_MatchedToGEN': 'HLT AK4-PF, 1.5<|#eta|<3.0, matched-to-GEN',
      'hltAK4PFJetsCorrected_HF1_MatchedToGEN': 'HLT AK4-PF, 3.0<|#eta|<4.0, matched-to-GEN',
      'hltAK4PFJetsCorrected_HF2_MatchedToGEN': 'HLT AK4-PF, 4.0<|#eta|<5.0, matched-to-GEN',

      'hltAK4PFJetsCorrected_EtaIncl_MatchedToOffline': 'HLT AK4-PF matched-to-Offline',
      'hltAK4PFJetsCorrected_HB_MatchedToOffline': 'HLT AK4-PF, |#eta|<1.5, matched-to-Offline',
      'hltAK4PFJetsCorrected_HGCal_MatchedToOffline': 'HLT AK4-PF, 1.5<|#eta|<3.0, matched-to-Offline',
      'hltAK4PFJetsCorrected_HF1_MatchedToOffline': 'HLT AK4-PF, 3.0<|#eta|<4.0, matched-to-Offline',
      'hltAK4PFJetsCorrected_HF2_MatchedToOffline': 'HLT AK4-PF, 4.0<|#eta|<5.0, matched-to-Offline',

      'hltAK4PFCHSJetsCorrected_EtaIncl_MatchedToGEN': 'HLT AK4-CHS matched-to-GEN',
      'hltAK4PFCHSJetsCorrected_HB_MatchedToGEN': 'HLT AK4-CHS, |#eta|<1.5, matched-to-GEN',
      'hltAK4PFCHSJetsCorrected_HGCal_MatchedToGEN': 'HLT AK4-CHS, 1.5<|#eta|<3.0, matched-to-GEN',
      'hltAK4PFCHSJetsCorrected_HF1_MatchedToGEN': 'HLT AK4-CHS, 3.0<|#eta|<4.0, matched-to-GEN',
      'hltAK4PFCHSJetsCorrected_HF2_MatchedToGEN': 'HLT AK4-CHS, 4.0<|#eta|<5.0, matched-to-GEN',

      'hltAK4PFCHSJetsCorrected_EtaIncl_MatchedToOffline': 'HLT AK4-CHS matched-to-Offline',
      'hltAK4PFCHSJetsCorrected_HB_MatchedToOffline': 'HLT AK4-CHS, |#eta|<1.5, matched-to-Offline',
      'hltAK4PFCHSJetsCorrected_HGCal_MatchedToOffline': 'HLT AK4-CHS, 1.5<|#eta|<3.0, matched-to-Offline',
      'hltAK4PFCHSJetsCorrected_HF1_MatchedToOffline': 'HLT AK4-CHS, 3.0<|#eta|<4.0, matched-to-Offline',
      'hltAK4PFCHSJetsCorrected_HF2_MatchedToOffline': 'HLT AK4-CHS, 4.0<|#eta|<5.0, matched-to-Offline',

      'hltAK4PuppiJetsCorrected_EtaIncl_MatchedToGEN': 'HLT AK4-Puppi matched-to-GEN',
      'hltAK4PuppiJetsCorrected_HB_MatchedToGEN': 'HLT AK4-Puppi, |#eta|<1.5, matched-to-GEN',
      'hltAK4PuppiJetsCorrected_HGCal_MatchedToGEN': 'HLT AK4-Puppi, 1.5<|#eta|<3.0, matched-to-GEN',
      'hltAK4PuppiJetsCorrected_HF1_MatchedToGEN': 'HLT AK4-Puppi, 3.0<|#eta|<4.0, matched-to-GEN',
      'hltAK4PuppiJetsCorrected_HF2_MatchedToGEN': 'HLT AK4-Puppi, 4.0<|#eta|<5.0, matched-to-GEN',

      'hltAK4PuppiJetsCorrected_EtaIncl_MatchedToOffline': 'HLT AK4-Puppi matched-to-Offline',
      'hltAK4PuppiJetsCorrected_HB_MatchedToOffline': 'HLT AK4-Puppi, |#eta|<1.5, matched-to-Offline',
      'hltAK4PuppiJetsCorrected_HGCal_MatchedToOffline': 'HLT AK4-Puppi, 1.5<|#eta|<3.0, matched-to-Offline',
      'hltAK4PuppiJetsCorrected_HF1_MatchedToOffline': 'HLT AK4-Puppi, 3.0<|#eta|<4.0, matched-to-Offline',
      'hltAK4PuppiJetsCorrected_HF2_MatchedToOffline': 'HLT AK4-Puppi, 4.0<|#eta|<5.0, matched-to-Offline',

      'ak4GenJetsNoNu_EtaIncl_pt' : 'GEN p_{T} [GeV]',
      'ak4GenJetsNoNu_EtaIncl_eta': 'GEN #eta',
      'ak4GenJetsNoNu_EtaIncl_phi': 'GEN #phi',

      'offlineAK4PFCHSJetsCorrected_EtaIncl_pt' : 'Offline p_{T} [GeV]',
      'offlineAK4PFCHSJetsCorrected_EtaIncl_eta': 'Offline #eta',
      'offlineAK4PFCHSJetsCorrected_EtaIncl_phi': 'Offline #phi',

      'offlineAK4PuppiJetsCorrected_EtaIncl_pt' : 'Offline p_{T} [GeV]',
      'offlineAK4PuppiJetsCorrected_EtaIncl_eta': 'Offline #eta',
      'offlineAK4PuppiJetsCorrected_EtaIncl_phi': 'Offline #phi',

      'Offline_pt' : 'Offline p_{T} [GeV]',
      'Offline_eta': 'Offline #eta',
      'Offline_phi': 'Offline #phi',

      'hltPFMET': 'HLT PF-MET',
      'hltPFMETTypeOne': 'HLT PF-MET Type-1',

      'hltPuppiMET': 'HLT Puppi-MET',
      'hltPuppiMETTypeOne': 'HLT Puppi-MET Type-1',

      'offlineMETs_Raw': 'Offline PF-MET Raw',
      'offlineMETsPuppi_Raw': 'Offline Puppi-MET Raw',

      'offlineNPV': 'Offline N_{PV}',

      'offlineMETs_Type1': 'Offline PF-MET Type-1',
      'offlineMETsPuppi_Type1': 'Offline Puppi-MET Type-1',

      'offlineMETs_Raw_pt': 'Offline MET [GeV]',
      'offlineMETsPuppi_Raw_pt': 'Offline MET [GeV]',
      'offlineMETs_Type1_pt': 'Offline MET [GeV]',
      'offlineMETsPuppi_Type1_pt': 'Offline MET [GeV]',

      'genMetTrue_pt': 'GEN MET [GeV]',
      'genMetTrue_phi': 'GEN #phi',
      'genMetTrue_sumEt': 'GEN Sum-E_{T} [GeV]',

      'phi_overGEN': '#phi / #phi^{GEN}',
      'phi_minusGEN': '#phi - #phi^{GEN}',

      'pt_paraToGEN': 'p_{T}^{#parallel GEN} [GeV]',
      'pt_paraToGEN_Mean': '<p_{T}^{#parallel GEN}> [GeV]',
      'pt_paraToGEN_RMS': '#sigma(p_{T}^{#parallel GEN}) [GeV]',
      'pt_paraToGEN_RMSScaledByResponse': '#sigma(p_{T}^{#parallel GEN}) / <p_{T} / p_{T}^{GEN}> [GeV]',
      'pt_paraToGENMinusGEN': 'p_{T}^{#parallel GEN} - p_{T}^{GEN} [GeV]',
      'pt_paraToGENMinusGEN_Mean': '<p_{T}^{#parallel GEN} - p_{T}^{GEN}> [GeV]',
      'pt_paraToGENMinusGEN_RMS': '#sigma(p_{T}^{#parallel GEN} - p_{T}^{GEN}) [GeV]',
      'pt_paraToGENMinusGEN_RMSScaledByResponse': '#sigma(p_{T}^{#parallel GEN} - p_{T}^{GEN}) / <p_{T} / p_{T}^{GEN}> [GeV]',
      'pt_perpToGEN': 'p_{T}^{#perp GEN} [GeV]',
      'pt_perpToGEN_Mean': '<p_{T}^{#perp GEN}> [GeV]',
      'pt_perpToGEN_RMS': '#sigma(p_{T}^{#perp GEN}) [GeV]',
      'pt_perpToGEN_RMSScaledByResponse': '#sigma(p_{T}^{#perp GEN}) / <p_{T} / p_{T}^{GEN}> [GeV]',

      'pt_paraToOffline': 'p_{T}^{#parallel Offl} [GeV]',
      'pt_paraToOffline_Mean': '<p_{T}^{#parallel Offl}> [GeV]',
      'pt_paraToOffline_RMS': '#sigma(p_{T}^{#parallel Offl}) [GeV]',
      'pt_paraToOffline_RMSScaledByResponse': '#sigma(p_{T}^{#parallel Offl}) / <p_{T} / p_{T}^{Offl}> [GeV]',
      'pt_paraToOfflineMinusOffline': 'p_{T}^{#parallel Offl} - p_{T}^{Offl} [GeV]',
      'pt_paraToOfflineMinusOffline_Mean': '<p_{T}^{#parallel Offl} - p_{T}^{Offl}> [GeV]',
      'pt_paraToOfflineMinusOffline_RMS': '#sigma(p_{T}^{#parallel Offl} - p_{T}^{Offl}) [GeV]',
      'pt_paraToOfflineMinusOffline_RMSScaledByResponse': '#sigma(p_{T}^{#parallel Offl} - p_{T}^{Offl}) / <p_{T} / p_{T}^{Offl}> [GeV]',
      'pt_perpToOffline': 'p_{T}^{#perp Offl} [GeV]',
      'pt_perpToOffline_Mean': '<p_{T}^{#perp Offl}> [GeV]',
      'pt_perpToOffline_RMS': '#sigma(p_{T}^{#perp Offl}) [GeV]',
      'pt_perpToOffline_RMSScaledByResponse': '#sigma(p_{T}^{#perp Offl}) / <p_{T} / p_{T}^{Offl}> [GeV]',

      'pt_minusGEN': 'p_{T} - p_{T}^{GEN} [GeV]',
      'pt_minusGEN_Mean': '<p_{T} - p_{T}^{GEN}> [GeV]',
      'pt_minusGEN_RMS': '#sigma(p_{T} - p_{T}^{GEN}) [GeV]',
      'pt_minusGEN_RMSScaledByResponse': '#sigma(p_{T} - p_{T}^{GEN}) / <p_{T} / p_{T}^{GEN}> [GeV]',

      'pt_overGEN': 'p_{T} / p_{T}^{GEN}',
      'pt_overGEN_Mean': '<p_{T} / p_{T}^{GEN}>',
      'pt_overGEN_RMS': '#sigma(p_{T} / p_{T}^{GEN})',
      'pt_overGEN_RMSScaledByResponse': '#sigma(p_{T} / p_{T}^{GEN}) / <p_{T} / p_{T}^{GEN}>',

      'pt_minusOffline': 'p_{T} - p_{T}^{Offl} [GeV]',
      'pt_minusOffline_Mean': '<p_{T} - p_{T}^{Offl}> [GeV]',
      'pt_minusOffline_RMS': '#sigma(p_{T} - p_{T}^{Offl}) [GeV]',
      'pt_minusOffline_RMSScaledByResponse': '#sigma(p_{T} - p_{T}^{Offl}) / <p_{T} / p_{T}^{Offl}> [GeV]',

      'pt_overOffline': 'p_{T} / p_{T}^{Offl}',
      'pt_overOffline_Mean': '<p_{T} / p_{T}^{Offl}>',
      'pt_overOffline_RMS': '#sigma(p_{T} / p_{T}^{Offl})',
      'pt_overOffline_RMSScaledByResponse': '#sigma(p_{T} / p_{T}^{Offl}) / <p_{T} / p_{T}^{Offl}>',

      'sumEt_minusGEN': 'SumEt - SumEt^{GEN} [GeV]',
      'sumEt_minusGEN_Mean': '<SumEt - SumEt^{GEN}> [GeV]',
      'sumEt_minusGEN_RMS': '#sigma(SumEt - SumEt^{GEN}) [GeV]',
      'sumEt_minusGEN_RMSScaledByResponse': '#sigma(SumEt - SumEt^{GEN}) / <SumEt / SumEt^{GEN}> [GeV]',

      'sumEt_overGEN': 'SumEt / SumEt^{GEN}',
      'sumEt_overGEN_Mean': '<SumEt / SumEt^{GEN}>',
      'sumEt_overGEN_RMS': '#sigma(SumEt / SumEt^{GEN})',
      'sumEt_overGEN_RMSScaledByResponse': '#sigma(SumEt / SumEt^{GEN}) / <SumEt / SumEt^{GEN}>',

      'sumEt_minusOffline': 'SumEt - SumEt^{Offl} [GeV]',
      'sumEt_minusOffline_Mean': '<SumEt - SumEt^{Offl}> [GeV]',
      'sumEt_minusOffline_RMS': '#sigma(SumEt - SumEt^{Offl}) [GeV]',
      'sumEt_minusOffline_RMSScaledByResponse': '#sigma(SumEt - SumEt^{Offl}) / <SumEt / SumEt^{Offl}> [GeV]',

      'sumEt_overOffline': 'SumEt / SumEt^{Offl}',
      'sumEt_overOffline_Mean': '<SumEt / SumEt^{Offl}>',
      'sumEt_overOffline_RMS': '#sigma(SumEt / SumEt^{Offl})',
      'sumEt_overOffline_RMSScaledByResponse': '#sigma(SumEt / SumEt^{Offl}) / <SumEt / SumEt^{Offl}>',

      'phi_minusGEN': '#phi - #phi^{GEN} [GeV]',
      'phi_minusGEN_Mean': '<#phi - #phi^{GEN}> [GeV]',
      'phi_minusGEN_RMS': '#sigma(#phi - #phi^{GEN}) [GeV]',
      'phi_minusGEN_RMSScaledByResponse': '#sigma(#phi - #phi^{GEN}) / <#phi / #phi^{GEN}> [GeV]',

      'phi_overGEN': '#phi / #phi^{GEN}',
      'phi_overGEN_Mean': '<#phi / #phi^{GEN}>',
      'phi_overGEN_RMS': '#sigma(#phi / #phi^{GEN})',
      'phi_overGEN_RMSScaledByResponse': '#sigma(#phi / #phi^{GEN}) / <#phi / #phi^{GEN}>',

      'phi_minusOffline': '#phi - #phi^{Offl} [GeV]',
      'phi_minusOffline_Mean': '<#phi - #phi^{Offl}> [GeV]',
      'phi_minusOffline_RMS': '#sigma(#phi - #phi^{Offl}) [GeV]',
      'phi_minusOffline_RMSScaledByResponse': '#sigma(#phi - #phi^{Offl}) / <#phi / #phi^{Offl}> [GeV]',

      'phi_overOffline': '#phi / #phi^{Offl}',
      'phi_overOffline_Mean': '<#phi / #phi^{Offl}>',
      'phi_overOffline_RMS': '#sigma(#phi / #phi^{Offl})',
      'phi_overOffline_RMSScaledByResponse': '#sigma(#phi / #phi^{Offl}) / <#phi / #phi^{Offl}>',

      'pt': 'p_{T} [GeV]',
      'pt0': 'leading-jet p_{T} [GeV]',
      'eta': '#eta',
      'phi': '#phi',
      'sumEt': 'Sum-E_{T} [GeV]',
      'mass': 'mass [GeV]',
      'dRmatch': '#DeltaR',
      'mass': 'mass [GeV]',
      'njets': 'number of jets',
      'chargedHadronEnergyFraction': 'chargedHadronEnergyFraction',
      'chargedHadronMultiplicity': 'chargedHadronMultiplicity',
      'neutralHadronEnergyFraction': 'neutralHadronEnergyFraction',
      'neutralHadronMultiplicity': 'neutralHadronMultiplicity',
      'electronEnergyFraction': 'electronEnergyFraction',
      'electronMultiplicity': 'electronMultiplicity',
      'photonEnergyFraction': 'photonEnergyFraction',
      'photonMultiplicity': 'photonMultiplicity',
      'muonEnergyFraction': 'muonEnergyFraction',
      'muonMultiplicity': 'muonMultiplicity',
    }

    the_dict = {}

    for _tmp in histo_dict_target:

        _tmp1 = _tmp[_tmp.rfind('/')+1:] if '/' in _tmp else _tmp

        if '_wrt_' in _tmp1:
           tmp_split = _tmp1.split('_wrt_')

           tx = tmp_split[1]
           ty = tmp_split[0]

           var0 = None
           for _tmp_var in [
             '_njets',
             '_pt',
             '_pt0',
             '_eta',
             '_phi',
             '_mass',
             '_dRmatch',
             '_sumEt',
             '_chargedHadronEnergyFraction',
             '_chargedHadronMultiplicity',
             '_neutralHadronEnergyFraction',
             '_neutralHadronMultiplicity',
             '_electronEnergyFraction',
             '_electronMultiplicity',
             '_photonEnergyFraction',
             '_photonMultiplicity',
             '_muonEnergyFraction',
             '_muonMultiplicity',
           ]:
             if _tmp_var in ty:
                var0 = _tmp_var
                break

           if var0 is None:
              KILL(_tmp)

           objtag = ty[:ty.find(var0)]

           ty = ty[ty.find(var0)+1:]

           the_dict[_tmp1] = {
             'titleX': tx if tx not in tags else tags[tx],
             'titleY': ty if ty not in tags else tags[ty],
             'Label': objtag if objtag not in tags else tags[objtag],
             'MarkerSize': 1.5,
             'PlotRatio': 1,
             'Draw': 'ep',
             'DrawLegend': 'ep',
             'DivideByBinWidth': 0,
           }

        else:
           tx = _tmp1

           var0 = None
           for _tmp_var in [
             '_njets',
             '_pt',
             '_pt0',
             '_eta',
             '_phi',
             '_mass',
             '_dRmatch',
             '_sumEt',
             '_chargedHadronEnergyFraction',
             '_chargedHadronMultiplicity',
             '_neutralHadronEnergyFraction',
             '_neutralHadronMultiplicity',
             '_electronEnergyFraction',
             '_electronMultiplicity',
             '_photonEnergyFraction',
             '_photonMultiplicity',
             '_muonEnergyFraction',
             '_muonMultiplicity',
           ]:
             if _tmp_var in tx:
                var0 = _tmp_var
                break

           DivideByBinWidth = 0
           for _tmp_var in [
             '_pt',
             '_pt0',
             '_eta',
             '_phi',
             '_mass',
             '_dRmatch',
             '_sumEt',
             '_chargedHadronEnergyFraction',
             '_chargedHadronMultiplicity',
             '_neutralHadronEnergyFraction',
             '_neutralHadronMultiplicity',
             '_electronEnergyFraction',
             '_electronMultiplicity',
             '_photonEnergyFraction',
             '_photonMultiplicity',
             '_muonEnergyFraction',
             '_muonMultiplicity',
           ]:
             if tx.endswith(_tmp_var):
                DivideByBinWidth = 1
                break

           if var0 is None:
              tx = var0 if var0 not in tags else tags[var0],
              objtag = None
#              KILL(_tmp)
           else:
              objtag = tx[:tx.find(var0)]
              tx = tx[tx.find(var0)+1:]
#              objtag = '' if objtag not in tags else tags[objtag]

           the_dict[_tmp1] = {
             'titleX': tx if tx not in tags else tags[tx],
             'titleY': 'Entries',
             'Label': objtag if objtag not in tags else tags[objtag],
             'MarkerSize': 0.,
             'Draw': 'hist,e0',
             'PlotRatio': 1,
             'DrawLegend': 'l',
             'DivideByBinWidth': DivideByBinWidth,
           }

    json.dump(the_dict, open('tmp.json', 'w'), sort_keys=True, indent=2)

    ### output files (plots)
    load_plot_style()

    ROOT.TGaxis.SetMaxDigits(4)

    histo_paths_common     = sorted([_tmp for _tmp in histo_dict_target.keys() if _tmp     in histo_dict_refern])
    histo_paths_onlyTarget = sorted([_tmp for _tmp in histo_dict_target.keys() if _tmp not in histo_dict_refern])
    histo_paths_onlyRefern = sorted([_tmp for _tmp in histo_dict_refern.keys() if _tmp not in histo_dict_target])

    kwargs = {

      'target_legend': str(opts.target_legend),

      'reference_legend': str(opts.reference_legend),

      'output_extensions': EXTS,

      'config': the_dict,
    }

    for histo_key in histo_paths_onlyTarget:
        plot_canvas(key=histo_key, output=os.path.abspath(opts.output)+'/only_target/'+histo_key.replace(' ', '_'), target=histo_dict_target[histo_key], reference=None, **kwargs)

    for histo_key in histo_paths_onlyRefern:
        plot_canvas(key=histo_key, output=os.path.abspath(opts.output)+'/only_reference/'+histo_key.replace(' ', '_'), target=None, reference=histo_dict_refern[histo_key], **kwargs)

    for histo_key in histo_paths_common:
        plot_canvas(key=histo_key, output=os.path.abspath(opts.output)+'/'+histo_key.replace(' ', '_'), target=histo_dict_target[histo_key], reference=histo_dict_refern[histo_key], **kwargs)
    ### -------------------
