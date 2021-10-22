#!/usr/bin/env python3
import ROOT
import array
import math
import random

#from utils import *

def get_histo_from_filepath(file_path, hpath, bins=[], auto_rebin=False):
    tfile = ROOT.TFile.Open(file_path)
    if not tfile: raise SystemExit

    h = get_histo_from_rootfile(tfile, hpath, bins, auto_rebin)

    tfile.Close()

    return h

def get_histo_from_rootfile(rootfile, hpath, bins=[], auto_rebin=False):
    if not rootfile: KILL('get_histo_from_rootfile -- input error: invalid input ROOT TFile object')

    h_ = rootfile.Get(hpath)
    if not h_:
       WARNING('get_histo_from_rootfile -- histogram not found: '+rootfile.GetName()+':'+hpath)
       return None

    h_ = get_histo_adjusted(h_, bins, auto_rebin)

    return h_

def get_histo_from_roottree(rootfile, bins=[], auto_rebin=False, **tree_dc):
    if not rootfile: KILL('get_histo_from_roottree -- input error: invalid input ROOT TFile object')

    tree_name = tree_dc.get('tree_name')
    tree_var  = tree_dc.get('tree_var')
    tree_cmd  = tree_dc.get('tree_cmd', '')

    h_name = tree_dc.get('h_name', 'tmp')

    h_xBinEdges = None
    if 'h_xBinEdges' in tree_dc:
        h_xBinEdges = get_binning(tree_dc.get('h_xBinEdges'))
    else:
       h_xBinN = tree_dc.get('h_xBinN')
       h_xMin  = tree_dc.get('h_xMin')
       h_xMax  = tree_dc.get('h_xMax')

    h_yBinEdges = None
    if 'h_yBinEdges' in tree_dc:
        h_yBinEdges = get_binning(tree_dc.get('h_yBinEdges'))
    else:
       h_yBinN = tree_dc.get('h_yBinN')
       h_yMin  = tree_dc.get('h_yMin')
       h_yMax  = tree_dc.get('h_yMax')

    make_th2 = bool((h_yBinEdges != None) and (h_yBinN != None) and (h_yMin != None) and (h_yMax != None))

    roottree = rootfile.Get(tree_name)
    if not roottree:
        input_ref = rootfile.GetName()+':'+tree_name
        KILL('get_histo_from_roottree -- TTree object not found in input ROOT TFile: '+input_ref)

    if make_th2 and bins != []:
       input_ref = rootfile.GetName()+':'+tree_name
       KILL('get_histo_from_roottree -- logic error: attempt to rebin TH2D object: '+input_ref)

    while ROOT.gDirectory.Get(h_name):
#       WARNING('get_histo_from_roottree -- object with name="'+h_name+'" already in memory: '+rootfile.GetName()+':'+tree_name)
       h_name = 'tmp'+str(random.randint(1, 1000))

    if make_th2:
       if h_xBinEdges and h_yBinEdges: h_ = ROOT.TH2D(h_name, h_name, len(h_xBinEdges)-1, h_xBinEdges, len(h_yBinEdges)-1, h_yBinEdges)
       else: h_ = ROOT.TH2D(h_name, h_name, int(h_xBinN), float(h_xMin), float(h_xMax), int(h_yBinN), float(h_yMin), float(h_yMax))

    else:
       if h_xBinEdges: h_ = ROOT.TH1D(h_name, h_name, len(h_xBinEdges)-1, h_xBinEdges)
       else: h_ = ROOT.TH1D(h_name, h_name, int(h_xBinN), float(h_xMin), float(h_xMax))

    roottree.Draw(tree_var+'>>'+h_name, tree_cmd, 'goff')

    h_ = get_histo_adjusted(h_, bins, auto_rebin)

    return h_

def get_histo_adjusted(h, bins=[], auto_rebin=False):
    if bins: h = get_rebinned_histo(h, bins, auto_rebin)
    if not h.GetSumw2N(): h.Sumw2()

    h.UseCurrentStyle()
    h.SetDirectory(0)

    return h

def bins(binN, xmin, xmax, keep_xmin=False):
    bin_list = list()
    for i in range(int(not keep_xmin), binN+1):
        bin_list.append(xmin + i * float(xmax-xmin)/binN)

    return bin_list

def get_binning(bin_ls):
    bins = sorted(list(set(bin_ls)))
    return array.array('d', bins)

def get_rebinned_histo(h, bin_ls, auto_rebin=False, force_rebin=False):

    if not bin_ls: pass

    elif len(bin_ls) == 1:

        if bin_ls[0] == -1:
           h = get_rebinned_histo_1bin(h, True)

        else:
           rebin_fac = bin_ls[0]

           if force_rebin or not auto_rebin:

              if h.GetNbinsX()%rebin_fac:
                 (WARNING if force_rebin else KILL)('get_rebinned_histo -- invalid rebinning factor ('+str(rebin_fac)+') for TH1 object [TH1::GetName()="'+h.GetName()+'"]')

              h.Rebin(rebin_fac)

           else:
              if rebin_fac > h.GetNbinsX(): rebin_fac = h.GetNbinsX()

              while h.GetNbinsX()%rebin_fac: rebin_fac += 1

              if rebin_fac != bin_ls[0]:
                 WARNING('get_rebinned_histo -- applied auto-rebinning, changed rebinning factor from '+str(bin_ls[0])+' to '+str(rebin_fac)+' [TH1::GetName()="'+h.GetName()+'"]')

              h.Rebin(rebin_fac)

    else:
        bins = get_binning(bin_ls)
        h = h.Rebin(len(bins)-1, h.GetName(), bins)

    return h

def get_rebinned_histo_1bin(h, merge_outflow=True):
    h = get_rebinned_histo(h, [h.GetBinLowEdge(1), h.GetBinLowEdge(h.GetNbinsX()+1)])

    if merge_outflow:
        h.AddBinContent(1, h.GetBinContent(0) + h.GetBinContent(h.GetNbinsX()+1))
        h.SetBinError  (1, math.sqrt(math.pow(h.GetBinError(1), 2) + math.pow(h.GetBinError(0), 2) + math.pow(h.GetBinError(h.GetNbinsX()+1), 2)))

    h.SetBinContent(0, 0.)
    h.SetBinError  (0, 0.)

    h.SetBinContent(h.GetNbinsX()+1, 0.)
    h.SetBinError  (h.GetNbinsX()+1, 0.)

    return h

def get_rebinned_histo2D(h, binX_ls, binY_ls):

    bX = get_binning(binX_ls)
    bY = get_binning(binY_ls)

    h1 = h.Clone()
    h1.Reset()
    h1.SetBins(len(bX)-1, bX, len(bY)-1, bY)

    for j in range(1, h.GetYaxis().GetNbins()):
        for i in range(1, h.GetXaxis().GetNbins()):
            h1.Fill(h.GetXaxis().GetBinCenter(i), h.GetYaxis().GetBinCenter(j), h.GetBinContent(i,j))

    return h1

def get_histo_projection(h2, axis, vmin=None, vmax=None, bin_ls=[]):

    if not h2: KILL('get_histo_projection -- null input histogram')

    if vmin==None and vmax==None: bmin, bmax = 0, -1
    elif axis == 'x': bmin, bmax = h2.GetYaxis().FindBin(float(vmin)), h2.GetYaxis().FindBin(float(vmax))-1
    elif axis == 'y': bmin, bmax = h2.GetXaxis().FindBin(float(vmin)), h2.GetXaxis().FindBin(float(vmax))-1
    else: KILL('get_histo_projection -- undefined value for "axis" argument: '+axis)

    if   axis == 'x': h = h2.ProjectionX(h2.GetName()+'__'+axis, bmin, bmax);
    elif axis == 'y': h = h2.ProjectionY(h2.GetName()+'__'+axis, bmin, bmax);
    else: KILL('get_histo_projection -- undefined value for "axis" argument: '+axis)

    h = get_histo_adjusted(h, bin_ls)

    return h

def pseudoDATA_histogram(h0, tag=''):

    bin_ls = []
    for b in range(1, h0.GetNbinsX()+2): bin_ls.append(h0.GetBinLowEdge(b))
    bins = array.array('d', sorted(bin_ls))

    h = ROOT.TH1D(h0.GetName()+'_pseudoDATA'+tag, h0.GetName()+'_pseudoDATA'+tag, h0.GetNbinsX(), bins)

    rand = ROOT.TRandom3()

    for b in range(0, h.GetNbinsX()+2):

        val0 = h0.GetBinContent(b)
        err0 = h0.GetBinError(b)

        val = rand.Gaus(val0, err0)
        val = round(val) if val > 0. else 0.

        err = math.sqrt(val)

        h.SetBinContent(b, val)
        h.SetBinError  (b, err)

    return h

def add_normalization_uncertainty(h_, unc_):

    if not h_.GetSumw2N(): h_.Sumw2()

    for i in range(0, h_.GetSize()):
        sys = h_.GetBinContent(i) * unc_
        err = math.sqrt(h_.GetBinError(i) * h_.GetBinError(i) + sys * sys)
        h_.SetBinError(i, err)

    return

def th1_SoverSqrtB(signal, background, reverse=False):

    h_1 = signal.Clone()
    h_1.Reset()

    for i_b in range(1, 1+h_1.GetNbinsX()):

        if signal.GetBinLowEdge(i_b) != background.GetBinLowEdge(i_b):
           KILL('th1_SoverSqrtB -- input error: input templates with different binning')

        v_bkg = (background.Integral(0, i_b) if reverse else background.Integral(i_b, -1))

        if not (v_bkg > 0.): continue

        v_sig = (signal.Integral(0, i_b) if reverse else signal.Integral(i_b, -1))

        h_1.SetBinContent(i_b, v_sig / math.sqrt(v_bkg))
        h_1.SetBinError  (i_b, 0.)

    return h_1

def th1_mergeUnderflowBinIntoFirstBin(th1):

    th1_new = th1.Clone()

    if th1_new.GetBinContent(0) != 0.:

       th1_new.SetName(th1.GetName() +'_withUnderflow')

       th1_new.SetBinContent(1, th1_new.GetBinContent(0) + th1_new.GetBinContent(1))
       th1_new.SetBinError  (1, math.sqrt(math.pow(th1_new.GetBinError(0), 2) + math.pow(th1_new.GetBinError(1), 2)))

       th1_new.SetBinContent(0, 0.0)
       th1_new.SetBinError  (0, 0.0)

    return th1_new

def th1_mergeOverflowBinIntoLastBin(th1):

    th1_new = th1.Clone()

    if th1_new.GetBinContent(th1_new.GetNbinsX() + 1) != 0.:

       th1_new.SetName(th1.GetName() +'_withOverflow')

       th1_new.SetBinContent(th1_new.GetNbinsX(), th1_new.GetBinContent(th1_new.GetNbinsX()) + th1_new.GetBinContent(th1_new.GetNbinsX() + 1))
       th1_new.SetBinError  (th1_new.GetNbinsX(), math.sqrt(math.pow(th1_new.GetBinError(th1_new.GetNbinsX()), 2) + math.pow(th1_new.GetBinError(th1_new.GetNbinsX() + 1), 2)))

       th1_new.SetBinContent(th1_new.GetNbinsX() + 1, 0.0)
       th1_new.SetBinError  (th1_new.GetNbinsX() + 1, 0.0)

    return th1_new
