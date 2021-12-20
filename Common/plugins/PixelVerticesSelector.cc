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
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "RecoPixelVertexing/PixelVertexFinding/interface/PVClusterComparer.h"

//#include <iostream>
//#define LogTrace(X) std::cout << std::endl

class PixelVerticesSelector : public edm::stream::EDProducer<> {
public:
  explicit PixelVerticesSelector(const edm::ParameterSet&);
  ~PixelVerticesSelector() override {}

  static void fillDescriptions(edm::ConfigurationDescriptions&);

protected:
  void produce(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<edm::View<reco::Vertex>> token_src_;

  const double minSumPt2_;
  const double minSumPt2FractionWrtMax_;
  const edm::ParameterSet ranker_pset_;

  std::unique_ptr<PVClusterComparer> pvComparer_;

  const int maxNVertices_;

  struct indexAndFOM {
    indexAndFOM(const size_t idx, const double foo) : index(idx), fom(foo) {}

    size_t index;
    double fom;
  };
};

PixelVerticesSelector::PixelVerticesSelector(const edm::ParameterSet& iConfig)
    : token_src_(consumes<edm::View<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("src"))),
      minSumPt2_(iConfig.getParameter<double>("minSumPt2")),
      minSumPt2FractionWrtMax_(iConfig.getParameter<double>("minSumPt2FractionWrtMax")),
      ranker_pset_(iConfig.getParameter<edm::ParameterSet>("ranker")),
      maxNVertices_(iConfig.getParameter<int>("maxNVertices")) {
  if (minSumPt2FractionWrtMax_ >= 1.) {
    throw cms::Exception("Input") << "invalid (>= 1.0) value for configuration parameter \"minSumPt2FractionWrtMax\": "
                                  << minSumPt2FractionWrtMax_;
  }

  const double track_pt_min = ranker_pset_.getParameter<double>("track_pt_min");
  const double track_pt_max = ranker_pset_.getParameter<double>("track_pt_max");
  const double track_chi2_max = ranker_pset_.getParameter<double>("track_chi2_max");
  const double track_prob_min = ranker_pset_.getParameter<double>("track_prob_min");

  pvComparer_.reset(new PVClusterComparer(track_pt_min, track_pt_max, track_chi2_max, track_prob_min));

  produces<reco::VertexCollection>();
}

void PixelVerticesSelector::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto const& vertices(iEvent.getHandle(token_src_));

  if (not vertices.isValid()) {
    edm::LogWarning("Input") << "invalid handle for input collection of vertices";
    return;
  }

  std::vector<PixelVerticesSelector::indexAndFOM> vec_indexAndFOM;
  vec_indexAndFOM.reserve(vertices->size());

  for (uint idx = 0; idx < vertices->size(); ++idx) {
    vec_indexAndFOM.emplace_back(PixelVerticesSelector::indexAndFOM(idx, pvComparer_->pTSquaredSum(vertices->at(idx))));

    LogTrace("") << "[PixelVerticesSelector::produce] "
                 << "input vertex #" << vec_indexAndFOM.back().index << ": z=" << vertices->at(idx).z()
                 << ", pTSquaredSum=" << vec_indexAndFOM.back().fom;
  }

  std::sort(vec_indexAndFOM.begin(),
            vec_indexAndFOM.end(),
            [](const PixelVerticesSelector::indexAndFOM& foo1, const PixelVerticesSelector::indexAndFOM& foo2) {
              return (foo1.fom > foo2.fom);
            });

  const double max_sumPt2((!vec_indexAndFOM.empty()) ? vec_indexAndFOM.at(0).fom : -1.);

  const double minSumPt2_rel(minSumPt2FractionWrtMax_ * max_sumPt2);

  auto out_vertices = std::make_unique<reco::VertexCollection>();
  out_vertices->reserve((maxNVertices_ >= 0) ? maxNVertices_ : vertices->size());

  for (auto const& idxNfom : vec_indexAndFOM) {
    if ((maxNVertices_ >= 0) && (out_vertices->size() >= ((uint)maxNVertices_))) {
      break;
    }

    if ((idxNfom.fom > minSumPt2_) && ((idxNfom.fom > minSumPt2_rel) || (minSumPt2FractionWrtMax_ < 0.))) {
      LogTrace("") << "[PixelVerticesSelector::produce] "
                   << "output vertex #" << out_vertices->size() << ": z=" << vertices->at(idxNfom.index).z()
                   << ", pTSquaredSum=" << idxNfom.fom << " (input index=" << idxNfom.index << ")";

      out_vertices->emplace_back(vertices->at(idxNfom.index));
    }
  }

  LogTrace("") << "[PixelVerticesSelector::produce] "
               << "output collection contains " << out_vertices->size() << " vertices (input: " << vertices->size()
               << " vertices)";

  iEvent.put(std::move(out_vertices));
}

void PixelVerticesSelector::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag(""))->setComment("input collection (pixel vertices)");
  desc.add<double>("minSumPt2", 0.)->setComment("minimum sumPt2");
  desc.add<double>("minSumPt2FractionWrtMax", 0.3)
      ->setComment("minimum sumPt2 fraction relative to the highest sumPt2 (for sumPt2 calculation, see ranker)");

  edm::ParameterSetDescription rankerPSet;
  rankerPSet.add<double>("track_pt_min", 1.)->setComment("minimum track pT");
  rankerPSet.add<double>("track_pt_max", 20.)->setComment("maximum track pT");
  rankerPSet.add<double>("track_chi2_max", 20.)->setComment("maximum track chi2");
  rankerPSet.add<double>("track_prob_min", -1.)->setComment("minimum track probability");
  desc.add<edm::ParameterSetDescription>("ranker", rankerPSet)
      ->setComment("parameters of PVClusterComparer to select tracks used in sumPt2 calculation");

  desc.add<int>("maxNVertices", -1)
      ->setComment("maximum number of vertices in output collection (if negative, no limit is applied)");

  descriptions.add("pixelVerticesSelector", desc);
}

DEFINE_FWK_MODULE(PixelVerticesSelector);
