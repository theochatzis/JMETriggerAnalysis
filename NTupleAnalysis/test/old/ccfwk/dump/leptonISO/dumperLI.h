//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Sun Apr 26 18:17:12 2015 by ROOT version 5.27/06
// from TTree Events/Events
// found on file: ../ntupleLI.MC.QCD_MuPt15_py8__phys14_pu20bx25.root
//////////////////////////////////////////////////////////

#ifndef dumperLI_h
#define dumperLI_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>

const Int_t kMaxEVT = 1;
const Int_t kMaxGENP = 4;
const Int_t kMaxHLT = 1;
const Int_t kMaxPVTX = 1;
const Int_t kMaxMUO = 1;
const Int_t kMaxELE = 1;
const Int_t kMaxJET_AK4 = 11;
const Int_t kMaxMET = 1;

#include <string>
#include <vector>

#include <TH2F.h>
#include <TLorentzVector.h>

class dumperLI : public TSelector {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain

   // Declaration of leaf types
   Int_t           EVT_;
   Int_t           EVT_Event[kMaxEVT];   //[EVT_]
   Int_t           EVT_LumiBlock[kMaxEVT];   //[EVT_]
   Int_t           EVT_Run[kMaxEVT];   //[EVT_]
   Int_t           EVT_nPV[kMaxEVT];   //[EVT_]
   Float_t         EVT_MCPileupBX0[kMaxEVT];   //[EVT_]
   Float_t         EVT_pdf_id1[kMaxEVT];   //[EVT_]
   Float_t         EVT_pdf_id2[kMaxEVT];   //[EVT_]
   Float_t         EVT_pdf_x1[kMaxEVT];   //[EVT_]
   Float_t         EVT_pdf_x2[kMaxEVT];   //[EVT_]
   Float_t         EVT_pdf_scalePDF[kMaxEVT];   //[EVT_]
   Float_t         EVT_pdf_xPDF1[kMaxEVT];   //[EVT_]
   Float_t         EVT_pdf_xPDF2[kMaxEVT];   //[EVT_]
   Float_t         EVT_MCWeight[kMaxEVT];   //[EVT_]
   Int_t           GENP_;
   Float_t         GENP_pt[kMaxGENP];   //[GENP_]
   Float_t         GENP_eta[kMaxGENP];   //[GENP_]
   Float_t         GENP_phi[kMaxGENP];   //[GENP_]
   Float_t         GENP_M[kMaxGENP];   //[GENP_]
   Int_t           GENP_pdgID[kMaxGENP];   //[GENP_]
   Int_t           GENP_status[kMaxGENP];   //[GENP_]
   Int_t           GENP_nMothers[kMaxGENP];   //[GENP_]
   Int_t           GENP_nDaughters[kMaxGENP];   //[GENP_]
   Int_t           GENP_index[kMaxGENP];   //[GENP_]
   Int_t           GENP_indexMo1[kMaxGENP];   //[GENP_]
   Int_t           GENP_indexMo2[kMaxGENP];   //[GENP_]
   Int_t           GENP_indexDa1[kMaxGENP];   //[GENP_]
   Int_t           GENP_indexDa2[kMaxGENP];   //[GENP_]
   Int_t           HLT_;
   Bool_t          HLT_Mu45_eta2p1[kMaxHLT];   //[HLT_]
   Bool_t          HLT_IsoMu24_eta2p1_IterTk02[kMaxHLT];   //[HLT_]
   Bool_t          HLT_Mu40_eta2p1_PFJet200_PFJet50[kMaxHLT];   //[HLT_]
   Bool_t          HLT_Ele95_CaloIdVT_GsfTrkIdT[kMaxHLT];   //[HLT_]
   Bool_t          HLT_Ele32_eta2p1_WP75_Gsf[kMaxHLT];   //[HLT_]
   Bool_t          HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50[kMaxHLT];   //[HLT_]
   Bool_t          HLT_AK8PFJet360TrimMod_Mass30[kMaxHLT];   //[HLT_]
   Bool_t          HLT_PFMET170_NoiseCleaned[kMaxHLT];   //[HLT_]
   Bool_t          HLT_PFMET120_NoiseCleaned_BTagCSV07[kMaxHLT];   //[HLT_]
   Bool_t          HLT_PFHT350_PFMET120_NoiseCleaned[kMaxHLT];   //[HLT_]
   Bool_t          HLT_PFHT900[kMaxHLT];   //[HLT_]
   Int_t           PVTX_;
   Bool_t          PVTX_isFake[kMaxPVTX];   //[PVTX_]
   Float_t         PVTX_chi2[kMaxPVTX];   //[PVTX_]
   Float_t         PVTX_nDOF[kMaxPVTX];   //[PVTX_]
   Float_t         PVTX_vx[kMaxPVTX];   //[PVTX_]
   Float_t         PVTX_vy[kMaxPVTX];   //[PVTX_]
   Float_t         PVTX_vz[kMaxPVTX];   //[PVTX_]
   Int_t           MUO_;
   Float_t         MUO_pt[kMaxMUO];   //[MUO_]
   Float_t         MUO_eta[kMaxMUO];   //[MUO_]
   Float_t         MUO_phi[kMaxMUO];   //[MUO_]
   Float_t         MUO_M[kMaxMUO];   //[MUO_]
   Int_t           MUO_pdgID[kMaxMUO];   //[MUO_]
   Int_t           MUO_charge[kMaxMUO];   //[MUO_]
   Float_t         MUO_vx[kMaxMUO];   //[MUO_]
   Float_t         MUO_vy[kMaxMUO];   //[MUO_]
   Float_t         MUO_vz[kMaxMUO];   //[MUO_]
   Float_t         MUO_dxyPV[kMaxMUO];   //[MUO_]
   Float_t         MUO_dzPV[kMaxMUO];   //[MUO_]
   Float_t         MUO_dB[kMaxMUO];   //[MUO_]
   Float_t         MUO_PFIso[kMaxMUO];   //[MUO_]
   Bool_t          MUO_isGlobalMuon[kMaxMUO];   //[MUO_]
   Bool_t          MUO_isPFMuon[kMaxMUO];   //[MUO_]
   Float_t         MUO_normChi2[kMaxMUO];   //[MUO_]
   Int_t           MUO_nValidMuonHits[kMaxMUO];   //[MUO_]
   Int_t           MUO_nMatchedStations[kMaxMUO];   //[MUO_]
   Int_t           MUO_nTrkLayersWithMsrt[kMaxMUO];   //[MUO_]
   Int_t           MUO_nValidPixelHits[kMaxMUO];   //[MUO_]
   Int_t           MUO_IDLoose[kMaxMUO];   //[MUO_]
   Int_t           MUO_IDMedium[kMaxMUO];   //[MUO_]
   Int_t           MUO_IDTight[kMaxMUO];   //[MUO_]
   Int_t           MUO_IDSoft[kMaxMUO];   //[MUO_]
   Int_t           MUO_IDHighPt[kMaxMUO];   //[MUO_]
   Int_t           ELE_;
   Float_t         ELE_pt[kMaxELE];   //[ELE_]
   Float_t         ELE_eta[kMaxELE];   //[ELE_]
   Float_t         ELE_phi[kMaxELE];   //[ELE_]
   Float_t         ELE_M[kMaxELE];   //[ELE_]
   Int_t           ELE_pdgID[kMaxELE];   //[ELE_]
   Int_t           ELE_charge[kMaxELE];   //[ELE_]
   Float_t         ELE_vx[kMaxELE];   //[ELE_]
   Float_t         ELE_vy[kMaxELE];   //[ELE_]
   Float_t         ELE_vz[kMaxELE];   //[ELE_]
   Float_t         ELE_dxyPV[kMaxELE];   //[ELE_]
   Float_t         ELE_dzPV[kMaxELE];   //[ELE_]
   Float_t         ELE_dB[kMaxELE];   //[ELE_]
   Float_t         ELE_PFIso[kMaxELE];   //[ELE_]
   Float_t         ELE_scEt[kMaxELE];   //[ELE_]
   Float_t         ELE_scEta[kMaxELE];   //[ELE_]
   Float_t         ELE_dEtaIn[kMaxELE];   //[ELE_]
   Float_t         ELE_dPhiIn[kMaxELE];   //[ELE_]
   Float_t         ELE_sigmaIEtaIEta[kMaxELE];   //[ELE_]
   Float_t         ELE_HoE[kMaxELE];   //[ELE_]
   Float_t         ELE_ecalEnergy[kMaxELE];   //[ELE_]
   Float_t         ELE_trackPAtVtx[kMaxELE];   //[ELE_]
   Bool_t          ELE_vtxFitConv[kMaxELE];   //[ELE_]
   Int_t           ELE_convMissHits[kMaxELE];   //[ELE_]
   Float_t         ELE_mvaNoTrig[kMaxELE];   //[ELE_]
   Float_t         ELE_mvaTrig[kMaxELE];   //[ELE_]
   Int_t           ELE_IDcutBased[kMaxELE];   //[ELE_]
   Int_t           ELE_IDmvaNoTrig[kMaxELE];   //[ELE_]
   Int_t           ELE_IDmvaTrig[kMaxELE];   //[ELE_]
   Int_t           JET_AK4_;
   Float_t         JET_AK4_pt[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_eta[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_phi[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_M[kMaxJET_AK4];   //[JET_AK4_]
   Bool_t          JET_AK4_isPFJet[kMaxJET_AK4];   //[JET_AK4_]
   Int_t           JET_AK4_partonFlavor[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_jetCharge[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_JEC[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_JECUnc[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_JER[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_JERup[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_JERdn[kMaxJET_AK4];   //[JET_AK4_]
   Int_t           JET_AK4_nDaughters[kMaxJET_AK4];   //[JET_AK4_]
   Int_t           JET_AK4_chaMultiplicity[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_chaHadEneFrac[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_chaEmEneFrac[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_neuHadEneFrac[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_neuEmEneFrac[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_puBeta[kMaxJET_AK4];   //[JET_AK4_]
   Int_t           JET_AK4_puIDmva[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_btagJP[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_btagCSV[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_btagCSVIVF[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_Tau1[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_Tau2[kMaxJET_AK4];   //[JET_AK4_]
   Float_t         JET_AK4_Tau3[kMaxJET_AK4];   //[JET_AK4_]
   Int_t           MET_;
   Float_t         MET_pt[kMaxMET];   //[MET_]
   Float_t         MET_phi[kMaxMET];   //[MET_]
   Float_t         MET_sumEt[kMaxMET];   //[MET_]
   Float_t         MET_mEtSig[kMaxMET];   //[MET_]
   Float_t         MET_signif[kMaxMET];   //[MET_]
   Int_t           lep1_pdgID;
   Float_t         lep1_pt;
   Float_t         lep1_eta;
   Float_t         lep1_scEta;
   Float_t         lep1_R010_CH_stand;
   Float_t         lep1_R010_NH_stand;
   Float_t         lep1_R010_Ph_stand;
   Float_t         lep1_R010_PU_stand;
   Float_t         lep1_R010_NH_pfwgt;
   Float_t         lep1_R010_Ph_pfwgt;
   Float_t         lep1_R020_CH_stand;
   Float_t         lep1_R020_NH_stand;
   Float_t         lep1_R020_Ph_stand;
   Float_t         lep1_R020_PU_stand;
   Float_t         lep1_R020_NH_pfwgt;
   Float_t         lep1_R020_Ph_pfwgt;
   Float_t         lep1_R030_CH_stand;
   Float_t         lep1_R030_NH_stand;
   Float_t         lep1_R030_Ph_stand;
   Float_t         lep1_R030_PU_stand;
   Float_t         lep1_R030_NH_pfwgt;
   Float_t         lep1_R030_Ph_pfwgt;
   Float_t         lep1_MINI_CH_stand;
   Float_t         lep1_MINI_NH_stand;
   Float_t         lep1_MINI_Ph_stand;
   Float_t         lep1_MINI_PU_stand;
   Float_t         lep1_MINI_NH_pfwgt;
   Float_t         lep1_MINI_Ph_pfwgt;

   // List of branches
   TBranch        *b_EVT_;   //!
   TBranch        *b_EVT_Event;   //!
   TBranch        *b_EVT_LumiBlock;   //!
   TBranch        *b_EVT_Run;   //!
   TBranch        *b_EVT_nPV;   //!
   TBranch        *b_EVT_MCPileupBX0;   //!
   TBranch        *b_EVT_pdf_id1;   //!
   TBranch        *b_EVT_pdf_id2;   //!
   TBranch        *b_EVT_pdf_x1;   //!
   TBranch        *b_EVT_pdf_x2;   //!
   TBranch        *b_EVT_pdf_scalePDF;   //!
   TBranch        *b_EVT_pdf_xPDF1;   //!
   TBranch        *b_EVT_pdf_xPDF2;   //!
   TBranch        *b_EVT_MCWeight;   //!
   TBranch        *b_GENP_;   //!
   TBranch        *b_GENP_pt;   //!
   TBranch        *b_GENP_eta;   //!
   TBranch        *b_GENP_phi;   //!
   TBranch        *b_GENP_M;   //!
   TBranch        *b_GENP_pdgID;   //!
   TBranch        *b_GENP_status;   //!
   TBranch        *b_GENP_nMothers;   //!
   TBranch        *b_GENP_nDaughters;   //!
   TBranch        *b_GENP_index;   //!
   TBranch        *b_GENP_indexMo1;   //!
   TBranch        *b_GENP_indexMo2;   //!
   TBranch        *b_GENP_indexDa1;   //!
   TBranch        *b_GENP_indexDa2;   //!
   TBranch        *b_HLT_;   //!
   TBranch        *b_HLT_Mu45_eta2p1;   //!
   TBranch        *b_HLT_IsoMu24_eta2p1_IterTk02;   //!
   TBranch        *b_HLT_Mu40_eta2p1_PFJet200_PFJet50;   //!
   TBranch        *b_HLT_Ele95_CaloIdVT_GsfTrkIdT;   //!
   TBranch        *b_HLT_Ele32_eta2p1_WP75_Gsf;   //!
   TBranch        *b_HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50;   //!
   TBranch        *b_HLT_AK8PFJet360TrimMod_Mass30;   //!
   TBranch        *b_HLT_PFMET170_NoiseCleaned;   //!
   TBranch        *b_HLT_PFMET120_NoiseCleaned_BTagCSV07;   //!
   TBranch        *b_HLT_PFHT350_PFMET120_NoiseCleaned;   //!
   TBranch        *b_HLT_PFHT900;   //!
   TBranch        *b_PVTX_;   //!
   TBranch        *b_PVTX_isFake;   //!
   TBranch        *b_PVTX_chi2;   //!
   TBranch        *b_PVTX_nDOF;   //!
   TBranch        *b_PVTX_vx;   //!
   TBranch        *b_PVTX_vy;   //!
   TBranch        *b_PVTX_vz;   //!
   TBranch        *b_MUO_;   //!
   TBranch        *b_MUO_pt;   //!
   TBranch        *b_MUO_eta;   //!
   TBranch        *b_MUO_phi;   //!
   TBranch        *b_MUO_M;   //!
   TBranch        *b_MUO_pdgID;   //!
   TBranch        *b_MUO_charge;   //!
   TBranch        *b_MUO_vx;   //!
   TBranch        *b_MUO_vy;   //!
   TBranch        *b_MUO_vz;   //!
   TBranch        *b_MUO_dxyPV;   //!
   TBranch        *b_MUO_dzPV;   //!
   TBranch        *b_MUO_dB;   //!
   TBranch        *b_MUO_PFIso;   //!
   TBranch        *b_MUO_isGlobalMuon;   //!
   TBranch        *b_MUO_isPFMuon;   //!
   TBranch        *b_MUO_normChi2;   //!
   TBranch        *b_MUO_nValidMuonHits;   //!
   TBranch        *b_MUO_nMatchedStations;   //!
   TBranch        *b_MUO_nTrkLayersWithMsrt;   //!
   TBranch        *b_MUO_nValidPixelHits;   //!
   TBranch        *b_MUO_IDLoose;   //!
   TBranch        *b_MUO_IDMedium;   //!
   TBranch        *b_MUO_IDTight;   //!
   TBranch        *b_MUO_IDSoft;   //!
   TBranch        *b_MUO_IDHighPt;   //!
   TBranch        *b_ELE_;   //!
   TBranch        *b_ELE_pt;   //!
   TBranch        *b_ELE_eta;   //!
   TBranch        *b_ELE_phi;   //!
   TBranch        *b_ELE_M;   //!
   TBranch        *b_ELE_pdgID;   //!
   TBranch        *b_ELE_charge;   //!
   TBranch        *b_ELE_vx;   //!
   TBranch        *b_ELE_vy;   //!
   TBranch        *b_ELE_vz;   //!
   TBranch        *b_ELE_dxyPV;   //!
   TBranch        *b_ELE_dzPV;   //!
   TBranch        *b_ELE_dB;   //!
   TBranch        *b_ELE_PFIso;   //!
   TBranch        *b_ELE_scEt;   //!
   TBranch        *b_ELE_scEta;   //!
   TBranch        *b_ELE_dEtaIn;   //!
   TBranch        *b_ELE_dPhiIn;   //!
   TBranch        *b_ELE_sigmaIEtaIEta;   //!
   TBranch        *b_ELE_HoE;   //!
   TBranch        *b_ELE_ecalEnergy;   //!
   TBranch        *b_ELE_trackPAtVtx;   //!
   TBranch        *b_ELE_vtxFitConv;   //!
   TBranch        *b_ELE_convMissHits;   //!
   TBranch        *b_ELE_mvaNoTrig;   //!
   TBranch        *b_ELE_mvaTrig;   //!
   TBranch        *b_ELE_IDcutBased;   //!
   TBranch        *b_ELE_IDmvaNoTrig;   //!
   TBranch        *b_ELE_IDmvaTrig;   //!
   TBranch        *b_JET_AK4_;   //!
   TBranch        *b_JET_AK4_pt;   //!
   TBranch        *b_JET_AK4_eta;   //!
   TBranch        *b_JET_AK4_phi;   //!
   TBranch        *b_JET_AK4_M;   //!
   TBranch        *b_JET_AK4_isPFJet;   //!
   TBranch        *b_JET_AK4_partonFlavor;   //!
   TBranch        *b_JET_AK4_jetCharge;   //!
   TBranch        *b_JET_AK4_JEC;   //!
   TBranch        *b_JET_AK4_JECUnc;   //!
   TBranch        *b_JET_AK4_JER;   //!
   TBranch        *b_JET_AK4_JERup;   //!
   TBranch        *b_JET_AK4_JERdn;   //!
   TBranch        *b_JET_AK4_nDaughters;   //!
   TBranch        *b_JET_AK4_chaMultiplicity;   //!
   TBranch        *b_JET_AK4_chaHadEneFrac;   //!
   TBranch        *b_JET_AK4_chaEmEneFrac;   //!
   TBranch        *b_JET_AK4_neuHadEneFrac;   //!
   TBranch        *b_JET_AK4_neuEmEneFrac;   //!
   TBranch        *b_JET_AK4_puBeta;   //!
   TBranch        *b_JET_AK4_puIDmva;   //!
   TBranch        *b_JET_AK4_btagJP;   //!
   TBranch        *b_JET_AK4_btagCSV;   //!
   TBranch        *b_JET_AK4_btagCSVIVF;   //!
   TBranch        *b_JET_AK4_Tau1;   //!
   TBranch        *b_JET_AK4_Tau2;   //!
   TBranch        *b_JET_AK4_Tau3;   //!
   TBranch        *b_MET_;   //!
   TBranch        *b_MET_pt;   //!
   TBranch        *b_MET_phi;   //!
   TBranch        *b_MET_sumEt;   //!
   TBranch        *b_MET_mEtSig;   //!
   TBranch        *b_MET_signif;   //!
   TBranch        *b_lep1_pdgID;   //!
   TBranch        *b_lep1_pt;   //!
   TBranch        *b_lep1_eta;   //!
   TBranch        *b_lep1_scEta;   //!
   TBranch        *b_lep1_R010_CH_stand;   //!
   TBranch        *b_lep1_R010_NH_stand;   //!
   TBranch        *b_lep1_R010_Ph_stand;   //!
   TBranch        *b_lep1_R010_PU_stand;   //!
   TBranch        *b_lep1_R010_NH_pfwgt;   //!
   TBranch        *b_lep1_R010_Ph_pfwgt;   //!
   TBranch        *b_lep1_R020_CH_stand;   //!
   TBranch        *b_lep1_R020_NH_stand;   //!
   TBranch        *b_lep1_R020_Ph_stand;   //!
   TBranch        *b_lep1_R020_PU_stand;   //!
   TBranch        *b_lep1_R020_NH_pfwgt;   //!
   TBranch        *b_lep1_R020_Ph_pfwgt;   //!
   TBranch        *b_lep1_R030_CH_stand;   //!
   TBranch        *b_lep1_R030_NH_stand;   //!
   TBranch        *b_lep1_R030_Ph_stand;   //!
   TBranch        *b_lep1_R030_PU_stand;   //!
   TBranch        *b_lep1_R030_NH_pfwgt;   //!
   TBranch        *b_lep1_R030_Ph_pfwgt;   //!
   TBranch        *b_lep1_MINI_CH_stand;   //!
   TBranch        *b_lep1_MINI_NH_stand;   //!
   TBranch        *b_lep1_MINI_Ph_stand;   //!
   TBranch        *b_lep1_MINI_PU_stand;   //!
   TBranch        *b_lep1_MINI_NH_pfwgt;   //!
   TBranch        *b_lep1_MINI_Ph_pfwgt;   //!

   dumperLI(TTree * /*tree*/ =0) { }
   virtual ~dumperLI() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();

   // user-defined
   std::string channel_;
   void set_channel(const std::string& lepton){ channel_ = lepton; }

   std::string output_file_;
   void set_output(const std::string& ofile){ output_file_ = ofile; }

   float dRmin(const TLorentzVector&, const std::vector<TLorentzVector>&);
   float pTrel(const TLorentzVector&, const std::vector<TLorentzVector>&);

   void addTH1F(TH1F**, const std::string&, const int, const float, const float);
   void addTH2F(TH2F**, const std::string&, const int, const float, const float, const int, const float, const float);

   TH1F* h_lep1_pt;
   TH1F* h_lep1_eta;
   TH1F* h_nPV;
   TH1F* h_MET;
   TH1F* h_HTlep;

   TH2F* h_lep1_pt__vs__lep1_pTrel_dR010;
   TH2F* h_lep1_eta__vs__lep1_pTrel_dR010;
   TH2F* h_lep1_nPV__vs__lep1_pTrel_dR010;
   TH2F* h_lep1_pt__vs__lep1_pTrel_dR020;
   TH2F* h_lep1_eta__vs__lep1_pTrel_dR020;
   TH2F* h_lep1_nPV__vs__lep1_pTrel_dR020;
   TH2F* h_lep1_pt__vs__lep1_pTrel_dR030;
   TH2F* h_lep1_eta__vs__lep1_pTrel_dR030;
   TH2F* h_lep1_nPV__vs__lep1_pTrel_dR030;
   TH2F* h_lep1_pt__vs__lep1_pTrel_dR040;
   TH2F* h_lep1_eta__vs__lep1_pTrel_dR040;
   TH2F* h_lep1_nPV__vs__lep1_pTrel_dR040;

   TH2F* h_lep1_pt__vs__lep1_R010iso_dbeta;
   TH2F* h_lep1_eta__vs__lep1_R010iso_dbeta;
   TH2F* h_lep1_nPV__vs__lep1_R010iso_dbeta;
   TH2F* h_lep1_pt__vs__lep1_R020iso_dbeta;
   TH2F* h_lep1_eta__vs__lep1_R020iso_dbeta;
   TH2F* h_lep1_nPV__vs__lep1_R020iso_dbeta;
   TH2F* h_lep1_pt__vs__lep1_R030iso_dbeta;
   TH2F* h_lep1_eta__vs__lep1_R030iso_dbeta;
   TH2F* h_lep1_nPV__vs__lep1_R030iso_dbeta;
   TH2F* h_lep1_pt__vs__lep1_MINIiso_dbeta;
   TH2F* h_lep1_eta__vs__lep1_MINIiso_dbeta;
   TH2F* h_lep1_nPV__vs__lep1_MINIiso_dbeta;

   TH2F* h_lep1_pt__vs__lep1_R010iso_pfwgt;
   TH2F* h_lep1_eta__vs__lep1_R010iso_pfwgt;
   TH2F* h_lep1_nPV__vs__lep1_R010iso_pfwgt;
   TH2F* h_lep1_pt__vs__lep1_R020iso_pfwgt;
   TH2F* h_lep1_eta__vs__lep1_R020iso_pfwgt;
   TH2F* h_lep1_nPV__vs__lep1_R020iso_pfwgt;
   TH2F* h_lep1_pt__vs__lep1_R030iso_pfwgt;
   TH2F* h_lep1_eta__vs__lep1_R030iso_pfwgt;
   TH2F* h_lep1_nPV__vs__lep1_R030iso_pfwgt;
   TH2F* h_lep1_pt__vs__lep1_MINIiso_pfwgt;
   TH2F* h_lep1_eta__vs__lep1_MINIiso_pfwgt;
   TH2F* h_lep1_nPV__vs__lep1_MINIiso_pfwgt;

   ClassDef(dumperLI,0);
};

#endif

#ifdef dumperLI_cxx
void dumperLI::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("EVT", &EVT_, &b_EVT_);
   fChain->SetBranchAddress("EVT.Event", EVT_Event, &b_EVT_Event);
   fChain->SetBranchAddress("EVT.LumiBlock", EVT_LumiBlock, &b_EVT_LumiBlock);
   fChain->SetBranchAddress("EVT.Run", EVT_Run, &b_EVT_Run);
   fChain->SetBranchAddress("EVT.nPV", EVT_nPV, &b_EVT_nPV);
   fChain->SetBranchAddress("EVT.MCPileupBX0", EVT_MCPileupBX0, &b_EVT_MCPileupBX0);
   fChain->SetBranchAddress("EVT.pdf_id1", EVT_pdf_id1, &b_EVT_pdf_id1);
   fChain->SetBranchAddress("EVT.pdf_id2", EVT_pdf_id2, &b_EVT_pdf_id2);
   fChain->SetBranchAddress("EVT.pdf_x1", EVT_pdf_x1, &b_EVT_pdf_x1);
   fChain->SetBranchAddress("EVT.pdf_x2", EVT_pdf_x2, &b_EVT_pdf_x2);
   fChain->SetBranchAddress("EVT.pdf_scalePDF", EVT_pdf_scalePDF, &b_EVT_pdf_scalePDF);
   fChain->SetBranchAddress("EVT.pdf_xPDF1", EVT_pdf_xPDF1, &b_EVT_pdf_xPDF1);
   fChain->SetBranchAddress("EVT.pdf_xPDF2", EVT_pdf_xPDF2, &b_EVT_pdf_xPDF2);
   fChain->SetBranchAddress("EVT.MCWeight", EVT_MCWeight, &b_EVT_MCWeight);
   fChain->SetBranchAddress("GENP", &GENP_, &b_GENP_);
   fChain->SetBranchAddress("GENP.pt", GENP_pt, &b_GENP_pt);
   fChain->SetBranchAddress("GENP.eta", GENP_eta, &b_GENP_eta);
   fChain->SetBranchAddress("GENP.phi", GENP_phi, &b_GENP_phi);
   fChain->SetBranchAddress("GENP.M", GENP_M, &b_GENP_M);
   fChain->SetBranchAddress("GENP.pdgID", GENP_pdgID, &b_GENP_pdgID);
   fChain->SetBranchAddress("GENP.status", GENP_status, &b_GENP_status);
   fChain->SetBranchAddress("GENP.nMothers", GENP_nMothers, &b_GENP_nMothers);
   fChain->SetBranchAddress("GENP.nDaughters", GENP_nDaughters, &b_GENP_nDaughters);
   fChain->SetBranchAddress("GENP.index", GENP_index, &b_GENP_index);
   fChain->SetBranchAddress("GENP.indexMo1", GENP_indexMo1, &b_GENP_indexMo1);
   fChain->SetBranchAddress("GENP.indexMo2", GENP_indexMo2, &b_GENP_indexMo2);
   fChain->SetBranchAddress("GENP.indexDa1", GENP_indexDa1, &b_GENP_indexDa1);
   fChain->SetBranchAddress("GENP.indexDa2", GENP_indexDa2, &b_GENP_indexDa2);
   fChain->SetBranchAddress("HLT", &HLT_, &b_HLT_);
   fChain->SetBranchAddress("HLT.Mu45_eta2p1", HLT_Mu45_eta2p1, &b_HLT_Mu45_eta2p1);
   fChain->SetBranchAddress("HLT.IsoMu24_eta2p1_IterTk02", HLT_IsoMu24_eta2p1_IterTk02, &b_HLT_IsoMu24_eta2p1_IterTk02);
   fChain->SetBranchAddress("HLT.Mu40_eta2p1_PFJet200_PFJet50", HLT_Mu40_eta2p1_PFJet200_PFJet50, &b_HLT_Mu40_eta2p1_PFJet200_PFJet50);
   fChain->SetBranchAddress("HLT.Ele95_CaloIdVT_GsfTrkIdT", HLT_Ele95_CaloIdVT_GsfTrkIdT, &b_HLT_Ele95_CaloIdVT_GsfTrkIdT);
   fChain->SetBranchAddress("HLT.Ele32_eta2p1_WP75_Gsf", HLT_Ele32_eta2p1_WP75_Gsf, &b_HLT_Ele32_eta2p1_WP75_Gsf);
   fChain->SetBranchAddress("HLT.Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50", HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50, &b_HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50);
   fChain->SetBranchAddress("HLT.AK8PFJet360TrimMod_Mass30", HLT_AK8PFJet360TrimMod_Mass30, &b_HLT_AK8PFJet360TrimMod_Mass30);
   fChain->SetBranchAddress("HLT.PFMET170_NoiseCleaned", HLT_PFMET170_NoiseCleaned, &b_HLT_PFMET170_NoiseCleaned);
   fChain->SetBranchAddress("HLT.PFMET120_NoiseCleaned_BTagCSV07", HLT_PFMET120_NoiseCleaned_BTagCSV07, &b_HLT_PFMET120_NoiseCleaned_BTagCSV07);
   fChain->SetBranchAddress("HLT.PFHT350_PFMET120_NoiseCleaned", HLT_PFHT350_PFMET120_NoiseCleaned, &b_HLT_PFHT350_PFMET120_NoiseCleaned);
   fChain->SetBranchAddress("HLT.PFHT900", HLT_PFHT900, &b_HLT_PFHT900);
   fChain->SetBranchAddress("PVTX", &PVTX_, &b_PVTX_);
   fChain->SetBranchAddress("PVTX.isFake", PVTX_isFake, &b_PVTX_isFake);
   fChain->SetBranchAddress("PVTX.chi2", PVTX_chi2, &b_PVTX_chi2);
   fChain->SetBranchAddress("PVTX.nDOF", PVTX_nDOF, &b_PVTX_nDOF);
   fChain->SetBranchAddress("PVTX.vx", PVTX_vx, &b_PVTX_vx);
   fChain->SetBranchAddress("PVTX.vy", PVTX_vy, &b_PVTX_vy);
   fChain->SetBranchAddress("PVTX.vz", PVTX_vz, &b_PVTX_vz);
   fChain->SetBranchAddress("MUO", &MUO_, &b_MUO_);
   fChain->SetBranchAddress("MUO.pt", MUO_pt, &b_MUO_pt);
   fChain->SetBranchAddress("MUO.eta", MUO_eta, &b_MUO_eta);
   fChain->SetBranchAddress("MUO.phi", MUO_phi, &b_MUO_phi);
   fChain->SetBranchAddress("MUO.M", MUO_M, &b_MUO_M);
   fChain->SetBranchAddress("MUO.pdgID", MUO_pdgID, &b_MUO_pdgID);
   fChain->SetBranchAddress("MUO.charge", MUO_charge, &b_MUO_charge);
   fChain->SetBranchAddress("MUO.vx", MUO_vx, &b_MUO_vx);
   fChain->SetBranchAddress("MUO.vy", MUO_vy, &b_MUO_vy);
   fChain->SetBranchAddress("MUO.vz", MUO_vz, &b_MUO_vz);
   fChain->SetBranchAddress("MUO.dxyPV", MUO_dxyPV, &b_MUO_dxyPV);
   fChain->SetBranchAddress("MUO.dzPV", MUO_dzPV, &b_MUO_dzPV);
   fChain->SetBranchAddress("MUO.dB", MUO_dB, &b_MUO_dB);
   fChain->SetBranchAddress("MUO.PFIso", MUO_PFIso, &b_MUO_PFIso);
   fChain->SetBranchAddress("MUO.isGlobalMuon", MUO_isGlobalMuon, &b_MUO_isGlobalMuon);
   fChain->SetBranchAddress("MUO.isPFMuon", MUO_isPFMuon, &b_MUO_isPFMuon);
   fChain->SetBranchAddress("MUO.normChi2", MUO_normChi2, &b_MUO_normChi2);
   fChain->SetBranchAddress("MUO.nValidMuonHits", MUO_nValidMuonHits, &b_MUO_nValidMuonHits);
   fChain->SetBranchAddress("MUO.nMatchedStations", MUO_nMatchedStations, &b_MUO_nMatchedStations);
   fChain->SetBranchAddress("MUO.nTrkLayersWithMsrt", MUO_nTrkLayersWithMsrt, &b_MUO_nTrkLayersWithMsrt);
   fChain->SetBranchAddress("MUO.nValidPixelHits", MUO_nValidPixelHits, &b_MUO_nValidPixelHits);
   fChain->SetBranchAddress("MUO.IDLoose", MUO_IDLoose, &b_MUO_IDLoose);
   fChain->SetBranchAddress("MUO.IDMedium", MUO_IDMedium, &b_MUO_IDMedium);
   fChain->SetBranchAddress("MUO.IDTight", MUO_IDTight, &b_MUO_IDTight);
   fChain->SetBranchAddress("MUO.IDSoft", MUO_IDSoft, &b_MUO_IDSoft);
   fChain->SetBranchAddress("MUO.IDHighPt", MUO_IDHighPt, &b_MUO_IDHighPt);
   fChain->SetBranchAddress("ELE", &ELE_, &b_ELE_);
   fChain->SetBranchAddress("ELE.pt", ELE_pt, &b_ELE_pt);
   fChain->SetBranchAddress("ELE.eta", ELE_eta, &b_ELE_eta);
   fChain->SetBranchAddress("ELE.phi", ELE_phi, &b_ELE_phi);
   fChain->SetBranchAddress("ELE.M", ELE_M, &b_ELE_M);
   fChain->SetBranchAddress("ELE.pdgID", ELE_pdgID, &b_ELE_pdgID);
   fChain->SetBranchAddress("ELE.charge", ELE_charge, &b_ELE_charge);
   fChain->SetBranchAddress("ELE.vx", ELE_vx, &b_ELE_vx);
   fChain->SetBranchAddress("ELE.vy", ELE_vy, &b_ELE_vy);
   fChain->SetBranchAddress("ELE.vz", ELE_vz, &b_ELE_vz);
   fChain->SetBranchAddress("ELE.dxyPV", ELE_dxyPV, &b_ELE_dxyPV);
   fChain->SetBranchAddress("ELE.dzPV", ELE_dzPV, &b_ELE_dzPV);
   fChain->SetBranchAddress("ELE.dB", ELE_dB, &b_ELE_dB);
   fChain->SetBranchAddress("ELE.PFIso", ELE_PFIso, &b_ELE_PFIso);
   fChain->SetBranchAddress("ELE.scEt", ELE_scEt, &b_ELE_scEt);
   fChain->SetBranchAddress("ELE.scEta", ELE_scEta, &b_ELE_scEta);
   fChain->SetBranchAddress("ELE.dEtaIn", ELE_dEtaIn, &b_ELE_dEtaIn);
   fChain->SetBranchAddress("ELE.dPhiIn", ELE_dPhiIn, &b_ELE_dPhiIn);
   fChain->SetBranchAddress("ELE.sigmaIEtaIEta", ELE_sigmaIEtaIEta, &b_ELE_sigmaIEtaIEta);
   fChain->SetBranchAddress("ELE.HoE", ELE_HoE, &b_ELE_HoE);
   fChain->SetBranchAddress("ELE.ecalEnergy", ELE_ecalEnergy, &b_ELE_ecalEnergy);
   fChain->SetBranchAddress("ELE.trackPAtVtx", ELE_trackPAtVtx, &b_ELE_trackPAtVtx);
   fChain->SetBranchAddress("ELE.vtxFitConv", ELE_vtxFitConv, &b_ELE_vtxFitConv);
   fChain->SetBranchAddress("ELE.convMissHits", ELE_convMissHits, &b_ELE_convMissHits);
   fChain->SetBranchAddress("ELE.mvaNoTrig", ELE_mvaNoTrig, &b_ELE_mvaNoTrig);
   fChain->SetBranchAddress("ELE.mvaTrig", ELE_mvaTrig, &b_ELE_mvaTrig);
   fChain->SetBranchAddress("ELE.IDcutBased", ELE_IDcutBased, &b_ELE_IDcutBased);
   fChain->SetBranchAddress("ELE.IDmvaNoTrig", ELE_IDmvaNoTrig, &b_ELE_IDmvaNoTrig);
   fChain->SetBranchAddress("ELE.IDmvaTrig", ELE_IDmvaTrig, &b_ELE_IDmvaTrig);
   fChain->SetBranchAddress("JET_AK4", &JET_AK4_, &b_JET_AK4_);
   fChain->SetBranchAddress("JET_AK4.pt", JET_AK4_pt, &b_JET_AK4_pt);
   fChain->SetBranchAddress("JET_AK4.eta", JET_AK4_eta, &b_JET_AK4_eta);
   fChain->SetBranchAddress("JET_AK4.phi", JET_AK4_phi, &b_JET_AK4_phi);
   fChain->SetBranchAddress("JET_AK4.M", JET_AK4_M, &b_JET_AK4_M);
   fChain->SetBranchAddress("JET_AK4.isPFJet", JET_AK4_isPFJet, &b_JET_AK4_isPFJet);
   fChain->SetBranchAddress("JET_AK4.partonFlavor", JET_AK4_partonFlavor, &b_JET_AK4_partonFlavor);
   fChain->SetBranchAddress("JET_AK4.jetCharge", JET_AK4_jetCharge, &b_JET_AK4_jetCharge);
   fChain->SetBranchAddress("JET_AK4.JEC", JET_AK4_JEC, &b_JET_AK4_JEC);
   fChain->SetBranchAddress("JET_AK4.JECUnc", JET_AK4_JECUnc, &b_JET_AK4_JECUnc);
   fChain->SetBranchAddress("JET_AK4.JER", JET_AK4_JER, &b_JET_AK4_JER);
   fChain->SetBranchAddress("JET_AK4.JERup", JET_AK4_JERup, &b_JET_AK4_JERup);
   fChain->SetBranchAddress("JET_AK4.JERdn", JET_AK4_JERdn, &b_JET_AK4_JERdn);
   fChain->SetBranchAddress("JET_AK4.nDaughters", JET_AK4_nDaughters, &b_JET_AK4_nDaughters);
   fChain->SetBranchAddress("JET_AK4.chaMultiplicity", JET_AK4_chaMultiplicity, &b_JET_AK4_chaMultiplicity);
   fChain->SetBranchAddress("JET_AK4.chaHadEneFrac", JET_AK4_chaHadEneFrac, &b_JET_AK4_chaHadEneFrac);
   fChain->SetBranchAddress("JET_AK4.chaEmEneFrac", JET_AK4_chaEmEneFrac, &b_JET_AK4_chaEmEneFrac);
   fChain->SetBranchAddress("JET_AK4.neuHadEneFrac", JET_AK4_neuHadEneFrac, &b_JET_AK4_neuHadEneFrac);
   fChain->SetBranchAddress("JET_AK4.neuEmEneFrac", JET_AK4_neuEmEneFrac, &b_JET_AK4_neuEmEneFrac);
   fChain->SetBranchAddress("JET_AK4.puBeta", JET_AK4_puBeta, &b_JET_AK4_puBeta);
   fChain->SetBranchAddress("JET_AK4.puIDmva", JET_AK4_puIDmva, &b_JET_AK4_puIDmva);
   fChain->SetBranchAddress("JET_AK4.btagJP", JET_AK4_btagJP, &b_JET_AK4_btagJP);
   fChain->SetBranchAddress("JET_AK4.btagCSV", JET_AK4_btagCSV, &b_JET_AK4_btagCSV);
   fChain->SetBranchAddress("JET_AK4.btagCSVIVF", JET_AK4_btagCSVIVF, &b_JET_AK4_btagCSVIVF);
   fChain->SetBranchAddress("JET_AK4.Tau1", JET_AK4_Tau1, &b_JET_AK4_Tau1);
   fChain->SetBranchAddress("JET_AK4.Tau2", JET_AK4_Tau2, &b_JET_AK4_Tau2);
   fChain->SetBranchAddress("JET_AK4.Tau3", JET_AK4_Tau3, &b_JET_AK4_Tau3);
   fChain->SetBranchAddress("MET", &MET_, &b_MET_);
   fChain->SetBranchAddress("MET.pt", MET_pt, &b_MET_pt);
   fChain->SetBranchAddress("MET.phi", MET_phi, &b_MET_phi);
   fChain->SetBranchAddress("MET.sumEt", MET_sumEt, &b_MET_sumEt);
   fChain->SetBranchAddress("MET.mEtSig", MET_mEtSig, &b_MET_mEtSig);
   fChain->SetBranchAddress("MET.signif", MET_signif, &b_MET_signif);
   fChain->SetBranchAddress("lep1_pdgID", &lep1_pdgID, &b_lep1_pdgID);
   fChain->SetBranchAddress("lep1_pt", &lep1_pt, &b_lep1_pt);
   fChain->SetBranchAddress("lep1_eta", &lep1_eta, &b_lep1_eta);
   fChain->SetBranchAddress("lep1_scEta", &lep1_scEta, &b_lep1_scEta);
   fChain->SetBranchAddress("lep1_R010_CH_stand", &lep1_R010_CH_stand, &b_lep1_R010_CH_stand);
   fChain->SetBranchAddress("lep1_R010_NH_stand", &lep1_R010_NH_stand, &b_lep1_R010_NH_stand);
   fChain->SetBranchAddress("lep1_R010_Ph_stand", &lep1_R010_Ph_stand, &b_lep1_R010_Ph_stand);
   fChain->SetBranchAddress("lep1_R010_PU_stand", &lep1_R010_PU_stand, &b_lep1_R010_PU_stand);
   fChain->SetBranchAddress("lep1_R010_NH_pfwgt", &lep1_R010_NH_pfwgt, &b_lep1_R010_NH_pfwgt);
   fChain->SetBranchAddress("lep1_R010_Ph_pfwgt", &lep1_R010_Ph_pfwgt, &b_lep1_R010_Ph_pfwgt);
   fChain->SetBranchAddress("lep1_R020_CH_stand", &lep1_R020_CH_stand, &b_lep1_R020_CH_stand);
   fChain->SetBranchAddress("lep1_R020_NH_stand", &lep1_R020_NH_stand, &b_lep1_R020_NH_stand);
   fChain->SetBranchAddress("lep1_R020_Ph_stand", &lep1_R020_Ph_stand, &b_lep1_R020_Ph_stand);
   fChain->SetBranchAddress("lep1_R020_PU_stand", &lep1_R020_PU_stand, &b_lep1_R020_PU_stand);
   fChain->SetBranchAddress("lep1_R020_NH_pfwgt", &lep1_R020_NH_pfwgt, &b_lep1_R020_NH_pfwgt);
   fChain->SetBranchAddress("lep1_R020_Ph_pfwgt", &lep1_R020_Ph_pfwgt, &b_lep1_R020_Ph_pfwgt);
   fChain->SetBranchAddress("lep1_R030_CH_stand", &lep1_R030_CH_stand, &b_lep1_R030_CH_stand);
   fChain->SetBranchAddress("lep1_R030_NH_stand", &lep1_R030_NH_stand, &b_lep1_R030_NH_stand);
   fChain->SetBranchAddress("lep1_R030_Ph_stand", &lep1_R030_Ph_stand, &b_lep1_R030_Ph_stand);
   fChain->SetBranchAddress("lep1_R030_PU_stand", &lep1_R030_PU_stand, &b_lep1_R030_PU_stand);
   fChain->SetBranchAddress("lep1_R030_NH_pfwgt", &lep1_R030_NH_pfwgt, &b_lep1_R030_NH_pfwgt);
   fChain->SetBranchAddress("lep1_R030_Ph_pfwgt", &lep1_R030_Ph_pfwgt, &b_lep1_R030_Ph_pfwgt);
   fChain->SetBranchAddress("lep1_MINI_CH_stand", &lep1_MINI_CH_stand, &b_lep1_MINI_CH_stand);
   fChain->SetBranchAddress("lep1_MINI_NH_stand", &lep1_MINI_NH_stand, &b_lep1_MINI_NH_stand);
   fChain->SetBranchAddress("lep1_MINI_Ph_stand", &lep1_MINI_Ph_stand, &b_lep1_MINI_Ph_stand);
   fChain->SetBranchAddress("lep1_MINI_PU_stand", &lep1_MINI_PU_stand, &b_lep1_MINI_PU_stand);
   fChain->SetBranchAddress("lep1_MINI_NH_pfwgt", &lep1_MINI_NH_pfwgt, &b_lep1_MINI_NH_pfwgt);
   fChain->SetBranchAddress("lep1_MINI_Ph_pfwgt", &lep1_MINI_Ph_pfwgt, &b_lep1_MINI_Ph_pfwgt);
}

Bool_t dumperLI::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

#endif // #ifdef dumperLI_cxx
