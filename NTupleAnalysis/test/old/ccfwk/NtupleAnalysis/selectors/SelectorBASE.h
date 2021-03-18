#ifndef NAK_SelectorBASE_H
#define NAK_SelectorBASE_H

#include <string>
#include <vector>

#include <TSelector.h>
#include <TChain.h>
#include <TFile.h>
#include <TProofOutputFile.h>
#include <TString.h>

#include <inc/Event.h>
#include <inc/HFolderBASE.h>
#include <inc/utils.h>

class SelectorBASE : public TSelector {
 protected:
  nak::Event EVT; //!

  void initialize();
  void printout_event_pct(const long int, const long int);

  TFile* fFile;
  TProofOutputFile* fFilePROOF;

  virtual void configure() = 0;
  virtual void configure_output(TFile&) = 0;

  void init_branch(const char*, void*, const bool auto_delete=1);

  long int max_evtN_;
  int PROOF_wrkN_;
  std::string output_file_;

  std::vector<std::string> key_v;

  std::map<std::string, nak::HFolderBASE*> hfolder_;
  typedef std::map<std::string, nak::HFolderBASE*>::iterator hfolder_itr;

  template<typename F> F* HFolder(const std::string&);
  template<typename F> void book_HFolder(TFile&, const std::string& dir="");

  void clear_hfolder_map();

  void KILL(const std::string& log){ Abort(log.c_str()); }
  void KILL(const TString& log){ Abort(log.Data()); }

 public:
  TTree* fChain; //!

  SelectorBASE();
  virtual ~SelectorBASE() {}

  virtual void Init(TTree *tree);

  virtual void   Begin(TTree*);
  virtual void   SlaveBegin(TTree*);
  virtual Bool_t Process(Long64_t entry);
  virtual void   SlaveTerminate();
  virtual void   Terminate();

  virtual Int_t  GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }

  virtual Int_t  Version() const { return 2; }
  virtual Bool_t Notify(){ return kTRUE; }
  virtual void   SetOption(const char *option){ fOption = option; }
  virtual void   SetObject(TObject *obj){ fObject = obj; }
  virtual void   SetInputList(TList *input){ fInput = input; }
  virtual TList* GetOutputList() const { return fOutput; }

  ClassDef(SelectorBASE, 0);
};

template<typename F>
void SelectorBASE::book_HFolder(TFile& file, const std::string& dname_){

  if(hfolder_.find(dname_) != hfolder_.end()) util::KILL("SelectorBASE::book_HFolder -- already existing folder key: "+dname_);
  else {

    hfolder_[dname_] = new F(file, dname_);
    key_v.push_back(dname_);
  }

  return;
}

template<typename F>
F* SelectorBASE::HFolder(const std::string& key_){

  F* f(0);

  if(hfolder_.find(key_) != hfolder_.end()) f = static_cast<F*>(hfolder_[key_]);
  else util::KILL("SelectorBASE::HFolder -- folder key not found: "+key_);

  if(!f) util::KILL("SelectorBASE::HFolder -- null pointer to folder: "+key_);

  return f;
}

#endif
