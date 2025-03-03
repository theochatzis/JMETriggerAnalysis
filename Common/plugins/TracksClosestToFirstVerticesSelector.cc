#include <memory>
#include <utility>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

class TracksClosestToFirstVerticesSelector : public edm::stream::EDProducer<> {
public:
  explicit TracksClosestToFirstVerticesSelector(const edm::ParameterSet&);
  ~TracksClosestToFirstVerticesSelector() override {}

  static void fillDescriptions(edm::ConfigurationDescriptions&);

protected:
  void produce(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetToken token_tracks_;
  edm::EDGetToken token_vertices_;

  const int maxNVertices_;
  const double maxDeltaZ_;
};

TracksClosestToFirstVerticesSelector::TracksClosestToFirstVerticesSelector(const edm::ParameterSet& iConfig)
    : token_tracks_(consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("tracks"))),
      token_vertices_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertices"))),
      maxNVertices_(iConfig.getParameter<int>("maxNVertices")),
      maxDeltaZ_(iConfig.getParameter<double>("maxDeltaZ")) {
  produces<reco::TrackCollection>();
}

void TracksClosestToFirstVerticesSelector::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto out_tracks = std::make_unique<reco::TrackCollection>();

  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByToken(token_tracks_, tracks);

  if (not tracks.isValid()) {
    edm::LogWarning("Input") << "invalid handle for input collection of tracks";
    return;
  }

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(token_vertices_, vertices);

  if (not vertices.isValid()) {
    edm::LogWarning("Input") << "invalid handle for input collection of vertices";
    return;
  }

  LogDebug("Input") << "size of input collections: " << tracks->size() << " tracks, " << vertices->size()
                    << " vertices";

  if (!vertices->empty()) {
    for (const auto& track : *tracks) {
      double trkVtx_minDz(-1.);
      int trkVtx_minDz_vtxIdx(-1);

      for (uint vtx_idx = 0; vtx_idx < vertices->size(); ++vtx_idx) {
        const double dz(std::abs(track.vz() - vertices->at(vtx_idx).z()));

        if ((dz < trkVtx_minDz) or (vtx_idx == 0)) {
          trkVtx_minDz = dz;
          trkVtx_minDz_vtxIdx = vtx_idx;
        }
      }

      LogDebug("Output") << "track-vertex association: track.vz=" << track.vz()
                         << ", min(abs(track.vz - vertex.z))=" << trkVtx_minDz
                         << ", vertex-index=" << trkVtx_minDz_vtxIdx
                         << ", passes-maxNVertices=" << ((trkVtx_minDz_vtxIdx < maxNVertices_) or (maxNVertices_ < 0))
                         << ", passes-maxDeltaZ=" << ((trkVtx_minDz < maxDeltaZ_) or (maxDeltaZ_ < 0));

      if ((trkVtx_minDz_vtxIdx < maxNVertices_) or (maxNVertices_ < 0)) {
        if ((trkVtx_minDz < maxDeltaZ_) or (maxDeltaZ_ < 0)) {
          out_tracks->emplace_back(track);
        }
      }
    }
  }

  LogDebug("Output") << "output collection contains " << out_tracks->size() << " tracks (input: " << tracks->size()
                     << " tracks)";

  iEvent.put(std::move(out_tracks));
}

void TracksClosestToFirstVerticesSelector::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("tracks", edm::InputTag(""))->setComment("input collection of tracks");
  desc.add<edm::InputTag>("vertices", edm::InputTag(""))
      ->setComment("input collection of vertices (if empty, no tracks will be retained)");
  desc.add<int>("maxNVertices", -1)
      ->setComment(
          "retain only tracks associated to one of the first N vertices (if negative, all vertices are considered)");
  desc.add<double>("maxDeltaZ", -1.)
      ->setComment(
          "maximum (absolute) delta-Z distance between track.vz and vertex.z for track-vertex matching (if negative, "
          "criterion is not applied");

  descriptions.add("TracksClosestToFirstVerticesSelector", desc);
}

DEFINE_FWK_MODULE(TracksClosestToFirstVerticesSelector);
