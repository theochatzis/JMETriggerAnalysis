#define postproc_pfhc_cxx
#include "postproc_pfhc.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

float deltaR2(float eta1, float eta2, float phi1, float phi2) {
  float dp = std::abs(phi1 - phi2);
  if (dp > float(M_PI))
    dp -= float(2 * M_PI);
  return (eta1 - eta2) * (eta1 - eta2) + dp * dp;
}


int main(int argc, char *argv[])
{
  if(argc > 1)
  { 
    postproc_pfhc t(argv[1], argv[2]);
    t.Loop(argv[2]);
  }

  return 0;
}

using namespace std;

void postproc_pfhc::Loop(const char* file2)
{

//   In a ROOT session, you can do:
//      root> .L postproc_pfhc.C
//      root> postproc_pfhc t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;

   TFile *file;
   file = new TFile(file2, "recreate");
   file->cd();
   TH1F *dR = new TH1F ("dR", "dR", 200, 0, 20);
   TH1F *reso_eh_barrel = new TH1F ("reso_eh_barrel", "reso_eh_barrel", 200, -1.5, 1.5);
   TH1F *reso_h_barrel = new TH1F ("reso_h_barrel", "reso_h_barrel", 200, -1.5, 1.5);
   TH1F *reso_eh_endcap = new TH1F ("reso_eh_endcap", "reso_eh_endcap", 200, -1.5, 1.5);
   TH1F *reso_h_endcap = new TH1F ("reso_h_endcap", "reso_h_endcap", 200, -1.5, 1.5);

   Float_t true_, ecal_, hcal_, eta_, phi_, p_;
   TTree *s = new TTree("Candidates", "Candidates");
   s->Branch("true",&true_,"true/F");
   s->Branch("ecal",&ecal_,"ecal/F");
   s->Branch("hcal",&hcal_,"hcal/F");
   s->Branch("eta",&eta_,"eta/F");
   s->Branch("phi",&phi_,"phi/F");
   s->Branch("p",&p_,"p/F");


   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);
      nbytes += nb;

      for(int j = 0; j < true_energy->size(); j++){
         double Dr = 99.;
         //neutron
         if(true_charge->at(j) == 0){
            eta_ = true_eta->at(j);
            phi_ = true_phi->at(j);
            true_ = true_energy->at(j);
            p_ = 0.;
            ecal_ = 0.;
            hcal_ = 0.;
            for(int i = 0; i < pfc_charge->size(); i++){
               Dr = deltaR2(pfc_eta->at(i), eta_, pfc_phi->at(i), phi_);
               dR->Fill(Dr);
               if(Dr > 0.01) continue;
               if(pfc_id->at(i) == 4) ecal_ += pfc_ecal->at(i);
               if(pfc_id->at(i) == 5) hcal_ += pfc_hcal->at(i);
            }
            if(Dr == 99.) continue;

            if(abs(eta_) < 1.5){
               if(ecal_ > 0 && hcal_ > 0) reso_eh_barrel->Fill((ecal_+hcal_-true_)/true_);
               if(ecal_ == 0 && hcal_ > 0) reso_h_barrel->Fill((hcal_-true_)/true_);
            }

            if(abs(eta_) > 1.5 && abs(eta_) < 3.0){
               if(ecal_ > 0 && hcal_ > 0) reso_eh_endcap->Fill((ecal_+hcal_-true_)/true_);
               if(ecal_ == 0 && hcal_ > 0) reso_h_endcap->Fill((hcal_-true_)/true_);
            }

            s->Fill();
            continue;
         }
         //pion
         for(int i = 0; i < pfc_charge->size(); i++){
            Dr = deltaR2(pfc_eta->at(i), true_eta->at(j), pfc_phi->at(i), true_phi->at(j));
            dR->Fill(Dr);
            if(Dr > 0.01) continue;
            eta_ = true_eta->at(j);
            phi_ = true_phi->at(j);
            true_ = true_energy->at(j);
            p_ = trackRef_p->at(i);
            ecal_ = pfc_ecal->at(i);
            hcal_ = pfc_hcal->at(i);

            if(abs(eta_) < 1.5){
               if(ecal_ > 0 && hcal_ > 0) reso_eh_barrel->Fill((ecal_+hcal_-true_)/true_);
               if(ecal_ == 0 && hcal_ > 0) reso_h_barrel->Fill((hcal_-true_)/true_);
            }

            if(abs(eta_) > 1.5 && abs(eta_) < 3.0){
               if(ecal_ > 0 && hcal_ > 0) reso_eh_endcap->Fill((ecal_+hcal_-true_)/true_);
               if(ecal_ == 0 && hcal_ > 0) reso_h_endcap->Fill((hcal_-true_)/true_);
            }  

            s->Fill(); 
         }
      }
   }

   dR->Write(); reso_eh_barrel->Write(); reso_h_barrel->Write(); reso_eh_endcap->Write(); reso_h_endcap->Write();
   s->Write();
   file->Close();
}
