#ifndef NAK_Event_H
#define NAK_Event_H

#include <NtupleObjects/inc/EventInfo.h>
#include <NtupleObjects/inc/GenParticle.h>
#include <NtupleObjects/inc/HLT.h>
#include <NtupleObjects/inc/PVertex.h>
#include <NtupleObjects/inc/Muon.h>
#include <NtupleObjects/inc/Electron.h>
#include <NtupleObjects/inc/Jet.h>
#include <NtupleObjects/inc/MergedJet.h>
#include <NtupleObjects/inc/MET.h>

#include <inc/utils.h>

#include <string>
#include <vector>

namespace nak {

  class Event {

   public:
    explicit Event();
    virtual ~Event() {}

    xtt::EventInfo* INFO;
    std::vector<xtt::GenParticle>* GENP;
    xtt::HLT* HLT;
    xtt::PVertex* PVTX;
    std::vector<xtt::Muon>* MUO;
    std::vector<xtt::Electron>* ELE;
    std::vector<xtt::Jet>* JET_AK4;
    std::vector<xtt::MergedJet>* JET_AK8;
    std::vector<xtt::MergedJet>* JET_CA15;
    xtt::MET* MET;

    // methods
    void* get(const std::string&) const;

    void Delete();

    template<typename C> void clean_kin(const std::string&, const float, const float);
  };

}

template<typename C>
void nak::Event::clean_kin(const std::string& key, const float min_pt_, const float max_eta_){

  std::vector<C>* coll = (std::vector<C>*) get(key);

  std::vector<C> coll_new;
  for(unsigned int i=0; i<coll->size(); ++i){

    const C& obj = coll->at(i);

    if(!(obj.pt > min_pt_)) continue;
    if(!(fabs(obj.eta) < max_eta_)) continue;

    coll_new.push_back(obj);
  }

  coll->clear();
  coll->reserve(coll_new.size());
  for(unsigned int i=0; i<coll_new.size(); ++i) coll->push_back(coll_new.at(i));

  sort_by_pt(*coll);

  return;
}

#endif
