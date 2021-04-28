#include "HLTrigger/JetMET/plugins/HLTMultiplicityValueProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

typedef HLTMultiplicityValueProducer<reco::Track, double> HLTTrackMultiplicityValueProducer;
DEFINE_FWK_MODULE(HLTTrackMultiplicityValueProducer);

typedef HLTMultiplicityValueProducer<reco::Vertex, double> HLTVertexMultiplicityValueProducer;
DEFINE_FWK_MODULE(HLTVertexMultiplicityValueProducer);
