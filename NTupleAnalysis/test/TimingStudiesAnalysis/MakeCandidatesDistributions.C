//=======================================================================================================|
// Macro for tests of candidates distributions originating from matched to gen and PU jets               |
// quantities can be calculated and weighted with different weight types                                 |
//=======================================================================================================|


// function that given jet direction and all gen jets directions says where the jet belongs to.
// possible categories:
// * MatchedToGen  -> Matched with at least one generated jet within some cone dR_max
// * NotMatchedToGen -> The oposite of MatchedToGen
// * NotMatchedToGen_PU -> Not matched to gen jets but far enough from them to be called "pileup jet"

string jetMatchingCategory(float JetEta, float JetPhi, vector<float> genJetEta, vector<float> genJetPhi, float dR_matching=0.2, float dR_PU=0.6){
    string jetCategory="NotMatchedToGen";
    float dEta, dPhi, dR, dR_min=1000.;
    
    for(int iGenJet=0;iGenJet< genJetEta.size();iGenJet++){
        dEta = JetEta - genJetEta[iGenJet];
        dPhi = TVector2::Phi_mpi_pi(JetPhi - genJetPhi[iGenJet]);
        dR   = TMath::Sqrt( dEta*dEta+dPhi*dPhi );
        
        // update the minimum dR value from gen jets
        if(dR<dR_min){
           dR_min=dR;
        }

        // in case at least one gen jet is "close" to our jet then it is matched
        if( dR<dR_matching){
           jetCategory="MatchedToGen";
           return jetCategory;
        }
    } // loop over gen jets directions
    
    if(dR_min>dR_PU){
        jetCategory="NotMatchedToGen_PU";
    }

    return jetCategory;
}


// main function
void MakeCandidatesDistributions(){

gROOT->SetBatch(kTRUE); // not show canvases when draw


// --- Define the input file
TFile *inf = TFile::Open("/eos/user/t/tchatzis/MTDtiming_samples/samples/Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200/Phase2HLTTDR_QCD_Flat_Pt-15to3000_14TeV_PU200.root");


// ============================= Input variables ==============================

// -- jet type e.g. offline CHS 
TString jet_type  = "offlineAK4PFCHSJetsCorrected";
//TString jet_type  = "offlineAK4PFPuppiJetsCorrected";

// weight types for candidates e.g. raw, energy weigghted, puppi, puppiNoLep
const int N_weights_methods = 2;
//std::array<std::pair<string,float>, N_weights_methods> weight_method;
//weight_method[0].first = "unweighted";
//weight_method[1].first = "energy weighted";
vector<float> weight[N_weights_methods]; // vector with weights for all particles in a jet
float weight_sum[N_weights_methods];     // vector with sum of weights of all particles in a jet

TString weight_name[N_weights_methods] = {
"unweighted"            ,//0
"energy_weighted"        //1
};



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
vector<uint>  *JetNumberOfDaughters(0);
vector<float> *JetPt(0);
vector<float> *JetEta(0);
vector<float> *JetPhi(0);

tree -> SetBranchAddress(jet_type+"_numberOfDaughters"       ,&JetNumberOfDaughters);
tree -> SetBranchAddress(jet_type+"_pt"                      ,&JetPt);
tree -> SetBranchAddress(jet_type+"_eta"                     ,&JetEta);
tree -> SetBranchAddress(jet_type+"_phi"                     ,&JetPhi);

// - candidates -
vector<float> *CandidateEnergy(0);
vector<float> *CandidatePt(0);
vector<float> *CandidateEta(0);
vector<float> *CandidatePhi(0);
vector<float> *CandidateTime(0);
vector<float> *CandidateTimeError(0);
vector<float> *CandidateVx(0);
vector<float> *CandidateVy(0);
vector<float> *CandidateVz(0);
vector<int>   *CandidateBelongsToJet(0);

tree -> SetBranchAddress(jet_type+"_CandidateEnergy"            ,&CandidateEnergy);
tree -> SetBranchAddress(jet_type+"_CandidatePt"                ,&CandidatePt);
tree -> SetBranchAddress(jet_type+"_CandidateEta"               ,&CandidateEta);
tree -> SetBranchAddress(jet_type+"_CandidatePhi"               ,&CandidatePhi);
tree -> SetBranchAddress(jet_type+"_CandidateTime"              ,&CandidateTime);
tree -> SetBranchAddress(jet_type+"_CandidateTimeError"         ,&CandidateTimeError);
tree -> SetBranchAddress(jet_type+"_CandidateVx"                ,&CandidateVx);
tree -> SetBranchAddress(jet_type+"_CandidateVy"                ,&CandidateVy);
tree -> SetBranchAddress(jet_type+"_CandidateVz"                ,&CandidateVz);
tree -> SetBranchAddress(jet_type+"_CandidateBelongsToJet"      ,&CandidateBelongsToJet);


// - vertices -
vector<float> *vertexTime(0);
vector<float> *vertexTimeError(0);

tree -> SetBranchAddress("offlineSlimmedPrimaryVertices4D_t"    ,&vertexTime);
tree -> SetBranchAddress("offlineSlimmedPrimaryVertices4D_tError"    ,&vertexTimeError);

// ======================= Assisting variables ================================
// -- timing related quantities for candidates of jets
const int N_vars = 5;

vector<float> var[N_vars];    // vector with variables values for all particles in a jet

TString var_name[N_vars][2] = {
{"deltaTime"                 ,"#Deltat [ns]"}                              ,//0
{"error_deltaTime"           ,"#sigma(#Deltat) [ns]"}                      ,//1
{"significance_deltaTime"    ,"|#Deltat|/#sigma(#Deltat)"}                 ,//2
{"candidate_time"            ,"candidate time [ns]"}                       ,//3
{"candidate_timeError"       ,"candidate #sigma(time) [ns]"}               ,//4
};

float var_ranges[N_vars][3] = {
{40,-0.5,0.5}       ,//0
{30,0.0,0.05}     ,//1
{30,0.,5.}        ,//2
{40,-0.5,0.5}       ,//3
{30,0.0,0.05}      //4
}; 

// -- vertex time
float LeadingVertexTime, LeadingVertexTimeError;

// -- variables for cuts
bool healthyVertex; // when the HS vertex (assumed to be first in collection) has tError>0
bool healthyParticle; // for a particle to be accepted in the histograms it must have timeError>0
bool JetPtCut; //  jets that are considered have a cut in pt

const float JetPtMin = 30; // minimum 30 GeV

vector<float> accepted_GenJetEta(0);
vector<float> accepted_GenJetPhi(0);

unsigned int FirstCandidateIndex;

string MatchCategory;

// =============================  Definitions =================================
// ----- histograms definitions
// there will be defined:
// N_vars variables ( e.g. time, time_error, significance) for
// N_weights_methods (e.g. no weight, energy weight)
// and these for 2 types of particles, belonging to matched jets and PU jets
// that yields : N_vars*N_weights_methods histograms for each category of jets

TH1F *hist_var_weight_MatchedToGen[N_vars][N_weights_methods];
TH1F *hist_var_weight_NotMatchedToGen_PU[N_vars][N_weights_methods];
TString histo_name = "";

for(int iVar=0;iVar<N_vars;iVar++){
  for(int iMethod=0;iMethod<N_weights_methods;iMethod++){
    histo_name  = var_name[iVar][0]+"_"+ weight_name[iMethod]+"_MatchedToGen";

    hist_var_weight_MatchedToGen[iVar][iMethod] = new TH1F(
       histo_name, histo_name, static_cast<int>(var_ranges[iVar][0]), var_ranges[iVar][1], var_ranges[iVar][2]
    );
    hist_var_weight_MatchedToGen[iVar][iMethod] -> Sumw2();
    
    histo_name  = var_name[iVar][0]+"_"+weight_name[iMethod]+"_NotMatchedToGen_PU";

    hist_var_weight_NotMatchedToGen_PU[iVar][iMethod] = new TH1F(
       histo_name, histo_name, static_cast<int>(var_ranges[iVar][0]), var_ranges[iVar][1], var_ranges[iVar][2]
    );
    hist_var_weight_NotMatchedToGen_PU[iVar][iMethod] -> Sumw2();
  }// loop over weight methods
}// loop over variables


TH1F *hist_LeadingVertexTime = new TH1F("hist_LeadingVertexTime","hist_LeadingVertexTime",30,-1.,1.);
TH1F *hist_LeadingVertexTimeError = new TH1F("hist_LeadingVertexTimeError","hist_LeadingVertexTimeError",30,0.,0.05);

// ======================= Run over events ====================================
int Nevents = 100000;// tree -> GetEntries();

/*
tree -> GetEntry(0);
for (unsigned int iCandidate=0;iCandidate<(*CandidateBelongsToJet).size();iCandidate++){
    cout << (*CandidateBelongsToJet)[iCandidate] << endl;
}// loop over candidates
*/

Float_t PROGRESS_COUNTER = 0.;

for(int iEvent=0;iEvent<Nevents;iEvent++){
  if (iEvent/(Nevents*1.)>PROGRESS_COUNTER){
	  cout << PROGRESS_COUNTER*100. << " %" << endl;
	  PROGRESS_COUNTER += 0.1;
  }

  tree -> GetEntry(iEvent);
  
  
  // --- reject the event if leading vertex has no time measurement
  LeadingVertexTime = (*vertexTime)[0];
  LeadingVertexTimeError = (*vertexTimeError)[0];
  if( !(LeadingVertexTimeError > 0) ){
    continue;
  }

  hist_LeadingVertexTime -> Fill(LeadingVertexTime);
  hist_LeadingVertexTimeError -> Fill(LeadingVertexTimeError);



  // --- selection of gen jets with minimum pt requirement (these directions will be used for the matching)
  for(int iGenJet=0;iGenJet<(*genJetPt).size();iGenJet++){
    if((*genJetPt)[iGenJet]>JetPtMin){
      accepted_GenJetEta.push_back((*genJetEta)[iGenJet]);
      accepted_GenJetPhi.push_back((*genJetPhi)[iGenJet]);
    }
  }// loop over gen jets
  
  FirstCandidateIndex = 0;

  for(int iJet=0;iJet<(*JetPt).size();iJet++){
    // - jet pt cut
    JetPtCut = ((*JetPt)[iJet]>JetPtMin);
    if(!JetPtCut){
        // --- changing the first particle index for the next loop and continue with next jet
        FirstCandidateIndex += (*JetNumberOfDaughters)[iJet];
        continue;
    }
    
    // - clear vectors that are filled for all particles per jet
    for(int iVar=0;iVar<N_vars;iVar++){
      var[iVar].clear();
    }

    // - clear the weight vector and initialize the weight sums
    for(int iWeight=0;iWeight<N_weights_methods;iWeight++){
      weight[iWeight].clear();
      weight_sum[iWeight] = 0.0;
    }

    for(unsigned int iCandidate=FirstCandidateIndex;iCandidate<(FirstCandidateIndex+(*JetNumberOfDaughters)[iJet]);iCandidate++){
       // - time error cut for candidates
       if((*CandidateTimeError)[iCandidate]<0 || (*CandidateTimeError)[iCandidate]>0.025){
        continue;
       }
       
       // exception that checks that the jet index is correctly assigned
       try{
          if(  (*CandidateBelongsToJet)[iCandidate] - iJet != 0 ){
            throw "ERROR: jets and candidates are not correctly assigned!";
          }
       }catch(const char* error_message) {
        cerr << error_message << endl;
        std::exit( EXIT_FAILURE );
       }
       

       // --- calculation of variables   
       var[0].push_back(  (*CandidateTime)[iCandidate] - LeadingVertexTime  );  
       var[1].push_back(  sqrt( (*CandidateTimeError)[iCandidate]*(*CandidateTimeError)[iCandidate] + LeadingVertexTimeError*LeadingVertexTimeError)   );
       var[2].push_back(   fabs((var[0])[iCandidate])/(var[1])[iCandidate]   );
       var[3].push_back((*CandidateTime)[iCandidate]);
       var[4].push_back((*CandidateTimeError)[iCandidate]);

       // --- weights and their sum calculation if needed (else the weight sum will be 0.0 and will not be used for the histos fill weight)
       weight[0].push_back(1.);

       weight[1].push_back( (*CandidateEnergy)[iCandidate] );
       weight_sum[1] += (weight[1])[iCandidate];
    }// loop over candidates
    

    // --- Filing histograms depending on jet category
    // MatchedToGen -> Fill matched to gen histos
    // NotMacthedToGen_PU -> Fill the PU histos
    // NotMatchedToGen -> don't fill anything , i.e. these jets are not considered

    // -- find the category the jet belongs to
    MatchCategory = jetMatchingCategory( (*JetEta)[iJet], (*JetPhi)[iJet], accepted_GenJetEta, accepted_GenJetPhi);

    for(int iVar=0;iVar<N_vars;iVar++){
       for(int iMethod=0;iMethod<N_weights_methods;iMethod++){
         // -- depending the category of the jet fill the corresponding histograms
         if(MatchCategory == "MatchedToGen"){
           // fill all the particles with the weights
           for(int iCandidate=0;iCandidate<var[iVar].size();iCandidate++){
             if(weight_sum[iMethod]>1e-06){
               hist_var_weight_MatchedToGen[iVar][iMethod]-> Fill( (var[iVar])[iCandidate]*(weight[iMethod])[iCandidate]/weight_sum[iMethod]);
             }else{
               hist_var_weight_MatchedToGen[iVar][iMethod]-> Fill( (var[iVar])[iCandidate]*(weight[iMethod])[iCandidate]);
             }
           }
         }


         if(MatchCategory == "NotMatchedToGen_PU"){
           // fill all the particles with the weights
           for(int iCandidate=0;iCandidate<var[iVar].size();iCandidate++){
             if(weight_sum[iMethod]>1e-06){
               hist_var_weight_NotMatchedToGen_PU[iVar][iMethod]-> Fill( (var[iVar])[iCandidate]*(weight[iMethod])[iCandidate]/weight_sum[iMethod]);
             }else{
               hist_var_weight_NotMatchedToGen_PU[iVar][iMethod]-> Fill( (var[iVar])[iCandidate]*(weight[iMethod])[iCandidate]);
             }
           }
         }
         
         
      }// loop over weight methods
    }// loop over variables


    // --- changing the first particle index for the next loop
    FirstCandidateIndex += (*JetNumberOfDaughters)[iJet];

    
  }// loop over jets

}// loop over events


// ======================= Make plots and save them ===========================
//gStyle -> SetOptStat(0);

TFile *output_file = TFile::Open("CandidatesDistributions_output.root","RECREATE");

TCanvas *can_var_weight[N_vars][N_weights_methods];
TLegend *legend;

for(int iVar=0;iVar<N_vars;iVar++){
  for(int iMethod=0;iMethod<N_weights_methods;iMethod++){
    
    can_var_weight[iVar][iMethod] = new TCanvas(var_name[iVar][0]+"_"+weight_name[iMethod], var_name[iVar][0]+"_"+weight_name[iMethod], 900,600);
    
    // normalize to unity integral
    hist_var_weight_MatchedToGen[iVar][iMethod]-> Scale(1./hist_var_weight_MatchedToGen[iVar][iMethod]->Integral());
    hist_var_weight_NotMatchedToGen_PU[iVar][iMethod]-> Scale(1./hist_var_weight_NotMatchedToGen_PU[iVar][iMethod]->Integral());
    
    hist_var_weight_MatchedToGen[iVar][iMethod]-> SetLineWidth(2);
    hist_var_weight_NotMatchedToGen_PU[iVar][iMethod]-> SetLineWidth(2);

    hist_var_weight_MatchedToGen[iVar][iMethod]-> SetLineColor(kBlue);
    hist_var_weight_NotMatchedToGen_PU[iVar][iMethod]-> SetLineColor(kRed);
    
    hist_var_weight_MatchedToGen[iVar][iMethod]-> SetTitle(jet_type);
    hist_var_weight_MatchedToGen[iVar][iMethod]-> GetXaxis() -> SetTitle(weight_name[iMethod]+" "+var_name[iVar][1]);
    hist_var_weight_MatchedToGen[iVar][iMethod]-> GetYaxis() -> SetTitle("normalized to unity");

    hist_var_weight_MatchedToGen[iVar][iMethod]-> Draw("HIST E1");
    hist_var_weight_NotMatchedToGen_PU[iVar][iMethod]-> Draw("HIST E1 SAME");

    legend = new TLegend(0.7,0.7,0.90,0.90);
 
    legend -> AddEntry(hist_var_weight_MatchedToGen[iVar][iMethod],"Matched to Gen jets","le");
    legend -> AddEntry(hist_var_weight_NotMatchedToGen_PU[iVar][iMethod],"PU jets","le");

    legend -> Draw();
    can_var_weight[iVar][iMethod] -> Write();
         
  }// loop over weight methods
}// loop over variables

TCanvas *can_LeadingVertexTime = new TCanvas("LeadingVertexTime","LeadingVertexTime",900,600);
hist_LeadingVertexTime -> SetTitle("");
hist_LeadingVertexTime -> SetLineWidth(2);
hist_LeadingVertexTime -> GetXaxis() -> SetTitle("leading vertex time [ns]");
hist_LeadingVertexTime -> GetYaxis() -> SetTitle("entries");
hist_LeadingVertexTime -> Draw("HIST E");

can_LeadingVertexTime -> Write();

TCanvas *can_LeadingVertexTimeError = new TCanvas("LeadingVertexTimeError","LeadingVertexTimeError",900,600);
hist_LeadingVertexTimeError -> SetTitle("");
hist_LeadingVertexTimeError -> SetLineWidth(2);
hist_LeadingVertexTimeError -> GetXaxis() -> SetTitle("leading vertex #sigma(time) [ns]");
hist_LeadingVertexTimeError -> GetYaxis() -> SetTitle("entries");
hist_LeadingVertexTimeError -> Draw("HIST E");

can_LeadingVertexTimeError -> Write();

output_file -> Close();
inf -> Close();


}