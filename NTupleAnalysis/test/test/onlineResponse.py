#!/usr/bin/env python
import ROOT
from DataFormats.FWLite import Events, Handle
import math
import array

def deltaPhi(phi1, phi2):
    PHI = abs(phi1-phi2)
    if (PHI<=math.pi):
        return PHI
    else:
        return 2*math.pi-PHI

def deltaR(eta1, phi1, eta2, phi2):
    deta = eta1-eta2
    dphi = deltaPhi(phi1,phi2)
    return math.sqrt(deta*deta + dphi*dphi)

#xbin = [10,15,18,20,22,25,30,35,40,45,50,60,75,100,160]
xbin = [5,10,15,17,18,19,20,25,30,35,40,45,50,55,60,80,100,150,200]
xbins = array.array('d', xbin)

JetCollection = 'slimmedJets'
jetType = 'CHS' # empty or "Corrected" or CHS or CHSCorrected or Puppi for offline

def histograms(files):

    #eta_thresholds = [0]
    #color={0:ROOT.kBlack, 1.3:ROOT.kBlue, 2.5:ROOT.kRed, 3:ROOT.kMagenta}
    eta_thresholds = [-1.3,1.3] # you can put here whatever interval you wish
    resp = {}
    thresholds = [10**(x/10.) for x in range(10,25)]
    jecvspt = ROOT.TProfile("jecvspt", "jecvspt", len(thresholds)-1, array.array('d', thresholds))
    jecvseta = ROOT.TProfile("jecvseta", "jecvseta", 20, -5.,5.,0.1,1.5)
    respvseta = ROOT.TProfile("responsevseta", "responsevseta", 20, -5.,5.,0.1,1.5)
    for eta_th in eta_thresholds:
        resp[eta_th] = ROOT.TProfile("response", "response", len(thresholds)-1, array.array('d', thresholds) )
        resp[eta_th].SetName("response "+str(eta_th))

    for fileName in files:

        events = Events(fileName)
        HLTJetHandle = Handle('std::vector<pat::Jet>')
#        GenJetHandle = Handle('std::vector<reco::GenJet>')
        deltaRMin = ROOT.TH1F("deltaRMin","",100,0.,1.0)

        for event in events:
#          event.getByLabel(("ak4GenJets"), GenJetHandle)        
#          genJets = GenJetHandle.product()
#          event.getByLabel(("slimmedJetsPuppi"), HLTJetHandle)
#          l2Jets = HLTJetHandle.product()
#          for genJet in genJets:
#               if  genJet.pt() < 10: continue
#               deltaR_min = 0.4
#               jetEt = -1000
#               for jet in l2Jets:
#                    deltar = deltaR(genJet.eta(), genJet.phi(), jet.eta(),jet.phi()) 
#                    if deltar < deltaR_min:
#                         deltaR_min = deltar
#                         jetEt = jet.et()
#               deltaRMin.Fill(deltaR_min)
#               if jetEt < -20: continue
#               if abs(genJet.eta()) > eta_thresholds[0] and abs(genJet.eta()) < eta_thresholds[1]:
#                         resp[eta_thresholds[0]].Fill(genJet.et(), jetEt / (genJet.et()))
#               respvseta.Fill(genJet.eta(), jetEt / (genJet.et()) )

          event.getByLabel(JetCollection, HLTJetHandle)
          l2Jets = HLTJetHandle.product()
          deltaR_min = 0.1
          jetPt = -1000
          for jet in l2Jets:
              if abs(jet.eta()) > 1.3: continue
              if jet.pt() < 20: continue
              genJet = jet.genJet()
              if not genJet: continue
              if genJet.pt() < 20: continue
#              if genJet.pt() > 200: continue
              deltar = deltaR(genJet.eta(), genJet.phi(), jet.eta(), jet.phi()) 
              if deltar < deltaR_min:
                 deltaR_min = deltar
                 jetPt = jet.pt()
              if jetPt < -20: continue
              deltaRMin.Fill(deltaR_min)
              if abs(genJet.eta()) > eta_thresholds[0] and abs(genJet.eta()) < eta_thresholds[1]:
#                 print genJet.pt(), jet.pt(), jet.correctedP4(0).pt(), jet.correctedP4(1).pt(), jet.correctedP4(2).pt() #, jet.correctedP4(3).pt()
                 resp[eta_thresholds[0]].Fill(genJet.pt(), jetPt / (genJet.pt()))
              respvseta.Fill(genJet.eta(), jetPt / (genJet.pt()) )
              jecvspt.Fill(genJet.pt(), jet.pt() / jet.correctedP4(0).pt())
              jecvseta.Fill(genJet.eta(), jet.pt() / jet.correctedP4(0).pt())

    c1 = ROOT.TCanvas()
    resp[eta_thresholds[0]].Draw()
    c1.SaveAs("resVSpt_"+str(eta_thresholds[0])+jetType+".pdf")

    c2=ROOT.TCanvas()
    deltaRMin.Draw()
    c2.SaveAs("deltaR_"+jetType+".pdf")
    respvseta.GetYaxis().SetRangeUser(0.1,1.5)

    respvseta.Draw()
    c2.SaveAs("resVsEta_"+jetType+".pdf")

    jecvspt.Draw()
    c2.SaveAs("jecVsPt_"+jetType+".pdf")

    jecvseta.Draw()
    c2.SaveAs("jecVsEta_"+jetType+".pdf")

    mylist = [deltaRMin, respvseta] 
    mylist.append(resp[eta_thresholds[0]])
    return mylist

# just to avoid opening windows
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

#ifile = "root://xrootd-cms.infn.it//store/mc/PhaseIITDRSpring19DR/QCD_Pt-15to3000_EMEnriched_TuneCP5_13TeV_pythia8/AODSIM/PU200_106X_upgrade2023_realistic_v3-v1/50000/7B3A058C-0CE2-1343-8304-D3EADE243D5E.root"
#ifile = "hltoutput_hlt.root"

#ifile = "root://xrootd-cms.infn.it//store/relval/CMSSW_10_6_0/RelValTTbar_14TeV/MINIAODSIM/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/8DEB5DEF-190E-7341-8BF0-242F428D4023.root"
#ifile = "file:RelValTTbar_14TeV_MINIAODSIM.root"

#ifile = "root://xrootd-cms.infn.it//store/mc/PhaseIITDRSpring19MiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/MINIAODSIM/PU200_106X_upgrade2023_realistic_v3-v1/240000/7A20ACE5-523B-8244-BDC4-0DEC2671DB71.root"
#ifile = "file:TT_14TeV_PU200_MINIAODSIM.root"

ifile = "root://xrootd-cms.infn.it//store/mc/PhaseIITDRSpring19MiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/MINIAODSIM/NoPU_106X_upgrade2023_realistic_v3-v2/40000/37220C36-515A-FA4A-AF94-2349FF426578.root"

myhistos = histograms([ifile])
newfile = ROOT.TFile("jets.root","RECREATE")
for idx in range(len(myhistos)): myhistos[idx].Write()
newfile.Close()
