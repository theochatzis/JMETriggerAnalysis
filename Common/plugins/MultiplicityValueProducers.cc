#include "JMETriggerAnalysis/Common/plugins/MultiplicityValueProducers.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Phase2TrackerCluster/interface/Phase2TrackerCluster1D.h"
#include "DataFormats/SiPixelCluster/interface/SiPixelCluster.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

typedef MultiplicityValueProducerFromNestedCollection<SiPixelClusterCollectionNew, double>
    SiPixelClusterMultiplicityValueProducer;
DEFINE_FWK_MODULE(SiPixelClusterMultiplicityValueProducer);

typedef MultiplicityValueProducerFromNestedCollection<Phase2TrackerCluster1DCollectionNew, double>
    SiPhase2TrackerClusterMultiplicityValueProducer;
DEFINE_FWK_MODULE(SiPhase2TrackerClusterMultiplicityValueProducer);

typedef MultiplicityValueProducer<reco::Track, double> TrackMultiplicityValueProducer;
DEFINE_FWK_MODULE(TrackMultiplicityValueProducer);

typedef MultiplicityValueProducer<reco::Vertex, double> VertexMultiplicityValueProducer;
DEFINE_FWK_MODULE(VertexMultiplicityValueProducer);
