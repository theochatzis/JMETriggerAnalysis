#include <inc/btagSF.h>

#include <inc/utils.h>

nak::btagSF::btagSF(const std::string& wp, const std::string& channel){//, const systematic& sys_){

  channel_ = channel;
//  sys = sys_;

  if(wp != "CSVM") util::KILL("btagSF(): undefined working point: "+wp);  
}

float nak::btagSF::GetWeight(const std::vector<xtt::Jet*>& jets){

  double weight(1.);

  if(&jets) return weight;

  return weight;
}

float nak::btagSF::GetWeight(const std::vector<xtt::Jet*>& jets, const std::vector<xtt::Jet*>& fat_jets){

  double weight(1.);

  if(&    jets) return weight;
  if(&fat_jets) return weight;

  return weight;
}
