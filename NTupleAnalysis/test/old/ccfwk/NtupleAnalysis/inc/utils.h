#ifndef UTIL_Utils_H
#define UTIL_Utils_H

#include <string>
#include <vector>
#include <limits>

#include <NtupleObjects/inc/EventInfo.h>
#include <NtupleObjects/inc/GenParticle.h>
#include <NtupleObjects/inc/HLT.h>
#include <NtupleObjects/inc/PVertex.h>
#include <NtupleObjects/inc/Lepton.h>
#include <NtupleObjects/inc/Jet.h>
#include <NtupleObjects/inc/MergedJet.h>
#include <NtupleObjects/inc/MET.h>

#include <TLorentzVector.h>

//!!enum systematic {NO, UP, DN};

namespace util {

  void KILL(const std::string&);
  void WARNING(const std::string&);

  std::string int_to_str(int);
  bool int_le_ge(int, int, int);

  float f_infty();

  std::vector<std::string> string_tokens(const std::string&, const std::string&);
  std::string get_option_from_string(const std::string&, const std::string&);

  void boost_x1_to_x2CM( TLorentzVector&, const TLorentzVector&);
  float cosThetaX (const TLorentzVector&, const TLorentzVector&, const TLorentzVector&);
  float cosThetaCS(const TLorentzVector&, const TLorentzVector&);

}

template<typename P>
inline std::vector<P> to_vector_of_objs(const std::vector<const P*>& vec_ptrs_){

  std::vector<P> vec;
  vec.reserve(vec_ptrs_.size());
  for(unsigned int i=0; i<vec_ptrs_.size(); ++i){
    if(!vec_ptrs_.at(i)) vec.push_back(*vec_ptrs_.at(i));
  }

  return vec;
}

// geometrical functions
template<typename P>
inline const P* jet_closest_by_DR(const xtt::Particle& p1_, const std::vector<P>& p2s_){

  const P* np(0);

  float minDR(-1);
  for(unsigned int i=0; i<p2s_.size(); ++i){

    float dr(p1_.p4().DeltaR(p2s_.at(i).p4()));
    if(!i || dr < minDR){ minDR = dr; np = &(p2s_.at(i)); }
  }

  if(!np) util::KILL("jet_closest_by_DR() -- jet closest-by-DeltaR not found");
  return np;
}

template<typename P>
inline float dRmin(const xtt::Particle& p1_, const std::vector<P>& p2s_){

  const P* p2_closestDR(jet_closest_by_DR(p1_, p2s_));
  return float(p1_.p4().DeltaR(p2_closestDR->p4()));
}

template<typename A, typename B>
inline float pTrel(const A& p1_, const B& p2_){

  return float(p1_.p4().P() * sin(p1_.p4().Angle(p2_.p4().Vect())));
}

template<typename P>
inline float pTrel_dRmin(const xtt::Particle& p1_, const std::vector<P>& p2s_){

  const P* p2_closestDR(jet_closest_by_DR(p1_, p2s_));
  return float(pTrel(p1_, *p2_closestDR));
}

template<typename P>
struct higher_pt {
  bool operator()(const P& p1, const P& p2) const { return (p1.pt > p2.pt); }
};

template<typename P>
inline void sort_by_pt(std::vector<P>& particles){

  std::sort(particles.begin(), particles.end(), higher_pt<P>());

  return;
}

// analysis-specific selections
bool lepton_2Dcut(const xtt::Particle&, const std::vector<xtt::Jet>&);
bool triangular_cut(const xtt::MET&, const xtt::Particle&);

bool topjet_tag(const xtt::MergedJet&);
float topjet_mmin(const xtt::MergedJet&);
float topjet_minDRsubjets(const xtt::MergedJet&);
float topjet_max_subjet_btag(const std::string&, const xtt::MergedJet&);
std::vector<xtt::MergedJet> get_toptag_jets(const std::vector<xtt::MergedJet>&);

#endif
