#!/usr/bin/env python

import datetime
import numpy as np
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", dest="filename", action="store") 
args = parser.parse_args()

ROOT.ROOT.EnableImplicitMT()

def dphi(phi):
    """Calculates delta phi between objects"""
    x = np.abs(phi[1] - phi[0])
    sign = x<=np.pi
    dphi = sign* x + ~sign * (2*np.pi - x)
    return dphi



def main():

    print("root://xrootd-cms.infn.it/"+args.filename)
    #df = ROOT.RDataFrame("Events", "DYJetsToLL_M_50_2022.root")
    #df = ROOT.RDataFrame("Events","root://xrootd-cms.infn.it//store/data/Run2023B/JetMET0/NANOAOD/22Sep2023-v1/2540000/060eed3c-d114-4135-b3f6-2cc6c8cf4c19.root")
    df = ROOT.RDataFrame("Events","root://xrootd-cms.infn.it//store/data/Run2023D/JetMET0/NANOAOD/22Sep2023_v1-v1/2530000/90b4ce31-2fb1-4822-8ca4-aef2c302761d.root")
    #df = ROOT.RDataFrame("Events","root://xrootd-cms.infn.it//store/mc/Run3Winter23NanoAOD/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/NANOAODSIM/126X_mcRun3_2023_forPU65_v1-v1/2540000/a1c3034d-ce5a-4d4c-9ee6-939b6c04edb5.root")
    df = df.Filter("nJet >= 2", "Events with exactly two muons")
    #df = df.Filter("Muon_charge[0] + Muon_charge[1] == 0", "Muons with opposite charge")

    #df_dimuon = df.Define("Dimuon_mass", "InvariantMass(Muon_pt, Muon_eta, Muon_phi, Muon_mass)")
    df = df.Define("Lead_jet", "Jet_pt[0]")
    df = df.Define("Sub_jet", "Jet_pt[1]")
    df = df.Define("Lead_jet_phi", "Jet_phi[0]")
    df = df.Define("Sub_jet_phi", "Jet_phi[1]")
    df = df.Define("Lead_jet_eta", "Jet_eta[0]")
    df = df.Define("Sub_jet_eta", "Jet_eta[1]")
    #print(np.array(df_lead_jet.Take['float']("Lead_jet").GetValue()))
    #print(type(ROOT.vector['float'](np.zeros(10))))
    ROOT.gInterpreter.Declare(
            """
            double dphi(double phi1, double phi2){
                float x  = abs(phi1-phi2);
                if (x>M_PI)return 2*M_PI - x;
                else return x;
            }
            """
            )
    ROOT.gInterpreter.Declare(
            """
            vector<int> match_hlt_offline ( ROOT::VecOps::RVec<float> hlt_eta,ROOT::VecOps::RVec<float> hlt_phi,ROOT::VecOps::RVec<float> off_eta,ROOT::VecOps::RVec<float> off_phi){
                vector<int> hlt_matched;
                int off_index;
                float dr=0.2;
                //for (int i=0; i< off_eta.size();i++){
                for (int i=0; i< off_eta.size();i++){
                    off_index = -1;
                    //std::cout<<off_phi.size()<<" | "<<off_eta.size()<<" | "<<i<<" | "<<hlt_phi.size()<<" | "<<hlt_eta.size()<<std::endl;
                    for (int j=0;j<hlt_eta.size();j++){
                        if (sqrt(pow(hlt_eta[j]-off_eta[i],2)+pow(hlt_phi[j]-off_phi[i],2))<dr){
                            off_index = j;
                            break;
                        }
                    }
                    //std::cout<<off_index<<std::endl;
                    hlt_matched.push_back(off_index);
                }
                return hlt_matched;
            }
            """

            )
    #df_delta_phi = df.Define("Delta_phi","double x = Jet_phi[0]- Jet_phi[1]; return x > TMath::pi ? 2 * TMath::pi - x : x")
    df = df.Define("Delta_phi","dphi(Jet_phi[0],Jet_phi[1])")
    df = df.Define("alpha","nJet==2 ? 0 : 2 * Jet_pt[2]/(Jet_pt[0]+Jet_pt[1])")
    df = df.Define("Trig_obj_pt","TrigObj_pt[TrigObj_id == 1]")
    df = df.Define("hlt_Jet_eta","TrigObj_eta[TrigObj_id == 1]")
    df = df.Define("hlt_Jet_phi","TrigObj_phi[TrigObj_id == 1]")
    df = df.Define("hlt_Jet_id","TrigObj_filterBits[TrigObj_id==1]")
    df = df.Define("Jet_hlt_matched_index","match_hlt_offline(hlt_Jet_eta,hlt_Jet_phi,Jet_eta,Jet_phi)")
    df = df.Define("hlt_Jet_off_matched_pt","Trig_obj_pt[Jet_hlt_matched_index[0]]")
    df = df.Define("hlt_Jet_matched_id","hlt_Jet_id[Jet_hlt_matched_index[0]]")
    df = df.Define("hlt_Jet_matched_eta","hlt_Jet_eta[Jet_hlt_matched_index[0]]")
    df = df.Define("hlt_Jet_matched_phi","hlt_Jet_phi[Jet_hlt_matched_index[0]]")
    #print(df.Take['vector<int>']("Jet_hlt_matched_index").GetValue())
    #df_delta_phi = df.Define("Delta_phi","dphi(Jet_phi)")
    df = df.Filter("Jet_hlt_matched_index[0]!=-1","") 
    #df_after = df.Filter("Delta_phi>2.7","") 
    #df_after = df_after.Filter("alpha < 0.1","") 
    df = df.Filter("HLT_PFJet140","")
    df = df.Filter("L1_SingleJet200 ","")

    df_60 = df.Filter("hlt_Jet_off_matched_pt>60","") 
    df_110 = df.Filter("hlt_Jet_off_matched_pt>110","") 
    df_140 = df.Filter("hlt_Jet_off_matched_pt>140","") 
    df_320 = df.Filter("hlt_Jet_off_matched_pt>320","") 
    df_500 = df.Filter("hlt_Jet_off_matched_pt>500","") 
    df_500_cut = df_500.Filter("Lead_jet<400","") 
    df_500_cut_over = df_500.Filter("Lead_jet>500","") 
    

    histo = df.Histo1D(("h_pt_lead", ";x-axis;y-axis", 100, 0, 1000), "Lead_jet")
    histo_sub = df.Histo1D(("h_pt_sub", ";x-axis;y-axis", 100, 0, 1000), "Sub_jet")
    histo_phi = df.Histo1D(("h_phi_lead", ";x-axis;y-axis", 100, -3.2, 3.2), "Lead_jet_phi")
    histo_sub_phi = df.Histo1D(("h_phi_sub", ";x-axis;y-axis", 100, -3.2, 3.2), "Sub_jet_phi")
    histo_eta = df.Histo1D(("h_eta_lead", ";x-axis;y-axis", 100, -5, 5), "Lead_jet_eta")
    histo_sub_eta = df.Histo1D(("h_eta_sub", ";x-axis;y-axis", 100, -5, 5), "Sub_jet_eta")
    histo_dphi = df.Histo1D(("h_dphi", ";x-axis;y-axis", 100, 0, 3.14), "Delta_phi")
    histo_alpha = df.Histo1D(("h_alpha", ";x-axis;y-axis", 100, 0, 1), "alpha")
    histo_trig = df.Histo1D(("h_trig_pt",";pT;a.u.",100,0,1000),"Trig_obj_pt")
    histo_matched = df.Histo1D(("h_hlt_matched_pt",";pT;a.u.",100,0,1000),"hlt_Jet_off_matched_pt")
    histo_matched_id = df.Histo1D(("h_hlt_matched_id",";pT;a.u.",100,0,100),"hlt_Jet_matched_id")
    histo_matched_eta = df.Histo1D(("h_hlt_matched_eta",";pT;a.u.",100,-5,5),"hlt_Jet_matched_eta")
    histo_matched_phi = df.Histo1D(("h_hlt_matched_phi",";pT;a.u.",100,-3.2,3.2),"hlt_Jet_matched_phi")

    histo_60 = df_60.Histo1D(("h_pt_lead_60", ";x-axis;y-axis", 100, 0, 1000), "Lead_jet")
    histo_sub_60 = df_60.Histo1D(("h_pt_sub_60", ";x-axis;y-axis", 100, 0, 1000), "Sub_jet")
    histo_phi_60 = df_60.Histo1D(("h_phi_lead_60", ";x-axis;y-axis", 100, -3.2, 3.2), "Lead_jet_phi")
    histo_sub_phi_60 = df_60.Histo1D(("h_phi_sub_60", ";x-axis;y-axis", 100, -3.2, 3.2), "Sub_jet_phi")
    histo_eta_60 = df_60.Histo1D(("h_eta_lead_60", ";x-axis;y-axis", 100, -5, 5), "Lead_jet_eta")
    histo_sub_eta_60 = df_60.Histo1D(("h_eta_sub_60", ";x-axis;y-axis", 100, -5, 5), "Sub_jet_eta")
    histo_dphi_60 = df_60.Histo1D(("h_dphi_60", ";x-axis;y-axis", 100, 0, 3.14), "Delta_phi")
    histo_alpha_60 = df_60.Histo1D(("h_alpha_60", ";x-axis;y-axis", 100, 0, 1), "alpha")
    histo_trig_60 = df_60.Histo1D(("h_trig_pt_60",";pT;a.u.",100,0,1000),"Trig_obj_pt")
    histo_matched_60 = df_60.Histo1D(("h_hlt_matched_60",";pT;a.u.",100,0,1000),"hlt_Jet_off_matched_pt")
    histo_matched_id_60 = df_60.Histo1D(("h_hlt_matched_id_60",";pT;a.u.",100,0,100),"hlt_Jet_matched_id")
    histo_matched_eta_60 = df_60.Histo1D(("h_hlt_matched_eta_60",";pT;a.u.",100,-5,5),"hlt_Jet_matched_eta")
    histo_matched_phi_60 = df_60.Histo1D(("h_hlt_matched_phi_60",";pT;a.u.",100,-3.2,3.2),"hlt_Jet_matched_phi")

    

    histo_110 = df_110.Histo1D(("h_pt_lead_110", ";x-axis;y-axis", 100, 0, 1000), "Lead_jet")
    histo_sub_110 = df_110.Histo1D(("h_pt_sub_110", ";x-axis;y-axis", 100, 0, 1000), "Sub_jet")
    histo_phi_110 = df_110.Histo1D(("h_phi_lead_110", ";x-axis;y-axis", 100, -3.2, 3.2), "Lead_jet_phi")
    histo_sub_phi_110 = df_110.Histo1D(("h_phi_sub_110", ";x-axis;y-axis", 100, -3.2, 3.2), "Sub_jet_phi")
    histo_eta_110 = df_110.Histo1D(("h_eta_lead_110", ";x-axis;y-axis", 100, -5, 5), "Lead_jet_eta")
    histo_sub_eta_110 = df_110.Histo1D(("h_eta_sub_110", ";x-axis;y-axis", 100, -5, 5), "Sub_jet_eta")
    histo_dphi_110 = df_110.Histo1D(("h_dphi_110", ";x-axis;y-axis", 100, 0, 3.14), "Delta_phi")
    histo_alpha_110 = df_110.Histo1D(("h_alpha_110", ";x-axis;y-axis", 100, 0, 1), "alpha")
    histo_trig_110 = df_110.Histo1D(("h_trig_pt_110",";pT;a.u.",100,0,1000),"Trig_obj_pt")
    histo_matched_110 = df_110.Histo1D(("h_hlt_matched_110",";pT;a.u.",100,0,1000),"hlt_Jet_off_matched_pt")
    histo_matched_id_110 = df_110.Histo1D(("h_hlt_matched_id_110",";pT;a.u.",100,0,100),"hlt_Jet_matched_id")
    histo_matched_eta_110 = df_110.Histo1D(("h_hlt_matched_eta_110",";pT;a.u.",100,-5,5),"hlt_Jet_matched_eta")
    histo_matched_phi_110 = df_110.Histo1D(("h_hlt_matched_phi_110",";pT;a.u.",100,-3.2,3.2),"hlt_Jet_matched_phi")
    

    histo_140 = df_140.Histo1D(("h_pt_lead_140", ";x-axis;y-axis", 100, 0, 1000), "Lead_jet")
    histo_sub_140 = df_140.Histo1D(("h_pt_sub_140", ";x-axis;y-axis", 100, 0, 1000), "Sub_jet")
    histo_phi_140 = df_140.Histo1D(("h_phi_lead_140", ";x-axis;y-axis", 100, -3.2, 3.2), "Lead_jet_phi")
    histo_sub_phi_140 = df_140.Histo1D(("h_phi_sub_140", ";x-axis;y-axis", 100, -3.2, 3.2), "Sub_jet_phi")
    histo_eta_140 = df_140.Histo1D(("h_eta_lead_140", ";x-axis;y-axis", 100, -5, 5), "Lead_jet_eta")
    histo_sub_eta_140 = df_140.Histo1D(("h_eta_sub_140", ";x-axis;y-axis", 100, -5, 5), "Sub_jet_eta")
    histo_dphi_140 = df_140.Histo1D(("h_dphi_140", ";x-axis;y-axis", 100, 0, 3.14), "Delta_phi")
    histo_alpha_140 = df_140.Histo1D(("h_alpha_140", ";x-axis;y-axis", 100, 0, 1), "alpha")
    histo_trig_140 = df_140.Histo1D(("h_trig_pt_140",";pT;a.u.",100,0,1000),"Trig_obj_pt")
    histo_matched_140 = df_140.Histo1D(("h_hlt_matched_140",";pT;a.u.",100,0,1000),"hlt_Jet_off_matched_pt")
    histo_matched_id_140 = df_140.Histo1D(("h_hlt_matched_id_140",";pT;a.u.",100,0,100),"hlt_Jet_matched_id")
    histo_matched_eta_140 = df_140.Histo1D(("h_hlt_matched_eta_140",";pT;a.u.",100,-5,5),"hlt_Jet_matched_eta")
    histo_matched_phi_140 = df_140.Histo1D(("h_hlt_matched_phi_140",";pT;a.u.",100,-3.2,3.2),"hlt_Jet_matched_phi")
    

    histo_320 = df_320.Histo1D(("h_pt_lead_320", ";x-axis;y-axis", 100, 0, 1000), "Lead_jet")
    histo_sub_320 = df_320.Histo1D(("h_pt_sub_320", ";x-axis;y-axis", 100, 0, 1000), "Sub_jet")
    histo_phi_320 = df_320.Histo1D(("h_phi_lead_320", ";x-axis;y-axis", 100, -3.2, 3.2), "Lead_jet_phi")
    histo_sub_phi_320 = df_320.Histo1D(("h_phi_sub_320", ";x-axis;y-axis", 100, -3.2, 3.2), "Sub_jet_phi")
    histo_eta_320 = df_320.Histo1D(("h_eta_lead_320", ";x-axis;y-axis", 100, -5, 5), "Lead_jet_eta")
    histo_sub_eta_320 = df_320.Histo1D(("h_eta_sub_320", ";x-axis;y-axis", 100, -5, 5), "Sub_jet_eta")
    histo_dphi_320 = df_320.Histo1D(("h_dphi_320", ";x-axis;y-axis", 100, 0, 3.14), "Delta_phi")
    histo_alpha_320 = df_320.Histo1D(("h_alpha_320", ";x-axis;y-axis", 100, 0, 1), "alpha")
    histo_trig_320 = df_320.Histo1D(("h_trig_pt_320",";pT;a.u.",100,0,1000),"Trig_obj_pt")
    histo_matched_320 = df_320.Histo1D(("h_hlt_matched_320",";pT;a.u.",100,0,1000),"hlt_Jet_off_matched_pt")
    histo_matched_id_320 = df_320.Histo1D(("h_hlt_matched_id_320",";pT;a.u.",100,0,100),"hlt_Jet_matched_id")
    histo_matched_eta_320 = df_320.Histo1D(("h_hlt_matched_eta_320",";pT;a.u.",100,-5,5),"hlt_Jet_matched_eta")
    histo_matched_phi_320 = df_320.Histo1D(("h_hlt_matched_phi_320",";pT;a.u.",100,-3.2,3.2),"hlt_Jet_matched_phi")
    

    histo_500 = df_500.Histo1D(("h_pt_lead_500", ";x-axis;y-axis", 100, 0, 1000), "Lead_jet")
    histo_sub_500 = df_500.Histo1D(("h_pt_sub_500", ";x-axis;y-axis", 100, 0, 1000), "Sub_jet")
    histo_phi_500 = df_500.Histo1D(("h_phi_lead_500", ";x-axis;y-axis", 100, -3.2, 3.2), "Lead_jet_phi")
    histo_sub_phi_500 = df_500.Histo1D(("h_phi_sub_500", ";x-axis;y-axis", 100, -3.2, 3.2), "Sub_jet_phi")
    histo_eta_500 = df_500.Histo1D(("h_eta_lead_500", ";x-axis;y-axis", 100, -5, 5), "Lead_jet_eta")
    histo_sub_eta_500 = df_500.Histo1D(("h_eta_sub_500", ";x-axis;y-axis", 100, -5, 5), "Sub_jet_eta")
    histo_dphi_500 = df_500.Histo1D(("h_dphi_500", ";x-axis;y-axis", 100, 0, 3.14), "Delta_phi")
    histo_alpha_500 = df_500.Histo1D(("h_alpha_500", ";x-axis;y-axis", 100, 0, 1), "alpha")
    histo_trig_500 = df_500.Histo1D(("h_trig_pt_500",";pT;a.u.",100,0,1000),"Trig_obj_pt")
    histo_matched_500 = df_500.Histo1D(("h_hlt_matched_500",";pT;a.u.",1000,0,10000),"hlt_Jet_off_matched_pt")
    histo_matched_id_500 = df_500.Histo1D(("h_hlt_matched_id_500",";pT;a.u.",100,0,100),"hlt_Jet_matched_id")
    histo_matched_eta_500 = df_500.Histo1D(("h_hlt_matched_eta_500",";pT;a.u.",100,-5,5),"hlt_Jet_matched_eta")
    histo_matched_phi_500 = df_500.Histo1D(("h_hlt_matched_phi_500",";pT;a.u.",100,-3.2,3.2),"hlt_Jet_matched_phi")
    
    histo_500_cut = df_500_cut.Histo1D(("h_pt_lead_500_cut", ";x-axis;y-axis", 100, 0, 1000), "Lead_jet")
    histo_sub_500_cut = df_500_cut.Histo1D(("h_pt_sub_500_cut", ";x-axis;y-axis", 100, 0, 1000), "Sub_jet")
    histo_phi_500_cut = df_500_cut.Histo1D(("h_phi_lead_500_cut", ";x-axis;y-axis", 100, -3.2, 3.2), "Lead_jet_phi")
    histo_sub_phi_500_cut = df_500_cut.Histo1D(("h_phi_sub_500_cut", ";x-axis;y-axis", 100, -3.2, 3.2), "Sub_jet_phi")
    histo_eta_500_cut = df_500_cut.Histo1D(("h_eta_lead_500_cut", ";x-axis;y-axis", 100, -5, 5), "Lead_jet_eta")
    histo_sub_eta_500_cut = df_500_cut.Histo1D(("h_eta_sub_500_cut", ";x-axis;y-axis", 100, -5, 5), "Sub_jet_eta")
    histo_dphi_500_cut = df_500_cut.Histo1D(("h_dphi_500_cut", ";x-axis;y-axis", 100, 0, 3.14), "Delta_phi")
    histo_alpha_500_cut = df_500_cut.Histo1D(("h_alpha_500_cut", ";x-axis;y-axis", 100, 0, 1), "alpha")
    histo_trig_500_cut = df_500_cut.Histo1D(("h_trig_pt_500_cut",";pT;a.u.",100,0,1000),"Trig_obj_pt")
    histo_matched_500_cut = df_500_cut.Histo1D(("h_hlt_matched_500_cut",";pT;a.u.",1000,0,10000),"hlt_Jet_off_matched_pt")
    histo_matched_id_500_cut = df_500_cut.Histo1D(("h_hlt_matched_id_500_cut",";pT;a.u.",10000,0,10000),"hlt_Jet_matched_id")
    histo_matched_eta_500_cut = df_500_cut.Histo1D(("h_hlt_matched_eta_500_cut",";pT;a.u.",100,-5,5),"hlt_Jet_matched_eta")
    histo_matched_phi_500_cut = df_500_cut.Histo1D(("h_hlt_matched_phi_500_cut",";pT;a.u.",100,-3.2,3.2),"hlt_Jet_matched_phi")

    histo_500_cut_over = df_500_cut_over.Histo1D(("h_pt_lead_500_cut_over", ";x-axis;y-axis", 100, 0, 1000), "Lead_jet")
    histo_sub_500_cut_over = df_500_cut_over.Histo1D(("h_pt_sub_500_cut_over", ";x-axis;y-axis", 100, 0, 1000), "Sub_jet")
    histo_phi_500_cut_over = df_500_cut_over.Histo1D(("h_phi_lead_500_cut_over", ";x-axis;y-axis", 100, -3.2, 3.2), "Lead_jet_phi")
    histo_sub_phi_500_cut_over = df_500_cut_over.Histo1D(("h_phi_sub_500_cut_over", ";x-axis;y-axis", 100, -3.2, 3.2), "Sub_jet_phi")
    histo_eta_500_cut_over = df_500_cut_over.Histo1D(("h_eta_lead_500_cut_over", ";x-axis;y-axis", 100, -5, 5), "Lead_jet_eta")
    histo_sub_eta_500_cut_over = df_500_cut_over.Histo1D(("h_eta_sub_500_cut_over", ";x-axis;y-axis", 100, -5, 5), "Sub_jet_eta")
    histo_dphi_500_cut_over = df_500_cut_over.Histo1D(("h_dphi_500_cut_over", ";x-axis;y-axis", 100, 0, 3.14), "Delta_phi")
    histo_alpha_500_cut_over = df_500_cut_over.Histo1D(("h_alpha_500_cut_over", ";x-axis;y-axis", 100, 0, 1), "alpha")
    histo_trig_500_cut_over = df_500_cut_over.Histo1D(("h_trig_pt_500_cut_over",";pT;a.u.",100,0,1000),"Trig_obj_pt")
    histo_matched_500_cut_over = df_500_cut_over.Histo1D(("h_hlt_matched_500_cut_over",";pT;a.u.",1000,0,10000),"hlt_Jet_off_matched_pt")
    histo_matched_id_500_cut_over = df_500_cut_over.Histo1D(("h_hlt_matched_id_500_cut_over",";pT;a.u.",10000,0,10000),"hlt_Jet_matched_id")
    histo_matched_eta_500_cut_over = df_500_cut_over.Histo1D(("h_hlt_matched_eta_500_cut_over",";pT;a.u.",100,-5,5),"hlt_Jet_matched_eta")
    histo_matched_phi_500_cut_over = df_500_cut_over.Histo1D(("h_hlt_matched_phi_500_cut_over",";pT;a.u.",100,-3.2,3.2),"hlt_Jet_matched_phi")

    fOUT = ROOT.TFile.Open("output_140_select.root","RECREATE")

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    now = datetime.datetime.now()
    m = "produced: %s %s"%(days[now.weekday()],now)
    timestamp = ROOT.TNamed(m,"")
    timestamp.Write()

    histo.Write()
    histo_sub.Write()
    histo_phi.Write()
    histo_sub_phi.Write()
    histo_eta.Write()
    histo_sub_eta.Write()
    histo_dphi.Write()
    histo_alpha.Write()
    histo_trig.Write()
    histo_matched.Write()
    histo_matched_id.Write()
    histo_matched_eta.Write()
    histo_matched_phi.Write()

    histo_60.Write()
    histo_sub_60.Write()
    histo_phi_60.Write()
    histo_sub_phi_60.Write()
    histo_eta_60.Write()
    histo_sub_eta_60.Write()
    histo_dphi_60.Write()
    histo_alpha_60.Write()
    histo_trig_60.Write()
    histo_matched_60.Write()
    histo_matched_id_60.Write()
    histo_matched_eta_60.Write()
    histo_matched_phi_60.Write()

    histo_110.Write()
    histo_sub_110.Write()
    histo_phi_110.Write()
    histo_sub_phi_110.Write()
    histo_eta_110.Write()
    histo_sub_eta_110.Write()
    histo_dphi_110.Write()
    histo_alpha_110.Write()
    histo_trig_110.Write()
    histo_matched_110.Write()
    histo_matched_id_110.Write()
    histo_matched_eta_110.Write()
    histo_matched_phi_110.Write()

    histo_140.Write()
    histo_sub_140.Write()
    histo_phi_140.Write()
    histo_sub_phi_140.Write()
    histo_eta_140.Write()
    histo_sub_eta_140.Write()
    histo_dphi_140.Write()
    histo_alpha_140.Write()
    histo_trig_140.Write()
    histo_matched_140.Write()
    histo_matched_id_140.Write()
    histo_matched_eta_140.Write()
    histo_matched_phi_140.Write()

    histo_320.Write()
    histo_sub_320.Write()
    histo_phi_320.Write()
    histo_sub_phi_320.Write()
    histo_eta_320.Write()
    histo_sub_eta_320.Write()
    histo_dphi_320.Write()
    histo_alpha_320.Write()
    histo_trig_320.Write()
    histo_matched_320.Write()
    histo_matched_id_320.Write()
    histo_matched_eta_320.Write()
    histo_matched_phi_320.Write()

    histo_500.Write()
    histo_sub_500.Write()
    histo_phi_500.Write()
    histo_sub_phi_500.Write()
    histo_eta_500.Write()
    histo_sub_eta_500.Write()
    histo_dphi_500.Write()
    histo_alpha_500.Write()
    histo_trig_500.Write()
    histo_matched_500.Write()
    histo_matched_id_500.Write()
    histo_matched_eta_500.Write()
    histo_matched_phi_500.Write()

    histo_500_cut.Write()
    histo_sub_500_cut.Write()
    histo_phi_500_cut.Write()
    histo_sub_phi_500_cut.Write()
    histo_eta_500_cut.Write()
    histo_sub_eta_500_cut.Write()
    histo_dphi_500_cut.Write()
    histo_alpha_500_cut.Write()
    histo_trig_500_cut.Write()
    histo_matched_500_cut.Write()
    histo_matched_id_500_cut.Write()
    histo_matched_eta_500_cut.Write()
    histo_matched_phi_500_cut.Write()

    histo_500_cut_over.Write()
    histo_sub_500_cut_over.Write()
    histo_phi_500_cut_over.Write()
    histo_sub_phi_500_cut_over.Write()
    histo_eta_500_cut_over.Write()
    histo_sub_eta_500_cut_over.Write()
    histo_dphi_500_cut_over.Write()
    histo_alpha_500_cut_over.Write()
    histo_trig_500_cut_over.Write()
    histo_matched_500_cut_over.Write()
    histo_matched_id_500_cut_over.Write()
    histo_matched_eta_500_cut_over.Write()
    histo_matched_phi_500_cut_over.Write()
    
    
    fOUT.Close()
    

if __name__ == "__main__":
    main()



