void ZjetAnalysisTest(){
  
  float minPtZ = 100.;
  
  //--- file open ---
  TFile *inf = TFile::Open("/eos/user/t/tchatzis/samples2023/test_DYToMuMu//HLT_Run3TRK/samples_merged/DYToMuMu_M-20_TuneCP5_13p6TeV-pythia8.root");
  TTree *tree = (TTree*) inf -> Get("JMETriggerNTuple/Events");
  
  bool makeGenPlots = true; 
  //--- get tree variables ---

  // trigger
  bool DimuonTriggerVLL;
  tree -> SetBranchAddress("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8", &DimuonTriggerVLL);
  
  // HLT AK4 PF jets
  vector<double> *hltAK4PFJetsCorrected_pt(0);
  vector<double> *hltAK4PFJetsCorrected_eta(0);
  vector<double> *hltAK4PFJetsCorrected_phi(0);
  vector<double> *hltAK4PFJetsCorrected_mass(0);
  vector<double> *hltAK4PFJetsCorrected_chargedHadronEnergyFraction(0);
  vector<double> *hltAK4PFJetsCorrected_neutralHadronEnergyFraction(0);
  vector<double> *hltAK4PFJetsCorrected_photonEnergyFraction(0);

  tree -> SetBranchAddress("hltAK4PFJetsCorrected_pt", &hltAK4PFJetsCorrected_pt);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_eta", &hltAK4PFJetsCorrected_eta);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_phi", &hltAK4PFJetsCorrected_phi);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_mass", &hltAK4PFJetsCorrected_mass);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_chargedHadronEnergyFraction", &hltAK4PFJetsCorrected_chargedHadronEnergyFraction);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_neutralHadronEnergyFraction", &hltAK4PFJetsCorrected_neutralHadronEnergyFraction);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_photonEnergyFraction", &hltAK4PFJetsCorrected_photonEnergyFraction);
  
  vector<double> *hltAK4GenJets_pt(0);
  vector<double> *hltAK4GenJets_eta(0);
  vector<double> *hltAK4GenJets_phi(0);
  vector<double> *hltAK4GenJets_mass(0);
  vector<double> *hltAK4GenJets_chargedHadronEnergyFraction(0);
  vector<double> *hltAK4GenJets_neutralHadronEnergyFraction(0);
  vector<double> *hltAK4GenJets_photonEnergyFraction(0);
  if (makeGenPlots){
    tree -> SetBranchAddress("ak4GenJetsNoNu_pt", &hltAK4GenJets_pt);
    tree -> SetBranchAddress("ak4GenJetsNoNu_eta", &hltAK4GenJets_eta);
    tree -> SetBranchAddress("ak4GenJetsNoNu_phi", &hltAK4GenJets_phi);
    tree -> SetBranchAddress("ak4GenJetsNoNu_mass", &hltAK4GenJets_mass);
    tree -> SetBranchAddress("ak4GenJetsNoNu_chargedHadronEnergyFraction", &hltAK4GenJets_chargedHadronEnergyFraction);
    tree -> SetBranchAddress("ak4GenJetsNoNu_neutralHadronEnergyFraction", &hltAK4GenJets_neutralHadronEnergyFraction);
    tree -> SetBranchAddress("ak4GenJetsNoNu_photonEnergyFraction", &hltAK4GenJets_photonEnergyFraction);
  }

  // HLT muons (Loose ID)
  vector<double> *hltMuons_pt(0);
  vector<double> *hltMuons_eta(0);
  vector<double> *hltMuons_phi(0);
  vector<double> *hltMuons_mass(0);

  vector<int> *hltMuons_pdgId(0);

  tree -> SetBranchAddress("hltMuons_pt", &hltMuons_pt);
  tree -> SetBranchAddress("hltMuons_eta", &hltMuons_eta);
  tree -> SetBranchAddress("hltMuons_phi", &hltMuons_phi);
  tree -> SetBranchAddress("hltMuons_mass", &hltMuons_mass);

  tree -> SetBranchAddress("hltMuons_pdgId", &hltMuons_pdgId);

  
  // cuts variables
  bool cut_finalState = false;
  bool cut_kinematics_muons = false;
  bool cut_kinematics_jet = false;
  bool cut_dimuon = false;

  // assisting variables
  TLorentzVector p4_mu1;
  TLorentzVector p4_mu2;
  TLorentzVector p4_jet;
  TLorentzVector p4_Z;

  Int_t Nmuons; // number of muons (set to 2)
  Int_t Njets; // >= 1 at least one jet


  // histograms definitions
  TH1F *h_ptResponse_Barrel = new TH1F("h_ptResponse_Barrel","h_ptResponse_Barrel",50,0.,2.);
  TH1F *h_chf_Barrel = new TH1F("h_chf_Barrel","h_chf_Barrel",50,0.,1.);
  TH1F *h_nhf_Barrel = new TH1F("h_nhf_Barrel","h_nhf_Barrel",50,0.,1.);
  TH1F *h_pf_Barrel = new TH1F("h_pf_Barrel","h_pf_Barrel",50,0.,1.);
  TH1F *h_ptResponse_Endcap = new TH1F("h_ptResponse_Endcap","h_ptResponse_Endcap",50,0.,2.);
  TH1F *h_chf_Endcap = new TH1F("h_chf_Endcap","h_chf_Endcap",50,0.,1.);
  TH1F *h_nhf_Endcap = new TH1F("h_nhf_Endcap","h_nhf_Endcap",50,0.,1.);
  TH1F *h_pf_Endcap = new TH1F("h_pf_Endcap","h_pf_Endcap",50,0.,1.);
  TH1F *h_ptResponse_Barrel_0p0_0p8 = new TH1F("h_ptResponse_Barrel_0p0_0p8","h_ptResponse_Barrel_0p0_0p8",50,0.,2.);
  TH1F *h_chf_Barrel_0p0_0p8 = new TH1F("h_chf_Barrel_0p0_0p8","h_chf_Barrel_0p0_0p8",50,0.,1.);
  TH1F *h_nhf_Barrel_0p0_0p8 = new TH1F("h_nhf_Barrel_0p0_0p8","h_nhf_Barrel_0p0_0p8",50,0.,1.);
  TH1F *h_pf_Barrel_0p0_0p8 = new TH1F("h_pf_Barrel_0p0_0p8","h_pf_Barrel_0p0_0p8",50,0.,1.);
  TH1F *h_ptResponse_Barrel_0p8_1p3 = new TH1F("h_ptResponse_Barrel_0p8_1p3","h_ptResponse_Barrel_0p8_1p3",50,0.,2.);
  TH1F *h_chf_Barrel_0p8_1p3 = new TH1F("h_chf_Barrel_0p8_1p3","h_chf_Barrel_0p8_1p3",50,0.,1.);
  TH1F *h_nhf_Barrel_0p8_1p3 = new TH1F("h_nhf_Barrel_0p8_1p3","h_nhf_Barrel_0p8_1p3",50,0.,1.);
  TH1F *h_pf_Barrel_0p8_1p3 = new TH1F("h_pf_Barrel_0p8_1p3","h_pf_Barrel_0p8_1p3",50,0.,1.);

  TH1F *h_ptResponseGen_Barrel = new TH1F("h_ptResponseGen_Barrel","h_ptResponseGen_Barrel",50,0.,2.);
  TH1F *h_ptResponseGen_Endcap = new TH1F("h_ptResponseGen_Endcap","h_ptResponseGen_Endcap",50,0.,2.);


  


  unsigned int Nevents = 4000000;//tree -> GetEntries();
  cout <<"# of events: " << Nevents << endl;
  Float_t PROCESS_COUNTER = 0.;

  // loop over the events
  for (unsigned int i=0;i<Nevents;i++){
    if (i/(Nevents*1.)>PROCESS_COUNTER){
	  cout << PROCESS_COUNTER*100. << " %" << endl;
	  PROCESS_COUNTER += 0.01;
    }
    
    tree -> GetEntry(i);
    

    //--- cuts application
    //trigger
    if (!DimuonTriggerVLL) continue;
    
    //finalState
    Nmuons = hltMuons_pt->size();
    Njets = hltAK4PFJetsCorrected_pt->size();
    cut_finalState = ( Nmuons == 2 ) and ( Njets > 0);
    if (!cut_finalState) continue;

    p4_mu1.SetPtEtaPhiM((*hltMuons_pt)[0],(*hltMuons_eta)[0],(*hltMuons_phi)[0],(*hltMuons_mass)[0]);
    p4_mu2.SetPtEtaPhiM((*hltMuons_pt)[1],(*hltMuons_eta)[1],(*hltMuons_phi)[1],(*hltMuons_mass)[1]);

    p4_Z = p4_mu1 + p4_mu2;

    p4_jet.SetPtEtaPhiM((*hltAK4PFJetsCorrected_pt)[0],(*hltAK4PFJetsCorrected_eta)[0],(*hltAK4PFJetsCorrected_phi)[0],(*hltAK4PFJetsCorrected_mass)[0]);
    
    //muons cuts
    cut_kinematics_muons = ( (*hltMuons_pdgId)[0]*(*hltMuons_pdgId)[1] < 0. ) 
                      and  ( (*hltMuons_pt)[1] > 20. ) 
                      and  ( fabs((*hltMuons_eta)[0]) < 2.3 ) and ( fabs((*hltMuons_eta)[1]) < 2.3 );
    if (!cut_kinematics_muons) continue;

    //jets cuts
    cut_kinematics_jet = ( fabs((*hltAK4PFJetsCorrected_eta)[0]) < 2.5 ) 
                    and  ( (*hltAK4PFJetsCorrected_pt)[0] > 0.8*minPtZ ) 
                    and  ( ( Njets > 1 ) ? (*hltAK4PFJetsCorrected_pt)[1]/p4_Z.Pt() < 1.0 : true );
    if (!cut_kinematics_jet) continue;

    //Z (dimuon) cuts
    cut_dimuon = ( p4_Z.DeltaPhi(p4_jet) > 2.7 ) and ( fabs(p4_Z.M() - 90) < 20 ) and ( p4_Z.Pt() > minPtZ );
    if (!cut_dimuon) continue; 
    
    if (fabs(p4_jet.Eta())<1.3){
      h_ptResponse_Barrel -> Fill(p4_jet.Pt()/p4_Z.Pt());
      h_chf_Barrel -> Fill((*hltAK4PFJetsCorrected_chargedHadronEnergyFraction)[0]);
      h_nhf_Barrel -> Fill((*hltAK4PFJetsCorrected_neutralHadronEnergyFraction)[0]);
      h_pf_Barrel -> Fill((*hltAK4PFJetsCorrected_photonEnergyFraction)[0]);
      if(fabs(p4_jet.Eta())<0.8){
        h_ptResponse_Barrel_0p0_0p8 -> Fill(p4_jet.Pt()/p4_Z.Pt());
        h_chf_Barrel_0p0_0p8 -> Fill((*hltAK4PFJetsCorrected_chargedHadronEnergyFraction)[0]);
        h_nhf_Barrel_0p0_0p8 -> Fill((*hltAK4PFJetsCorrected_neutralHadronEnergyFraction)[0]);
        h_pf_Barrel_0p0_0p8 -> Fill((*hltAK4PFJetsCorrected_photonEnergyFraction)[0]);
      }else{
        h_ptResponse_Barrel_0p8_1p3 -> Fill(p4_jet.Pt()/p4_Z.Pt());
        h_chf_Barrel_0p8_1p3 -> Fill((*hltAK4PFJetsCorrected_chargedHadronEnergyFraction)[0]);
        h_nhf_Barrel_0p8_1p3 -> Fill((*hltAK4PFJetsCorrected_neutralHadronEnergyFraction)[0]);
        h_pf_Barrel_0p8_1p3 -> Fill((*hltAK4PFJetsCorrected_photonEnergyFraction)[0]);
      }
      if (makeGenPlots){
        h_ptResponseGen_Barrel -> Fill((*hltAK4GenJets_pt)[0]/p4_Z.Pt());
      }
    }else{
      h_ptResponse_Endcap -> Fill(p4_jet.Pt()/p4_Z.Pt());
      h_chf_Endcap -> Fill((*hltAK4PFJetsCorrected_chargedHadronEnergyFraction)[0]);
      h_nhf_Endcap -> Fill((*hltAK4PFJetsCorrected_neutralHadronEnergyFraction)[0]);
      h_pf_Endcap -> Fill((*hltAK4PFJetsCorrected_photonEnergyFraction)[0]);
      if (makeGenPlots){
        h_ptResponseGen_Endcap -> Fill((*hltAK4GenJets_pt)[0]/p4_Z.Pt());
      }
    }
    

    
    
  } // end on events loop
  
  TFile *outf = TFile::Open("output_Zjet_MCgen_latest2.root","RECREATE");
  h_ptResponse_Barrel -> Write();
  h_chf_Barrel -> Write();
  h_nhf_Barrel -> Write();
  h_pf_Barrel -> Write();
  h_ptResponse_Endcap -> Write();
  h_chf_Endcap -> Write();
  h_nhf_Endcap -> Write();
  h_pf_Endcap -> Write();
  h_ptResponse_Barrel_0p0_0p8 -> Write();
  h_chf_Barrel_0p0_0p8 -> Write();
  h_nhf_Barrel_0p0_0p8 -> Write();
  h_pf_Barrel_0p0_0p8 -> Write();
  h_ptResponse_Barrel_0p8_1p3 -> Write();
  h_chf_Barrel_0p8_1p3 -> Write();
  h_nhf_Barrel_0p8_1p3 -> Write();
  h_pf_Barrel_0p8_1p3 -> Write();
  if (makeGenPlots){
    h_ptResponseGen_Barrel -> Write();
    h_ptResponseGen_Endcap -> Write();
  }

  outf -> Close();
  inf -> Close();
  
}
