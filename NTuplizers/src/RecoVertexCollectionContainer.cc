#include <JMETriggerAnalysis/NTuplizers/interface/RecoVertexCollectionContainer.h>

RecoVertexCollectionContainer::RecoVertexCollectionContainer(const std::string& name,
                                                             const std::string& inputTagLabel,
                                                             const edm::EDGetToken& token,
                                                             const std::string& strCut)
    : VCollectionContainer(name, inputTagLabel, token, strCut) {}

void RecoVertexCollectionContainer::clear() {
  tracksSize_.clear();
  isFake_.clear();
  chi2_.clear();
  ndof_.clear();
  x_.clear();
  y_.clear();
  z_.clear();
  xError_.clear();
  yError_.clear();
  zError_.clear();
}

void RecoVertexCollectionContainer::reserve(const size_t vec_size) {
  tracksSize_.reserve(vec_size);
  isFake_.reserve(vec_size);
  chi2_.reserve(vec_size);
  ndof_.reserve(vec_size);
  x_.reserve(vec_size);
  y_.reserve(vec_size);
  z_.reserve(vec_size);
  xError_.reserve(vec_size);
  yError_.reserve(vec_size);
  zError_.reserve(vec_size);
}

void RecoVertexCollectionContainer::emplace_back(const reco::Vertex& obj) {
  tracksSize_.emplace_back(obj.tracksSize());
  isFake_.emplace_back(obj.isFake());
  chi2_.emplace_back(obj.chi2());
  ndof_.emplace_back(obj.ndof());
  x_.emplace_back(obj.x());
  y_.emplace_back(obj.y());
  z_.emplace_back(obj.z());
  xError_.emplace_back(obj.xError());
  yError_.emplace_back(obj.yError());
  zError_.emplace_back(obj.zError());
}
