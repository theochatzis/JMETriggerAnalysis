#!/usr/bin/env python

# Plotting JECs from txt files
# 09042024/S.Lehti
# Usage: plotJECs.py ref-jec-file jec-file --pt --eta

import os,sys,re
import array

import ROOT

from optparse import OptionParser

def usage():
    print
    print("### Usage:  ",os.path.basename(sys.argv[0]),"inputfile(s)")
    print
    sys.exit()

class JEC:
    def __init__(self,filename):
        self.data = []

        print("JEC",filename)
        fIN = open(filename)

        firstline = fIN.readline()
        firstline = firstline.replace('{','')
        firstline = firstline.replace('}','')
        firstline = firstline.split()

        nVariations = int(firstline[0])
        self.variations = firstline[1:][:nVariations]

        nVariables = int(firstline[1+nVariations])
        self.variables = firstline[1+nVariations+1:][:nVariables]

        self.expression = firstline[1+nVariations+1+nVariables]

        self.name = firstline[-1]

        for line in fIN:
            dataline_str = " ".join(line.split())
            if len(dataline_str) == 0:
                continue

            dataline_str = dataline_str.split()
            dataline_float = [float(string) for string in dataline_str]
            self.data.append(dataline_float)

    def getCorrection(self,JetPt,JetEta,JetPhi,JetA,Rho):

        dataline = []
        for d in self.data:
            if len(self.variations) == 1:
                if d[0] <= JetEta and JetEta <= d[1]:
                    dataline = d
                    break
            if len(self.variations) == 2:
                if d[0] <= JetEta and JetEta <= d[1] and d[2] <= JetPhi and JetPhi <= d[3]:
                    dataline = d
                    break

        params = dataline[-int(dataline[2*len(self.variations)]-2*len(self.variables)):]
        ranges = []
        for i in range(len(self.variables)):
            ranges.append(dataline[2*len(self.variations)+1+2*i:2*len(self.variations)+1+2*i+2])

        if len(self.variables) == 1:
            func = ROOT.TF1("func",self.expression,ranges[0][0],ranges[0][1])
            for i,p in enumerate(params):
                func.SetParameter(i,p)
            x = JetPt
            import math
            #print("should",max(0.0001,params[0]+(params[1]/(pow(math.log10(x),2)+params[2]))+(params[3]*math.exp(-(params[4]*((math.log10(x)-params[5])*(math.log10(x)-params[5])))))+(params[6]*math.exp(-(params[7]*((math.log10(x)-params[8])*(math.log10(x)-params[8])))))))
            #print("value",func.Eval(JetPt))
            return func.Eval(JetPt)
        if len(self.variables) == 3:
            func = ROOT.TF3("func",self.expression,ranges[0][0],ranges[0][1],ranges[1][0],ranges[1][1],ranges[2][0],ranges[2][1])
            for i,p in enumerate(params):
                func.SetParameter(i,p)
            #print("input3",Rho,JetPt,JetA)
            #print("param3",params)
            x = Rho
            y = JetPt
            z = JetA
            import math
            #print("should",max(0.0001,1-(z/y)*(params[0]+(params[1]*(x))*(1+params[2]*math.log(y)))))
            #print("value",func.Eval(Rho,JetPt,JetA))
            #print("formula",func.GetFormula().GetExpFormula(),func.GetFormula().GetParameter(0),func.GetFormula().GetParameter(1),func.GetFormula().GetParameter(2))
            return func.Eval(Rho,JetPt,JetA)

        return 1.0

def plot(x,y,xlabel,ylable,filename,customtext=""):

    colors = [ROOT.kBlack,ROOT.kRed,ROOT.kBlue,ROOT.kMagenta]
    
    canvas = ROOT.TCanvas("canvas","",500,500)
    canvas.cd()

    if len(y) > 1:
        a1 = 0.01
        b1 = 0.33
        a2 = 0.99
        b2 = 0.99
        graphpad = ROOT.TPad("graphpad","graphpad",a1,b1,a2,b2)
        graphpad.SetTopMargin(0.04)
        graphpad.SetRightMargin(0.04)
        graphpad.SetLeftMargin(0.14)
        graphpad.SetBottomMargin(0)
        graphpad.Draw()
        graphpad.cd()
    else:
        canvas.SetTopMargin(0.04)
        canvas.SetRightMargin(0.04)
        canvas.SetLeftMargin(0.14)
        canvas.SetBottomMargin(0.14)


    graphFrame = ROOT.TH2F("frame","",len(x),min(x),max(x),2,0,2)
    graphFrame.SetStats(0)
    graphFrame.GetXaxis().SetTitle(xlabel)
    graphFrame.GetXaxis().SetTitleOffset(1.2)
    graphFrame.GetXaxis().SetTitleSize(0.05)
    graphFrame.GetYaxis().SetTitleSize(0.05)
    graphFrame.GetYaxis().SetTitleOffset(1.2)
    graphFrame.GetYaxis().SetTitle(ylable)
    graphFrame.Draw()

    if len(customtext) > 0:
        text = ROOT.TText(0.2,0.9,customtext)
        text.SetNDC(True)
        text.Draw()

    jec_re = re.compile("(?P<jec>\S+)_(?P<level>L\w+)_(?P<jet>\w+)\.txt")

    legendtitle = "Empty Title"
    filetitle = ""
    legendgraphs = {}
    y_reference = None
    y_ratios = {}

    for i,key in enumerate(y.keys()):
        x_values = array.array('d',x)
        y_values = array.array('d',y[key])

        if y_reference == None:
            y_reference = y_values
        else:
            gtr1 = False
            ratios = []
            for j in reversed(range(len(y_reference))):
                ratio = y_values[j]/y_reference[j]
                if y_values[j] < 0.0002:
                    ratio = y_values[j]
                if y_reference[j] < 0.0002 and gtr1:
                    ratio = 999
                if ratio > 1:
                    gtr1 = True
                else:
                    gtr1 = False
                ratios.append(ratio)
            ratios = list(reversed(ratios))
            y_ratios[key] = ratios

        graph = ROOT.TGraph(len(x),x_values,y_values)
        graph.SetName("graph%s"%i)
        graph.SetMarkerColor(colors[i])
        graph.SetLineColor(colors[i])
        graph.Draw("LSAME")

        corrname = "NamelessJEC"
        match = jec_re.search(key)
        if match:
            corrname = match.group("jec")
            legendtitle = match.group("level")+' '+match.group("jet")
            filetitle = legendtitle.replace(' ','_')
        legendgraphs[corrname] = graph

    legend = ROOT.TLegend(0.5,0.75,0.96,0.96)
    legend.SetHeader(legendtitle,"C")
    for key in legendgraphs.keys():
        legend.AddEntry(legendgraphs[key],key)
    legend.Draw()

    canvas.cd()

    if len(y) > 1:
        a1 = 0.01
        b1 = 0.01
        a2 = 0.99
        b2 = 0.33
        ratiopad = ROOT.TPad("ratiopad","",a1,b1,a2,b2)
        ratiopad.SetTopMargin(0)
        ratiopad.SetRightMargin(0.04)
        ratiopad.SetLeftMargin(0.14)
        ratiopad.SetBottomMargin(0.3)
        ratiopad.SetFrameBorderMode(0)
        ratiopad.Draw()
        ratiopad.cd()
        ratioFrame = ROOT.TH2F("rframe","",2,graphFrame.GetXaxis().GetBinLowEdge(1),graphFrame.GetXaxis().GetBinLowEdge(graphFrame.GetNbinsX()+1),2,0.9,1.1)
        ratioFrame.SetStats(0)
        ratioFrame.GetXaxis().SetTitle(xlabel)
        titlescale = 2
        ratioFrame.GetXaxis().SetTitleSize(titlescale*graphFrame.GetXaxis().GetTitleSize())
        ratioFrame.GetXaxis().SetLabelSize(titlescale*graphFrame.GetXaxis().GetLabelSize())
        ratioFrame.GetYaxis().SetTitleSize(titlescale*graphFrame.GetYaxis().GetTitleSize())
        ratioFrame.GetYaxis().SetLabelSize(titlescale*graphFrame.GetYaxis().GetLabelSize())
        ratioFrame.GetYaxis().SetTitleOffset(0.65)
        ratioFrame.GetYaxis().SetTitle("Ratio  ")
        ratioFrame.Draw()

        line = ROOT.TLine(min(x),1,max(x),1)
        line.SetLineColor(ROOT.kRed)
        line.SetLineStyle(2)
        line.Draw()
    
        for key in y_ratios.keys():
            x_values = array.array('d',x)
            y_values = array.array('d',y_ratios[key])
            graphr = ROOT.TGraph(len(x),x_values,y_values)
            graphr.SetName(key)
            graphr.Draw("LSAME")

    if len(filetitle) > 0:
        filename += '_' + filetitle

    canvas.SaveAs(filename+".pdf")
    #canvas.SaveAs(filename+".C")

def main(opts, args):

    if len(args) == 0:
        usage()

    correctionfiles = []
    for arg in args:
        if os.path.isfile(arg):
            correctionfiles.append(arg)

    x = []
    y = {}
    if opts.pt:
        ptrange = range(1,500)
        etarange = [0, 1.3, 2, 2.7, 3.5]

        phi = 0
        jetA = 5
        rho = 10
        for eta in etarange:
            etastr = "eta%s"%eta
            etastr = etastr.replace('.','p')
            etatext = "Jet eta = %s"%eta
            for fIN in correctionfiles:
                jec = JEC(fIN)
                x = []
                y[fIN] = []
                for pt in ptrange:
                    corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                    x.append(pt)
                    y[fIN].append(corr)
            plot(x,y,"Jet p_{T} (GeV)","JEC","jecs_pt_"+etastr,etatext)
    if opts.eta:
        etarange = list(map(lambda x: x/100.0, range(-500, 501)))
        ptrange = [30, 100, 300]

        phi = 0 
        jetA = 5
        rho = 10
        for pt in ptrange:
            ptstr = "pt%s"%pt
            pttext = "Jet pt = %s GeV"%pt
            for fIN in correctionfiles:
                jec = JEC(fIN)
                x = []
                y[fIN] = [] 
                for eta in etarange:
                    corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                    x.append(eta)
                    y[fIN].append(corr)
            plot(x,y,"Jet eta","JEC","jecs_eta_"+ptstr,pttext)

if __name__=="__main__":

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--pt", dest="pt", default=False, action="store_true",
                      help="Plot as a function of JetPt [default: False")
    parser.add_option("--eta", dest="eta", default=False, action="store_true",
                      help="Plot as a function of JetEta [default: False")
    (opts, args) = parser.parse_args()
    main(opts, args)
