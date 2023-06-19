void ZjetAnalysisTest(){
  //--- file open ---
  TFile *inf = TFile::Open("testZjet.root");
  TTree *tree = (TTree*) inf -> Get("JMETriggerNTuple/Events");
  
  //--- get tree variables ---

  // trigger
  bool DimuonTriggerVLL;
  tree -> SetBranchAddress("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8", &DimuonTriggerVLL);

  // HLT AK4 PF jets
  vector<double> *hltAK4PFJetsCorrected_pt(0);
  vector<double> *hltAK4PFJetsCorrected_eta(0);
  vector<double> *hltAK4PFJetsCorrected_phi(0);
  vector<double> *hltAK4PFJetsCorrected_mass(0);

  tree -> SetBranchAddress("hltAK4PFJetsCorrected_pt", &hltAK4PFJetsCorrected_pt);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_eta", &hltAK4PFJetsCorrected_eta);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_phi", &hltAK4PFJetsCorrected_phi);
  tree -> SetBranchAddress("hltAK4PFJetsCorrected_mass", &hltAK4PFJetsCorrected_mass);

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
  TH1F *h_ptResponse = new TH1F("h_ptResponse","h_ptResponse",50,0.,2.);


  


  unsigned int Nevents = tree -> GetEntries();
  cout <<"# of events: " << Nevents << endl;
  Float_t PROCESS_COUNTER = 0.;

  // loop over the events
  for (unsigned int i=0;i<Nevents;i++){
    if (i/(Nevents*1.)>PROCESS_COUNTER){
	  cout << PROCESS_COUNTER*100. << " %" << endl;
	  PROCESS_COUNTER += 0.1;
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
    cut_kinematics_jet = ( fabs((*hltAK4PFJetsCorrected_eta)[0]) < 1.3 ) 
                    and  ( (*hltAK4PFJetsCorrected_pt)[0] > 30. ) 
                    and  ( ( Njets > 1 ) ? (*hltAK4PFJetsCorrected_pt)[1]/(*hltAK4PFJetsCorrected_pt)[0] < 1.0 : true);
    if (!cut_kinematics_jet) continue;

    //Z (dimuon) cuts
    cut_dimuon = ( p4_Z.DeltaPhi(p4_jet)< 0.44 ) and ( fabs(p4_Z.M() - 90) < 20 ) and ( p4_Z.Pt() > 50 );
    if (!cut_dimuon) continue; 
    
    h_ptResponse -> Fill(p4_jet.Pt()/p4_Z.Pt());

    
    
  } // end on events loop
  
  h_ptResponse -> Draw();
  
}