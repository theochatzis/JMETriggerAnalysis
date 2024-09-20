#!/usr/bin/env python3
#
# Read NanoAOD skim and make histograms in RDataFrame
# Usage:
#       analysis_RDataFrame.py <multicrabdir> [options]
# Example:
#       analysis_RDataFrame.py multicrab_ZbAnalysis_v1405_Run2024BCDE_20240605T1127 -i 2024B,DY
#
# 20.6.2024/S.Lehti
#

import os
import sys
import re
import subprocess
import datetime
import json

from optparse import OptionParser

import ROOT

basepath_re = re.compile("(?P<basepath>\S+/NanoAnalysis)/")
match = basepath_re.search(os.getcwd())
if match:
    sys.path.append(os.path.join(match.group("basepath"),"NanoAODAnalysis/Framework/python"))

import multicrabdatasets


ROOT.ROOT.EnableImplicitMT()

def main(opts, args):

    if len(args) == 0:
        usage()
        sys.exit()

    multicrabdir = os.path.abspath(args[0])
    if not os.path.exists(multicrabdir) or not os.path.isdir(multicrabdir):
        usage()
        sys.exit()
    year = multicrabdatasets.getYear(multicrabdir)

    blacklist = []
    whitelist = []
    if opts.includeTasks != 'None':
        whitelist.extend(opts.includeTasks.split(','))
    if opts.excludeTasks != 'None':
        blacklist.extend(opts.excludeTasks.split(','))

    datasets = multicrabdatasets.getDatasets(multicrabdir,whitelist=whitelist,blacklist=blacklist)
    pileup_data = multicrabdatasets.getDataPileupROOT(datasets)
    lumi = multicrabdatasets.loadLuminosity(multicrabdir,datasets)

    time = datetime.datetime.now().strftime("%Y%m%dT%H%M")
    LEPTONFLAVOR = int(opts.lepton)
    lepton = "_"
    if LEPTONFLAVOR == 11:
        lepton+="Electron"
    if LEPTONFLAVOR == 13:
        lepton+="Muon"


    outputmulticrab = os.path.basename(os.path.abspath(multicrabdir))+"_processed"+time+lepton
    if len(opts.name) > 0:
        outputmulticrab = outputmulticrab + "_"+opts.name
    if not os.path.exists(outputmulticrab):
        os.mkdir(outputmulticrab)

    print("whitelist",whitelist)
    print("blacklist",blacklist)

    print("Number of datasets: %s"%len(datasets))
    for i,dataset in enumerate(datasets):
        print(dataset.name)
        print(dataset.files)
        print(lepton)
        txt = "Dataset %s/%s"%(i+1,len(datasets))
        analysisLoop(year,outputmulticrab,dataset,pileup_data,lumi,txt,lepton)

    print( "Output written in",outputmulticrab )
    print( "Workdir:",os.getcwd() )


def analysisLoop(year,outputmulticrab,dataset,pileup_data,lumi,txt,lepton):
    subdir = os.path.join(outputmulticrab,dataset.name)
    outputdir = os.path.join(subdir,"results")
    if not os.path.exists(subdir):
        os.mkdir(subdir)
        os.mkdir(outputdir)

    # RDataFrame begin
    df = ROOT.RDataFrame("Events", dataset.files)

    counter1 = df.Count()

    df = df.Filter("HLT_IsoMu24 > 0.5", "Events passing trigger")
    counter2 = df.Count()

    histo = df.Histo1D(("h_pileup", ";x-axis;y-axis", 100, 0, 100), "PV_npvs")

    print
    print(txt)
    print(dataset.name)
    print("All events",counter1.GetValue())
    print("trigger   ",counter2.GetValue())

    fOUT = ROOT.TFile.Open(os.path.join(outputdir,"histograms.root"),"RECREATE")

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    now = datetime.datetime.now()
    m = "produced: %s %s"%(days[now.weekday()],now)
    timestamp = ROOT.TNamed(m,"")
    timestamp.Write()

    histo.Write()

    fOUT.Close()

if __name__ == "__main__":
    import time
    t0 = time.time()

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-i", "--includeTasks", dest="includeTasks", default="None", type="string",
                      help="Only perform action for this dataset(s) [default: \"\"]")
    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", default="None", type="string",
                      help="Exclude this dataset(s) from action [default: \"\"]")
    parser.add_option("--name",dest="name", default="", type="string",
                      help="Ending for the multicrabdir [default: \"\"]")
    parser.add_option("-l", "--lepton",dest="lepton", default="13", type="string",
                      help="Electron (11) or Muon (13) [default: \"13\"]")

    (opts, args) = parser.parse_args()

    main(opts, args)

    t1 = time.time()
    dt = t1-t0
    print("Processing time %s s"%(int(dt%60)))
