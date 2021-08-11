#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ nestedclass;

// user classes

#pragma link C++ class xtt::EventInfo+;
#pragma link C++ class xtt::Particle+;
#pragma link C++ class xtt::GenParticle+;
#pragma link C++ class xtt::HLT+;
#pragma link C++ class xtt::PVertex+;
#pragma link C++ class xtt::Lepton+;
#pragma link C++ class xtt::Muon+;
#pragma link C++ class xtt::Electron+;
#pragma link C++ class xtt::Jet+;
#pragma link C++ class xtt::MergedJet+;
#pragma link C++ class xtt::MET+;

#pragma link C++ class std::vector<xtt::EventInfo>+;
#pragma link C++ class std::vector<xtt::Particle>+;
#pragma link C++ class std::vector<xtt::GenParticle>+;
#pragma link C++ class std::vector<xtt::HLT>+;
#pragma link C++ class std::vector<xtt::PVertex>+;
#pragma link C++ class std::vector<xtt::Lepton>+;
#pragma link C++ class std::vector<xtt::Muon>+;
#pragma link C++ class std::vector<xtt::Electron>+;
#pragma link C++ class std::vector<xtt::Jet>+;
#pragma link C++ class std::vector<xtt::MergedJet>+;
#pragma link C++ class std::vector<xtt::MET>+;

#endif
