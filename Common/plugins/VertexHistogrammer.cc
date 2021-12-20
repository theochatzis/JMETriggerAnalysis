#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include <memory>

#include <TH1D.h>

class VertexHistogrammer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit VertexHistogrammer(const edm::ParameterSet &);
  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void analyze(const edm::Event &, const edm::EventSetup &) override;

  const edm::InputTag vertices_tag_;
  const edm::EDGetTokenT<reco::VertexCollection> vertices_token_;

  TH1D *h_vertex_mult_ = nullptr;
  TH1D *h_vertex_x_ = nullptr;
  TH1D *h_vertex_y_ = nullptr;
  TH1D *h_vertex_z_ = nullptr;
  TH1D *h_vertex_normChi2_ = nullptr;
  TH1D *h_vertex_ndof_ = nullptr;
  TH1D *h_vertex_nTracks_ = nullptr;
  TH1D *h_vertex0_x_ = nullptr;
  TH1D *h_vertex0_y_ = nullptr;
  TH1D *h_vertex0_z_ = nullptr;
  TH1D *h_vertex0_normChi2_ = nullptr;
  TH1D *h_vertex0_ndof_ = nullptr;
  TH1D *h_vertex0_nTracks_ = nullptr;

  TH1D *h_track_pt_ = nullptr;
  TH1D *h_track_pt_2_ = nullptr;
  TH1D *h_track_eta_ = nullptr;
  TH1D *h_track_phi_ = nullptr;
  TH1D *h_track_dxy_ = nullptr;
  TH1D *h_track_dz_ = nullptr;
};

VertexHistogrammer::VertexHistogrammer(const edm::ParameterSet &iConfig)
    : vertices_tag_(iConfig.getParameter<edm::InputTag>("src")),
      vertices_token_(consumes<reco::VertexCollection>(vertices_tag_)) {
  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if (not fs) {
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  h_vertex_mult_ = fs->make<TH1D>("vertex_mult", "vertex_mult", 120, 0, 600);
  h_vertex_x_ = fs->make<TH1D>("vertex_x", "vertex_x", 600, -0.1, 0.1);
  h_vertex_y_ = fs->make<TH1D>("vertex_y", "vertex_y", 600, -0.1, 0.1);
  h_vertex_z_ = fs->make<TH1D>("vertex_z", "vertex_z", 600, -30, 30);
  h_vertex_normChi2_ = fs->make<TH1D>("vertex_normChi2", "vertex_normChi2", 600, 0, 12);
  h_vertex_ndof_ = fs->make<TH1D>("vertex_ndof", "vertex_ndof", 120, 0, 480);
  h_vertex_nTracks_ = fs->make<TH1D>("vertex_nTracks", "vertex_nTracks", 120, 0, 480);
  h_vertex0_x_ = fs->make<TH1D>("vertex0_x", "vertex0_x", 600, -0.1, 0.1);
  h_vertex0_y_ = fs->make<TH1D>("vertex0_y", "vertex0_y", 600, -0.1, 0.1);
  h_vertex0_z_ = fs->make<TH1D>("vertex0_z", "vertex0_z", 600, -30, 30);
  h_vertex0_normChi2_ = fs->make<TH1D>("vertex0_normChi2", "vertex0_normChi2", 600, 0, 12);
  h_vertex0_ndof_ = fs->make<TH1D>("vertex0_ndof", "vertex0_ndof", 120, 0, 480);
  h_vertex0_nTracks_ = fs->make<TH1D>("vertex0_nTracks", "vertex0_nTracks", 120, 0, 480);

  h_track_pt_ = fs->make<TH1D>("track_pt", "track_pt", 600, 0, 5.);
  h_track_pt_2_ = fs->make<TH1D>("track_pt_2", "track_pt_2", 600, 0, 600.);
  h_track_eta_ = fs->make<TH1D>("track_eta", "track_eta", 600, -5., 5.);
  h_track_phi_ = fs->make<TH1D>("track_phi", "track_phi", 600, -3., 3.);
  h_track_dxy_ = fs->make<TH1D>("track_dxy", "track_dxy", 600, -1., 1.);
  h_track_dz_ = fs->make<TH1D>("track_dz", "track_dz", 600, -1., 1.);
}

void VertexHistogrammer::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
  auto const &vertices(iEvent.getHandle(vertices_token_));

  if (vertices.isValid()) {
    h_vertex_mult_->Fill(vertices->size());

    for (uint idx = 0; idx < vertices->size(); ++idx) {
      auto const &vtx(vertices->at(idx));

      if (idx == 0) {
        h_vertex0_x_->Fill(vtx.x());
        h_vertex0_y_->Fill(vtx.y());
        h_vertex0_z_->Fill(vtx.z());
        h_vertex0_normChi2_->Fill(vtx.normalizedChi2());
        h_vertex0_ndof_->Fill(vtx.ndof());
        h_vertex0_nTracks_->Fill(vtx.nTracks());
      }

      h_vertex_x_->Fill(vtx.x());
      h_vertex_y_->Fill(vtx.y());
      h_vertex_z_->Fill(vtx.z());
      h_vertex_normChi2_->Fill(vtx.normalizedChi2());
      h_vertex_ndof_->Fill(vtx.ndof());
      h_vertex_nTracks_->Fill(vtx.nTracks());

      if (vtx.hasRefittedTracks()) {
        for (auto const &trk : vtx.refittedTracks()) {
          h_track_pt_->Fill(trk.pt());
          h_track_pt_2_->Fill(trk.pt());
          h_track_eta_->Fill(trk.eta());
          h_track_phi_->Fill(trk.phi());
          h_track_dxy_->Fill(trk.dxy(vtx.position()));
          h_track_dz_->Fill(trk.dz(vtx.position()));
        }
      } else {
        for (std::vector<reco::TrackBaseRef>::const_iterator trk_it = vtx.tracks_begin(); trk_it != vtx.tracks_end();
             ++trk_it) {
          auto const &trk_ref(*trk_it);
          h_track_pt_->Fill(trk_ref->pt());
          h_track_pt_2_->Fill(trk_ref->pt());
          h_track_eta_->Fill(trk_ref->eta());
          h_track_phi_->Fill(trk_ref->phi());
          h_track_dxy_->Fill(trk_ref->dxy(vtx.position()));
          h_track_dz_->Fill(trk_ref->dz(vtx.position()));
        }
      }
    }
  } else {
    edm::LogWarning("Input") << "invalid handle to reco::VertexCollection : " << vertices_tag_.encode();
  }
}

void VertexHistogrammer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of reco::VertexCollection");
  descriptions.add("VertexHistogrammer", desc);
}

DEFINE_FWK_MODULE(VertexHistogrammer);
