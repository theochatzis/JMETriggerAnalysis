//=======================================================================================================|
// This code validates the assignement of particle candidates with jets in the NTuples                   |
// It is done by ckecking:                                                                               |
// * deltaR distribution of candidates with the corresponding jet                                        |
// * 2D distributions of energy in eta-phi plane for some jet in an event                                |
//=======================================================================================================|

#include "TMath.h"
#include "TH1F.h"
#include "TH2F.h"


// main function
void CandidatesJetValidation(){

gROOT->SetBatch(kTRUE); // not show canvases when draw

// --- Define the input file
TFile *inf = TFile::Open("/eos/user/t/tchatzis/MTDtiming_samples/samples/Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200/Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200.root");


// ============================= Input variables ==============================

// -- jet type e.g. offline CHS 
TString jet_type  = "offlineAK4PFCHSJetsCorrected";

// --- Get the tree
TTree* tree = (TTree*) inf -> Get("JMETriggerNTuple/Events");

// --- Get useful tree variables
// - reco jets -
vector<float> *JetEta(0);
vector<float> *JetPhi(0);
vector<uint> *JetNumberOfDaughters(0);

tree -> SetBranchAddress(jet_type+"_numberOfDaughters"       ,&JetNumberOfDaughters);
tree -> SetBranchAddress(jet_type+"_eta"                     ,&JetEta);
tree -> SetBranchAddress(jet_type+"_phi"                     ,&JetPhi);
// - candidates -
vector<float> *CandidateEnergy(0);
vector<float> *CandidatePt(0);
vector<float> *CandidateEta(0);
vector<float> *CandidatePhi(0);
vector<int>   *CandidateBelongsToJet(0);

tree -> SetBranchAddress(jet_type+"_CandidateEnergy"            ,&CandidateEnergy);
tree -> SetBranchAddress(jet_type+"_CandidatePt"                ,&CandidatePt);
tree -> SetBranchAddress(jet_type+"_CandidateEta"               ,&CandidateEta);
tree -> SetBranchAddress(jet_type+"_CandidatePhi"               ,&CandidatePhi);
tree -> SetBranchAddress(jet_type+"_CandidateBelongsToJet"      ,&CandidateBelongsToJet);


// ======================= Assisting variables ================================
int nJets;
float dEta_candidate_jet;
float dPhi_candidate_jet;
float deltaR_candidate_jet;


// for test candidates energy deposition 2D plot
int testEventIndex = 10; 
int testJetIndex = 0;

float testJetEta, testJetPhi;


// =============================  Definitions =================================
// -- histograms definitions
TH1F *hist_deltaR_candidate_jet = new TH1F("hist_deltaR_candidate_jet","hist_deltaR_candidate_jet",100,0.,1.0);
TH2F *hist_candidates_energyDistribution = new TH2F("hist_candidates_energyDistribution","hist_candidates_energyDistribution",100,-5.0,5.0,100,-3.15,3.15);

// ======================= Run over events ====================================
int Nevents = 1000;//tree -> GetEntries();

Float_t PROGRESS_COUNTER = 0.;

for(int iEvent=0;iEvent<Nevents;iEvent++){
  if (iEvent/(Nevents*1.)>PROGRESS_COUNTER){
	  cout << PROGRESS_COUNTER*100. << " %" << endl;
	  PROGRESS_COUNTER += 0.1;
  }

  tree -> GetEntry(iEvent);
  
  nJets = (*JetEta).size();
  
  if(iEvent==testEventIndex ){
    testJetEta = (*JetEta)[testJetIndex];
    testJetPhi = (*JetPhi)[testJetIndex];
  }

  for (unsigned int iCandidate=0;iCandidate<(*CandidateBelongsToJet).size();iCandidate++){
    dEta_candidate_jet = (*CandidateEta)[iCandidate] - (*JetEta)[(*CandidateBelongsToJet)[iCandidate]];
    dPhi_candidate_jet = TVector2::Phi_mpi_pi( (*CandidatePhi)[iCandidate] - (*JetPhi)[(*CandidateBelongsToJet)[iCandidate]] ); 
    deltaR_candidate_jet   = TMath::Sqrt( dEta_candidate_jet*dEta_candidate_jet + dPhi_candidate_jet*dPhi_candidate_jet );
    
    hist_deltaR_candidate_jet -> Fill(deltaR_candidate_jet);

    if(iEvent==testEventIndex && (*CandidateBelongsToJet)[iCandidate]==testJetIndex){
      hist_candidates_energyDistribution -> Fill((*CandidateEta)[iCandidate],(*CandidatePhi)[iCandidate],(*CandidateEnergy)[iCandidate]);
    }

  }// loop over candidates

}// loop over events


// ======================= Make plots and save them ===========================
TFile *output_file = TFile::Open("CandidatesJetValidation_output.root","RECREATE"); 

TCanvas *can_deltaR_candidate_jet = new TCanvas("can_deltaR_candidate_jet","can_deltaR_candidate_jet");
can_deltaR_candidate_jet -> SetLogy(true);
hist_deltaR_candidate_jet -> SetLineWidth(2);
hist_deltaR_candidate_jet -> SetTitle("");
hist_deltaR_candidate_jet -> GetXaxis() -> SetTitle("#DeltaR(jet candidate,jet)");
hist_deltaR_candidate_jet -> Draw("HIST");

can_deltaR_candidate_jet -> Write();

TCanvas *can_candidates_energyDistribution = new TCanvas("can_candidates_energyDistribution","can_candidates_energyDistribution");

string testJetEtaString = std::to_string(testJetEta).substr(0, std::to_string(testJetEta).find(".") + 3);
string testJetPhiString = std::to_string(testJetPhi).substr(0, std::to_string(testJetPhi).find(".") + 3);

hist_candidates_energyDistribution -> SetTitle(("#eta_{jet}="+testJetEtaString+" , #phi_{jet}="+testJetPhiString).c_str());
hist_candidates_energyDistribution -> GetXaxis() -> SetTitle("candidate #eta");
hist_candidates_energyDistribution -> GetXaxis() -> SetTitleOffset(2);
hist_candidates_energyDistribution -> GetYaxis() -> SetTitle("candidate #phi");
hist_candidates_energyDistribution -> GetYaxis() -> SetTitleOffset(2);
hist_candidates_energyDistribution -> GetYaxis() -> SetTitleOffset(2);
hist_candidates_energyDistribution -> GetZaxis() -> SetTitle("jet particles energy [GeV]");
hist_candidates_energyDistribution -> GetZaxis() -> SetTitleOffset(1.2);
hist_candidates_energyDistribution -> Draw("LEGO");

can_candidates_energyDistribution -> Write();

inf -> Close();
output_file -> Close();



}