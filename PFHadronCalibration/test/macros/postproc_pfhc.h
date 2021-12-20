//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Sep 17 04:42:14 2020 by ROOT version 6.20/07
// from TTree s/ PFCalibration
// found on file: /hdfs/store/user/pdas/MultiPion_PT0to200/crab_MultiPion_PT0to200_Winter20_16Sep/200916_213004/0000/PFHadCalibration_1.root
//////////////////////////////////////////////////////////

#ifndef postproc_pfhc_h
#define postproc_pfhc_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TLorentzVector.h>
#include <string>
#include <iostream>
#include <fstream>
#include <TMap.h>
#include <vector>
using namespace std;

class postproc_pfhc {
public:
  TTree *fChain;   //!pointer to the analyzed TTree or TChain
  Int_t fCurrent;  //!current Tree number in a TChain

  // Fixed size dimensions of array or collections stored in the TTree if any.

  // Declaration of leaf types
  vector<float> *true_energy;
  vector<float> *true_eta;
  vector<float> *true_phi;
  vector<float> *true_dr;
  vector<int> *true_charge;
  vector<float> *pfc_ecal;
  vector<float> *pfc_hcal;
  vector<float> *pfc_eta;
  vector<float> *pfc_phi;
  vector<int> *pfc_charge;
  vector<float> *pfc_id;
  vector<float> *pfc_trackRef_p;

  // List of branches
  TBranch *b_true_energy;     //!
  TBranch *b_true_eta;        //!
  TBranch *b_true_phi;        //!
  TBranch *b_true_dr;         //!
  TBranch *b_true_charge;     //!
  TBranch *b_pfc_ecal;        //!
  TBranch *b_pfc_hcal;        //!
  TBranch *b_pfc_eta;         //!
  TBranch *b_pfc_phi;         //!
  TBranch *b_pfc_charge;      //!
  TBranch *b_pfc_id;          //!
  TBranch *b_pfc_trackRef_p;  //!

  postproc_pfhc(const char *file1, const char *file2);
  virtual ~postproc_pfhc();
  virtual Int_t Cut(Long64_t entry);
  virtual Int_t GetEntry(Long64_t entry);
  virtual Long64_t LoadTree(Long64_t entry);
  virtual void Init(TTree *tree);
  virtual void Loop(const char *file2);
  virtual Bool_t Notify();
  virtual void Show(Long64_t entry = -1);
};

#endif

#ifdef postproc_pfhc_cxx
postproc_pfhc::postproc_pfhc(const char *file1, const char *file2) {
  TChain *chain = new TChain("Candidates");
  ifstream file;
  file.open(file1, ifstream::in);
  char filename[2000];
  while (true) {
    file >> filename;
    if (file.eof())
      break;
    chain->Add(filename);
    cout << "Added " << filename << endl;
  }  //loop over while

  Init(chain);
}

postproc_pfhc::~postproc_pfhc() {
  if (!fChain)
    return;
  delete fChain->GetCurrentFile();
}

Int_t postproc_pfhc::GetEntry(Long64_t entry) {
  // Read contents of entry.
  if (!fChain)
    return 0;
  return fChain->GetEntry(entry);
}
Long64_t postproc_pfhc::LoadTree(Long64_t entry) {
  // Set the environment to read one entry
  if (!fChain)
    return -5;
  Long64_t centry = fChain->LoadTree(entry);
  if (centry < 0)
    return centry;
  if (fChain->GetTreeNumber() != fCurrent) {
    fCurrent = fChain->GetTreeNumber();
    Notify();
  }
  return centry;
}

void postproc_pfhc::Init(TTree *tree) {
  // The Init() function is called when the selector needs to initialize
  // a new tree or chain. Typically here the branch addresses and branch
  // pointers of the tree will be set.
  // It is normally not necessary to make changes to the generated
  // code, but the routine can be extended by the user if needed.
  // Init() will be called many times when running on PROOF
  // (once per file to be processed).

  // Set object pointer
  true_energy = 0;
  true_eta = 0;
  true_phi = 0;
  true_dr = 0;
  true_charge = 0;
  pfc_ecal = 0;
  pfc_hcal = 0;
  pfc_eta = 0;
  pfc_phi = 0;
  pfc_charge = 0;
  pfc_id = 0;
  pfc_trackRef_p = 0;

  // Set branch addresses and branch pointers
  if (!tree)
    return;
  fChain = tree;
  fCurrent = -1;
  fChain->SetMakeClass(1);

  fChain->SetBranchAddress("true_energy", &true_energy, &b_true_energy);
  fChain->SetBranchAddress("true_eta", &true_eta, &b_true_eta);
  fChain->SetBranchAddress("true_phi", &true_phi, &b_true_phi);
  fChain->SetBranchAddress("true_dr", &true_dr, &b_true_dr);
  fChain->SetBranchAddress("true_charge", &true_charge, &b_true_charge);
  fChain->SetBranchAddress("pfc_ecal", &pfc_ecal, &b_pfc_ecal);
  fChain->SetBranchAddress("pfc_hcal", &pfc_hcal, &b_pfc_hcal);
  fChain->SetBranchAddress("pfc_eta", &pfc_eta, &b_pfc_eta);
  fChain->SetBranchAddress("pfc_phi", &pfc_phi, &b_pfc_phi);
  fChain->SetBranchAddress("pfc_charge", &pfc_charge, &b_pfc_charge);
  fChain->SetBranchAddress("pfc_id", &pfc_id, &b_pfc_id);
  fChain->SetBranchAddress("pfc_trackRef_p", &pfc_trackRef_p, &b_pfc_trackRef_p);

  Notify();
}

Bool_t postproc_pfhc::Notify() {
  // The Notify() function is called when a new file is opened. This
  // can be either for a new TTree in a TChain or when when a new TTree
  // is started when using PROOF. It is normally not necessary to make changes
  // to the generated code, but the routine can be extended by the
  // user if needed. The return value is currently not used.

  return kTRUE;
}

void postproc_pfhc::Show(Long64_t entry) {
  // Print contents of entry.
  // If entry is not specified, print current entry
  if (!fChain)
    return;
  fChain->Show(entry);
}
Int_t postproc_pfhc::Cut(Long64_t entry) {
  // This function may be called from Loop.
  // returns  1 if entry is accepted.
  // returns -1 otherwise.
  return 1;
}
#endif  // #ifdef postproc_pfhc_cxx
