/*
Code that calculates the dR distances between all reco and gen jets
to validate the cuts used for the matching with true and PU jets 
*/

void deltaRValidation(){

gROOT->SetBatch(kTRUE); // not show canvases when draw

// --- Define the input file
TFile *inf = TFile::Open("/eos/user/t/tchatzis/MTDtiming_samples/samples/Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200/Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200.root");


// ============================= Input variables ==============================

// -- jet type e.g. offline CHS 
TString jet_type_CHS  = "offlineAK4PFCHSJetsCorrected";
TString jet_type_PUPPI  = "offlineAK4PFPuppiJetsCorrected";


// --- Get the tree
TTree* tree = (TTree*) inf -> Get("JMETriggerNTuple/Events");

// --- Get useful tree variables
// - generated jets -
vector<float> *genJetPt(0);
vector<float> *genJetEta(0);
vector<float> *genJetPhi(0);

tree -> SetBranchAddress("ak4GenJets_pt"    ,&genJetPt);
tree -> SetBranchAddress("ak4GenJets_eta"   ,&genJetEta);
tree -> SetBranchAddress("ak4GenJets_phi"   ,&genJetPhi);

// - reco jets -
vector<float> *JetPt_CHS(0);
vector<float> *JetEta_CHS(0);
vector<float> *JetPhi_CHS(0);

tree -> SetBranchAddress(jet_type_CHS+"_pt"                      ,&JetPt_CHS);
tree -> SetBranchAddress(jet_type_CHS+"_eta"                     ,&JetEta_CHS);
tree -> SetBranchAddress(jet_type_CHS+"_phi"                     ,&JetPhi_CHS);


vector<float> *JetPt_PUPPI(0);
vector<float> *JetEta_PUPPI(0);
vector<float> *JetPhi_PUPPI(0);

tree -> SetBranchAddress(jet_type_PUPPI+"_pt"                      ,&JetPt_PUPPI);
tree -> SetBranchAddress(jet_type_PUPPI+"_eta"                     ,&JetEta_PUPPI);
tree -> SetBranchAddress(jet_type_PUPPI+"_phi"                     ,&JetPhi_PUPPI);
// ======================= Assisting variables ================================
float dEta, dPhi, dR;

// =============================  Definitions =================================
// -- histograms definitions
TH1F *hist_deltaR_CHS = new TH1F("hist_deltaR_CHS","hist_deltaR_CHS",50,0.,1.0);
TH1F *hist_deltaR_PUPPI = new TH1F("hist_deltaR_PUPPI","hist_deltaR_PUPPI",50,0.,1.0);


// ======================= Run over events ====================================
int Nevents = 100000;//tree -> GetEntries();

Float_t PROGRESS_COUNTER = 0.;

for(int iEvent=0;iEvent<Nevents;iEvent++){
  if (iEvent/(Nevents*1.)>PROGRESS_COUNTER){
	  cout << PROGRESS_COUNTER*100. << " %" << endl;
	  PROGRESS_COUNTER += 0.1;
  }

  tree -> GetEntry(iEvent);
  
  for(int iGenJet=0;iGenJet<(*genJetEta).size();iGenJet++){
    if((*genJetPt)[iGenJet]<30.){
        continue;
    }
    for(int iJet=0;iJet<(*JetEta_CHS).size();iJet++){
      if((*JetPt_CHS)[iJet]<30.){
        continue;
      }
      // CHS jets 
      dEta = (*JetEta_CHS)[iJet] - (*genJetEta)[iGenJet];
      dPhi = TVector2::Phi_mpi_pi((*JetPhi_CHS)[iJet] - (*genJetPhi)[iGenJet]);
      dR   = TMath::Sqrt( dEta*dEta+dPhi*dPhi );
       
      hist_deltaR_CHS -> Fill(dR);
    }// loop over reco CHS jets

    for(int iJet=0;iJet<(*JetEta_PUPPI).size();iJet++){
      if((*JetPt_PUPPI)[iJet]<30.){
        continue;
      }
      // PUPPI jets 
      dEta = (*JetEta_PUPPI)[iJet] - (*genJetEta)[iGenJet];
      dPhi = TVector2::Phi_mpi_pi((*JetPhi_PUPPI)[iJet] - (*genJetPhi)[iGenJet]);
      dR   = TMath::Sqrt( dEta*dEta+dPhi*dPhi );
       
      hist_deltaR_PUPPI -> Fill(dR);
    }// loop over reco PUPPI jets

  }// loop over gen jets

}// loop over events

TFile *output_file = TFile::Open("deltaRValidation_output.root","RECREATE");

TCanvas *can = new TCanvas("can","can",900,600);
can -> SetLogy(true);

hist_deltaR_CHS -> SetLineWidth(2);
hist_deltaR_CHS -> SetLineColor(kBlue);

hist_deltaR_PUPPI -> SetLineWidth(2);
hist_deltaR_PUPPI -> SetLineColor(kRed);

hist_deltaR_CHS -> SetTitle("");
hist_deltaR_CHS -> GetYaxis() -> SetTitle("entries");
hist_deltaR_CHS -> GetXaxis() -> SetTitle("#DeltaR(reco,gen) jets");
hist_deltaR_CHS -> Draw();
hist_deltaR_PUPPI -> Draw("SAME");

TLegend *legend = new TLegend(0.7,0.7,0.90,0.90);
 
legend -> AddEntry(hist_deltaR_CHS,"AK4 CHS jets","l");
legend -> AddEntry(hist_deltaR_PUPPI,"AK4 PUPPI jets","l");
legend -> Draw();

can-> Write();


}