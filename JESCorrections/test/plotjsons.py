#!/usr/bin/env python

# Plotting JECs from txt files
# 09042024/S.Lehti
# Usage: plotjsons.py json-files                                                                                          

import os,sys,re
import json
import array

import ROOT

from optparse import OptionParser

def usage():
    print
    print("### Usage:  ",os.path.basename(sys.argv[0]),"inputfile(s)")
    print
    sys.exit()

jec_re = re.compile("(?P<prefix>jecs_\w+?_\w+?)_(?P<jec>\S+)_(?P<level>L\w+)_(?P<jet>\w+)")

def plot(x,y,opts):
    print("Number of graphs",len(y.keys()))
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
    graphFrame.GetXaxis().SetTitle(opts.xTitle)
    graphFrame.GetXaxis().SetTitleOffset(1.2)
    graphFrame.GetXaxis().SetTitleSize(0.05)
    graphFrame.GetYaxis().SetTitleSize(0.05)
    graphFrame.GetYaxis().SetTitleOffset(1.2)
    graphFrame.GetYaxis().SetTitle(opts.yTitle)
    graphFrame.Draw()

    if len(opts.customtext) > 0:
        text = ROOT.TText(0.2,0.965,opts.customtext)
        text.SetNDC(True)
        text.Draw()

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
            if len(y.keys()) > 1:
                opts.filename = "%s_%s_%s"%(match.group("prefix"),match.group("level"),match.group("jet"))
        legendgraphs[key] = graph

    if len(opts.graphTitles) > 0:
        if len(opts.graphTitles) == len(legendgraphs.keys()):
            newlegendgraphs = {}
            oldvalues = list(legendgraphs.keys())
            for i in range(len(y.keys())):
                oldvalue = oldvalues[i]
                newvalue = opts.graphTitles[i]
                newlegendgraphs[newvalue] = legendgraphs[oldvalue]
            legendgraphs = newlegendgraphs
        else:
            print("Number of graphs and command line parameter legend labels do not match")
            print("    Graphs: %s, legend labels: %s"%(len(y.keys()),len(opts.graphTitles)))
            sys.exit()

    legend = ROOT.TLegend(0.5,0.75,0.96,0.96)
    legend.SetHeader(opts.legendTitle,"C")
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
        ratioFrame.GetXaxis().SetTitle(opts.xTitle)
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

#    if len(filetitle) > 0:
#        opts.filename += '_' + filetitle

    canvas.cd()
    if len(opts.text) > 0:
        for t in opts.text:
            text = ROOT.TText(float(t[1]),float(t[2]),t[0])
            text.SetNDC(True)
            text.DrawClone()

    canvas.SaveAs(opts.filename+".pdf")
    #canvas.SaveAs(opts.filename+".png")

def main(opts, args):

    if len(args) == 0:
        usage()

    jsonfiles = []
    for arg in args:
        if os.path.isfile(arg):
            jsonfiles.append(arg)
    x = []
    y = {}

    xlable = "x-label"
    ylable = "y-label"
    filename = jsonfiles[0]
#    customtext = ""


    for jsonfile in jsonfiles:
        fIN = open(jsonfile,'r')
        data = json.load(fIN)
        fname = re.sub('\.json$', '', jsonfile)
        if len(x) == 0:
            x = data['x']
            if opts.xTitle == "None":
                opts.xTitle = data['xlabel']
            if opts.yTitle == "None":
                opts.yTitle = data['ylabel']
            if opts.filename == "None":
                opts.filename = fname
            if opts.legendTitle == "None":
                match = jec_re.search(jsonfile)
                if match:
                    if opts.jec == "None":
                        opts.jec = match.group("jec")
                    opts.legendTitle = match.group("level")+' '+match.group("jet")
                    filetitle = opts.legendTitle.replace(' ','_')
        else:
            if not x == data['x']:
                print("x-axis not matching")
                print("    bins: %s, %s"%(len(x),len(data['x'])))
                sys.exit()
        y[fname] = data['y']

    plot(x,y,opts)

if __name__=="__main__":

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-x", "--x-title", dest="xTitle", default="None", type="string",
                      help="Set legend title [default: \"\"]")
    parser.add_option("-y", "--y-title", dest="yTitle", default="None", type="string",
                      help="Set legend title [default: \"\"]")
    parser.add_option("-c", "--customtext", dest="customtext", default="", type="string",
                      help="Set legend title [default: \"\"]")
    parser.add_option("-f", "--filename", dest="filename", default="None", type="string",
                      help="Set legend title [default: \"\"]")
    parser.add_option("-l", "--legendtitle", dest="legendTitle", default="None", type="string",
                      help="Set legend title [default: \"\"]")
    parser.add_option("-g", "--graphtitle", dest="graphTitles", default="None", type="string",
                      help="Set graph title in legend [default: \"\"]")
    parser.add_option("-j", "--jec", dest="jec", default="None", type="string",
                      help="Set JEC name [default: \"\"]")
    parser.add_option("-t", "--text", dest="text", default="", type="string",
                      help="Write text to x,y (NDC) with -t text,x,y [default: \"\"]")
    (opts, args) = parser.parse_args()

    opts.graphTitles = opts.graphTitles.split(',')
    if 'None' in opts.graphTitles:
        opts.graphTitles = opts.graphTitles.remove('None')
    if len(opts.text) > 0:
        opts.text = opts.text.split(',')
        opts.text = [[opts.text[columns+3*rows] for columns in range(3)] for rows in range(int(len(opts.text)/3))]
    
    main(opts, args)
