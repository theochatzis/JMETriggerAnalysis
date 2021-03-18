#include "SelectorBASE.h"

#include <iostream>
#include <string>
#include <vector>
#include <cmath>

#include <TObject.h>

#include <inc/utils.h>

SelectorBASE::SelectorBASE(): fChain(0) {

  fFile = 0;
  fFilePROOF = 0;

  max_evtN_ = -1;
  PROOF_wrkN_ = 0;
  output_file_ = "";

  return;
}

void SelectorBASE::Init(TTree *tree){

  if(!tree) return;
  fChain = tree;

  init_branch("EVT"     , &EVT.INFO);
  init_branch("GENP"    , &EVT.GENP);
  init_branch("HLT"     , &EVT.HLT);
  init_branch("PVTX"    , &EVT.PVTX);
  init_branch("MUO"     , &EVT.MUO);
  init_branch("ELE"     , &EVT.ELE);
  init_branch("JET_AK4" , &EVT.JET_AK4);
  init_branch("JET_AK8" , &EVT.JET_AK8);
  init_branch("JET_CA15", &EVT.JET_CA15);
  init_branch("MET"     , &EVT.MET);

  return;
}

void SelectorBASE::init_branch(const char* bname, void* obj_addr, const bool auto_delete){

  if(!fChain) return;

  fChain->SetBranchAddress(bname, obj_addr);
  fChain->GetBranch(bname)->SetAutoDelete(auto_delete);

  return;
}

void SelectorBASE::Begin(TTree*){

  return;
}

void SelectorBASE::SlaveBegin(TTree*){

  std::string options = GetOption();

  const std::string max_evtN_str(util::get_option_from_string(options, "n"));
  if(max_evtN_str != "") max_evtN_ = atol(max_evtN_str.c_str());

  const std::string PROOF_wrkN_str(util::get_option_from_string(options, "w"));
  if(PROOF_wrkN_str != "") PROOF_wrkN_ = atoi(PROOF_wrkN_str.c_str());

  output_file_ = util::get_option_from_string(options, "output");

  configure();

  if(output_file_ != ""){

    if(PROOF_wrkN_ > 0){

      std::string tmp_ofname(output_file_.substr(0, output_file_.find(".root")));
      tmp_ofname += "-temp.root";

      fFilePROOF = new TProofOutputFile(tmp_ofname.c_str(), "ML");
      fFilePROOF->SetOutputFileName(output_file_.c_str());

      TDirectory* savedir = gDirectory;

      fFile = fFilePROOF->OpenFile("RECREATE");
      if(fFile && fFile->IsZombie()) SafeDelete(fFile);

      savedir->cd();
    }
    else fFile = new TFile(output_file_.c_str(), "recreate");

    if(fFile) configure_output(*fFile);
  }

  return;
}

Bool_t SelectorBASE::Process(Long64_t entry){

  if((max_evtN_ != -1) && (entry >= max_evtN_)) return kFALSE;

  GetEntry(entry);

  if(!(PROOF_wrkN_ > 0)){

    if(max_evtN_ != -1) printout_event_pct(entry+1, max_evtN_);
    else                printout_event_pct(entry+1, fChain->GetEntries());
  }

  return kTRUE;
}

void SelectorBASE::SlaveTerminate(){

  if(fFile){

    TDirectory* savedir = gDirectory;
    fFile->cd();

    for(unsigned int k=0; k<key_v.size(); ++k){

      const std::string& key = key_v.at(k);
      if(hfolder_.find(key) != hfolder_.end()) hfolder_[key]->Write();
    }

    gDirectory = savedir;
    fFile->Close();

    if(PROOF_wrkN_ > 0){

      fFilePROOF->Print();
      fOutput->Add(fFilePROOF);
    }
    else fOutput->Add(fFile);

    clear_hfolder_map();

    EVT.Delete();
  }

  return;
}

void SelectorBASE::Terminate(){

//  std::vector<std::string> obj_vec;
//  obj_vec.push_back("PROOF_Status");
//  obj_vec.push_back("PROOF_TOutputListSelectorDataMap_object");
//  for(unsigned int i=0; i<obj_vec.size(); ++i){
//
//    TObject* obj = fOutput->FindObject(obj_vec.at(i).c_str());
//    if(obj) fOutput->Remove(obj);
//  }

  return;
}

void SelectorBASE::printout_event_pct(const long int ient, const long int nent){

  if(!(int((ient/float(nent))*1000) % 10)){

    std::cout << "\r -- completed :";
    std::cout << " " << int((ient/float(nent))*1000.)/10. << "%";
    std::cout << " (" << ient << " / " << nent << ")   ";
  }

  if(ient == nent) std::cout << std::endl;

  return;
}

void SelectorBASE::clear_hfolder_map(){

  for(hfolder_itr ihf=hfolder_.begin(); ihf != hfolder_.end(); ++ihf){

    if(ihf->second) delete ihf->second;
    ihf->second = 0;
  }

  return;
}
