#include <FWCore/Framework/interface/MakerMacros.h>
#include <JMETriggerAnalysis/Common/plugins/FwdPtrConverter.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>

typedef FwdPtrConverter<reco::PFCandidate> FwdPtrRecoPFCandidateConverter;
DEFINE_FWK_MODULE(FwdPtrRecoPFCandidateConverter);
