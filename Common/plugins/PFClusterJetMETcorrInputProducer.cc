#include "FWCore/Framework/interface/MakerMacros.h"
#include "JetMETCorrections/Type1MET/interface/JetCorrExtractorT.h"
#include "DataFormats/JetReco/interface/PFClusterJet.h"
#include "PFClusterJetMETcorrInputProducerT.h"

typedef PFClusterJetMETcorrInputProducerT<reco::PFClusterJet, JetCorrExtractorT<reco::PFClusterJet>>
    PFClusterJetMETcorrInputProducer;

DEFINE_FWK_MODULE(PFClusterJetMETcorrInputProducer);
