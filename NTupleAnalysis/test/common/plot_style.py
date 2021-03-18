#!/usr/bin/env python
import ROOT

def get_style(type_=0):

    s = ROOT.TStyle('swagger', 'plot swagger')

    # For the canvas:
    s.SetCanvasColor(ROOT.kWhite)
    s.SetCanvasBorderMode(0)
    s.SetCanvasDefX(0)
    s.SetCanvasDefY(0)
    s.SetCanvasDefW(800)
    if type_ == 2: s.SetCanvasDefH(625)
    else: s.SetCanvasDefH(725)

    # For the Pad:
    s.SetPadBorderMode(0)
    # s.SetPadBorderSize(1)
    s.SetPadColor(ROOT.kWhite)
    s.SetPadGridX(False)
    s.SetPadGridY(False)
    s.SetGridColor(0)
    s.SetGridStyle(3)
    s.SetGridWidth(1)

    # For the frame:
    s.SetFrameBorderMode(0)
    s.SetFrameBorderSize(1)
    s.SetFrameFillColor(0)
    s.SetFrameFillStyle(0)
    s.SetFrameLineColor(1)
    s.SetFrameLineStyle(1)
    s.SetFrameLineWidth(1)

    # For the histo:
    # s.SetHistFillColor(1)
    # s.SetHistFillStyle(0)
    s.SetHistLineColor(4)
    s.SetHistLineStyle(0)
    s.SetHistLineWidth(1)
    # s.SetLegoInnerR(0.5)
    # s.SetNumberContours(20)

    s.SetEndErrorSize(2)
    # s.SetErrorMarker(20)
    #s.SetErrorX(0.)
    
    s.SetMarkerStyle(20)
    
    #For the fit/function:
    s.SetOptFit(1)
    s.SetFitFormat('5.4g')
    s.SetFuncColor(2)
    s.SetFuncStyle(1)
    s.SetFuncWidth(1)

    #For the date:
    s.SetOptDate(0)
    # s.SetDateX(0.01)
    # s.SetDateY(0.01)

    # For the statistics box:
    s.SetOptFile(0)
    if type_ == 2: s.SetOptStat(1)
    else: s.SetOptStat(0)
    s.SetStatColor(ROOT.kWhite)
    s.SetStatFont(42)
    s.SetStatFontSize(0.025)
    s.SetStatTextColor(1)
    s.SetStatFormat('6.4g')
    s.SetStatBorderSize(1)
    s.SetStatH(0.1)
    s.SetStatW(0.15)
    # s.SetStatStyle(1001)
    # s.SetStatX(0)
    # s.SetStatY(0)

    # Margins:
    s.SetPadTopMargin(0.08)
    s.SetPadBottomMargin(0.15)
    if type_ == 0:
       s.SetPadLeftMargin(0.15)
       s.SetPadRightMargin(0.04)
    elif type_ == 2:
       s.SetPadLeftMargin (0.12)
       s.SetPadRightMargin(0.12)
    else:
       s.SetPadLeftMargin(0.14)
       s.SetPadRightMargin(0.04)

    # For the Global title:
    s.SetOptTitle(1)
#    s.SetTitleStyle(1001)
    s.SetTitleFont(42)
    s.SetTitleColor(1)
    s.SetTitleTextColor(1)
    s.SetTitleFillColor(10)
    s.SetTitleFontSize(.05*.95)
#    s.SetTitleAlign(23)
#    s.SetTitleBorderSize(0)
#    s.SetTitleX(s.GetPadLeftMargin()+(1-s.GetPadRightMargin()-s.GetPadLeftMargin())*.50)
#    s.SetTitleY((1-s.GetPadTopMargin())+s.GetPadTopMargin()*.9)
##    s.SetTitleH(s.GetPadTopMargin()*.80)
##    s.SetTitleW(.50)

    # For the axis titles:
    s.SetTitleColor(1, 'XYZ')
    s.SetTitleFont(42, 'XYZ')
    s.SetTitleSize(.05*.95, 'XYZ')
    if   type_ == 0:
        s.SetTitleOffset(1.25, 'X')
        s.SetTitleOffset(1.45, 'Y')
    elif type_ == 2:
        s.SetTitleOffset(1.20, 'X')
        s.SetTitleOffset(1.23, 'Y')
    else:
        s.SetTitleOffset(1.15, 'X')
        s.SetTitleOffset(1.40, 'Y')

    # For the axis labels:
    s.SetLabelColor(1, 'XYZ')
    s.SetLabelFont(42, 'XYZ')
    s.SetLabelOffset(0.005, 'XYZ')
    s.SetLabelSize(0.0425, 'XYZ')

    s.SetPalette(57)

    s.SetPadTickX(1)
    s.SetPadTickY(1)

    return s
