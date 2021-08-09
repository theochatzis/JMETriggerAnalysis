#include "HLTrigger/JetMET/plugins/HLTMultiplicityValueProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

typedef HLTMultiplicityValueProducer<reco::Track, double> TrackMultiplicityValueProducer;
DEFINE_FWK_MODULE(TrackMultiplicityValueProducer);

typedef HLTMultiplicityValueProducer<reco::Vertex, double> VertexMultiplicityValueProducer;
DEFINE_FWK_MODULE(VertexMultiplicityValueProducer);
