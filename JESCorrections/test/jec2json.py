#!/usr/bin/env python

# Writing JECs into a json file for plotting
# 22042024/S.Lehti
# Usage: jec2json.py jec-txt-file

import os,sys,re
import json
import ROOT
import datetime

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

def writejson(x,y,xlabel,ylabel,originalfilename,filename,customtext=""):
    data = {}

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    now = datetime.datetime.now()
    data['date'] = "produced: %s %s"%(days[now.weekday()],now)

    data['originalfile'] = originalfilename
    data['x'] = x
    data['xlabel'] = xlabel
    data['y'] = y
    data['ylabel'] = ylabel

    data['customtext'] = customtext

    origfname = re.sub('\.txt$', '', originalfilename)
    with open('%s_%s.json'%(filename,origfname), 'w') as f:
        json.dump(data, f, indent=4)

    

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
        rho = 25
        for eta in etarange:
            etastr = "eta%s"%eta
            etastr = etastr.replace('.','p')
            etatext = "Jet eta = %s"%eta
            for fIN in correctionfiles:
                jec = JEC(fIN)
                x = []
                y = []
                for pt in ptrange:
                    corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                    x.append(pt)
                    y.append(corr)
                writejson(x,y,"Jet p_{T} (GeV)","JEC",fIN,"jecs_pt_"+etastr,etatext)

        #BPix
        etarange = [-0.5]
        phi = -1.0
        rho = 25
        for eta in etarange:
            etastr = "BPix_eta%sphi%s"%(eta,phi)
            etastr = etastr.replace('.','p')
            etastr = etastr.replace('-','m')
            etatext = "BPix, Jet eta = %s, phi = %s"%(eta,phi)
            for fIN in correctionfiles:
                jec = JEC(fIN)
                x = []
                y = []
                for pt in ptrange:
                    corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                    x.append(pt)
                    y.append(corr)
                writejson(x,y,"Jet p_{T} (GeV)","JEC",fIN,"jecs_pt_"+etastr,etatext)

    if opts.eta:
        etarange = list(map(lambda x: x/100.0, range(-500, 501)))
        ptrange = [30, 100, 300]

        phi = 0
        jetA = 5
        rho = 25
        for pt in ptrange:
            ptstr = "pt%s"%pt
            pttext = "Jet pt = %s GeV"%pt
            for fIN in correctionfiles:
                jec = JEC(fIN)
                x = []
                y = []
                for eta in etarange:
                    corr = jec.getCorrection(pt,eta,phi,jetA,rho)
                    x.append(eta)
                    y.append(corr)
                writejson(x,y,"Jet eta","JEC",fIN,"jecs_eta_"+ptstr,pttext)


if __name__=="__main__":

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--pt", dest="pt", default=False, action="store_true",
                      help="Plot as a function of JetPt only [default: False]")
    parser.add_option("--eta", dest="eta", default=False, action="store_true",
                      help="Plot as a function of JetEta only [default: False]")

    (opts, args) = parser.parse_args()

    if not (opts.pt or opts.eta):
        opts.pt = True
        opts.eta = True

    main(opts, args)
