#include <inc/EventSelection.h>

bool nak::VTagEvent::pass(const nak::Event& evt){

  std::vector<xtt::MergedJet>* VJETS = (std::vector<xtt::MergedJet>*) evt.get(vjet_key_);
  std::vector<xtt::Jet>* JETS = (std::vector<xtt::Jet>*) evt.get(jet_key_);

  for(unsigned int v=0; v<VJETS->size(); ++v){

    if(!(*vtagID_)(VJETS->at(v))) continue;

    int jetN(0);
    for(unsigned int j=0; j<JETS->size(); ++j){

      if(JETS->at(j).p4().DeltaR(VJETS->at(v).p4()) > minDR_vtag_jet_) ++jetN;

      if(jetN >= 2) return true;
    }
  }

  return false;
}

bool nak::TopTagEvent::pass(const nak::Event& evt){

  std::vector<xtt::MergedJet>* TOPJETS = (std::vector<xtt::MergedJet>*) evt.get(topjet_key_);
  std::vector<xtt::Jet>* JETS = (std::vector<xtt::Jet>*) evt.get(jet_key_);

  for(unsigned int t=0; t<TOPJETS->size(); ++t){

    if(!(*ttagID_)(TOPJETS->at(t))) continue;

    int jetN(0);
    for(unsigned int j=0; j<JETS->size(); ++j){

      if(JETS->at(j).p4().DeltaR(TOPJETS->at(t).p4()) > minDR_ttag_jet_) ++jetN;

      if(jetN >= 1) return true;
    }
  }

  return false;
}
