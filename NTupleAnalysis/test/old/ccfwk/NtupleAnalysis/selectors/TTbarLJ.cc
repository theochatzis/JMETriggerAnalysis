#include "TTbarLJ.h"

#include <iostream>

#include <inc/HFolderLepton.h>

void TTbarLJ::configure(){

  return;
}

void TTbarLJ::configure_output(TFile& of){

  book_HFolder<nak::HFolderLepton>(of, "input");

  return;
}

Bool_t TTbarLJ::Process(Long64_t entry){

  if(!SelectorBASE::Process(entry)) return kFALSE;

  const float& wgt = EVT.INFO->MCWeight;

  for(unsigned int i=0; i<EVT.MUO->size(); ++i)
    HFolder<nak::HFolderLepton>("input")->Fill(EVT.MUO->at(i), wgt);

  return kTRUE;
}
