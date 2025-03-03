#include "FWCore/Framework/interface/MakerMacros.h"
#include "JetMETCorrections/Modules/interface/CorrectedJetProducer.h"
#include "DataFormats/JetReco/interface/PFClusterJet.h"

typedef reco::CorrectedJetProducer<reco::PFClusterJet> CorrectedPFClusterJetProducer;
DEFINE_FWK_MODULE(CorrectedPFClusterJetProducer);
