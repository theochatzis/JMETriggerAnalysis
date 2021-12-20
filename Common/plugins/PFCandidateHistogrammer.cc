#include "JMETriggerAnalysis/Common/plugins/PFCandidateHistogrammer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

typedef PFCandidateHistogrammer<reco::PFCandidate> RecoPFCandidateHistogrammer;
DEFINE_FWK_MODULE(RecoPFCandidateHistogrammer);

typedef PFCandidateHistogrammer<pat::PackedCandidate> PATPackedCandidateHistogrammer;
DEFINE_FWK_MODULE(PATPackedCandidateHistogrammer);
