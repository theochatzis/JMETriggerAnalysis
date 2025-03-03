#!/usr/bin/env python3
import ROOT
import math
import ctypes

from common.th1 import *

def get_efficiency(hP, hT):
    hP1, hT1 = hP.Clone(), hT.Clone()

    hP1 = get_rebinned_histo_1bin(hP1, True)
    hT1 = get_rebinned_histo_1bin(hT1, True)

    g = ROOT.TGraphAsymmErrors(hP1, hT1, 'cl=0.683 b(1,1) mode')
    if g.GetN() != 1:
        WARNING('get_global_efficiency -- failed efficiency computation: '+hP1.GetName()+' / '+hT1.GetName()+' [N='+str(g.GetN())+']')
        return [0., 0., 0.]

    x, y = ctypes.c_double(0.), ctypes.c_double(0.)
    g.GetPoint(0, x, y)

    eff = [y, g.GetErrorYhigh(0), g.GetErrorYlow(0)]

    del hP1, hT1, g

    return eff

def get_efficiency_graph(hP, hT, bin_ls=[]):
    hP1, hT1 = hP.Clone(), hT.Clone()

    hP1 = get_rebinned_histo(hP1, bin_ls)
    hT1 = get_rebinned_histo(hT1, bin_ls)

    eff = ROOT.TGraphAsymmErrors(hP1, hT1, 'cl=0.683 b(1,1) mode')

    del hP1, hT1

    return eff

def get_ratio_graph(g_num_, g_den_, verbose=False):

    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetLineColor(g_num_.GetLineColor())
    ratio.SetLineStyle(g_num_.GetLineStyle())
    ratio.SetLineWidth(g_num_.GetLineWidth())
    ratio.SetMarkerColor(g_num_.GetMarkerColor())
    ratio.SetMarkerStyle(g_num_.GetMarkerStyle())
    ratio.SetMarkerSize(g_num_.GetMarkerSize())

    n = -1
    for i in range(g_den_.GetN()):

        xdc, ydc = ctypes.c_double(0.), ctypes.c_double(0.)
        g_den_.GetPoint(i, xdc, ydc)

        xd = xdc.value
        yd = ydc.value

        for j in range(g_num_.GetN()):
            xnc, ync = ctypes.c_double(0.), ctypes.c_double(0.)
            g_num_.GetPoint(j, xnc, ync)

            xn = xnc.value
            yn = ync.value

            if xn != xd: continue

            if yn and (not yd):
               if verbose:
                  WARNING('get_ratio_graph: null denominator value: N='+str(i)+' [num = '+g_num_.GetName()+', den = '+g_den_.GetName()+']')
               continue

            n += 1
            r = yn/yd if yd else 1.
            ratio.SetPoint(n, xn, r)
            ratio.SetPointEXhigh(n, g_num_.GetErrorXhigh(j))
            ratio.SetPointEXlow (n, g_num_.GetErrorXlow (j))

            # up error
            up = 0.
            if yd:
               un = g_num_.GetErrorYhigh(j)
               ud = g_den_.GetErrorYlow (i) * r
               up = (1./yd) * math.sqrt(un*un+ud*ud)
            ratio.SetPointEYhigh(n, up)

            # down error
            dw = 0.
            if yd:
               dn = g_num_.GetErrorYlow (j)
               dd = g_den_.GetErrorYhigh(i) * r
               dw = (1./yd) * math.sqrt(dn*dn+dd*dd)
            ratio.SetPointEYlow(n, dw)

    return ratio

def getFirstXValueWithYValueAbove(tgraphae, yMin):
    xyvals = []
    for p_i in range(effg.GetN()):
      xd, yd = ctypes.c_double(0.), ctypes.c_double(0.)
      effg.GetPoint(p_i, xd, yd)
      xyvals += [[xd-effg.GetErrorXlow(p_i), yd]]

    xyvals = sorted(xyvals, key=lambda x: x[0])

    ret = None
    for [x0, y0] in xyvals:
      if y0 > yMin:
        ret = x0
        break

    return ret
