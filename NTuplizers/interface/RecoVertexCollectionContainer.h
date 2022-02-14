#ifndef JMETriggerAnalysis_RecoVertexCollectionContainer_h
#define JMETriggerAnalysis_RecoVertexCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VCollectionContainer.h>
#include <DataFormats/VertexReco/interface/Vertex.h>

class RecoVertexCollectionContainer : public VCollectionContainer<reco::Vertex> {
public:
  explicit RecoVertexCollectionContainer(const std::string&,
                                         const std::string&,
                                         const edm::EDGetToken&,
                                         const std::string& strCut = "");
  ~RecoVertexCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const reco::Vertex&) override;

  std::vector<uint>& vec_tracksSize() { return tracksSize_; }
  std::vector<bool>& vec_isFake() { return isFake_; }
  std::vector<float>& vec_chi2() { return chi2_; }
  std::vector<float>& vec_ndof() { return ndof_; }
  std::vector<float>& vec_x() { return x_; }
  std::vector<float>& vec_y() { return y_; }
  std::vector<float>& vec_z() { return z_; }
  std::vector<float>& vec_xError() { return xError_; }
  std::vector<float>& vec_yError() { return yError_; }
  std::vector<float>& vec_zError() { return zError_; }
  std::vector<float>& vec_t() { return t_; }
  std::vector<float>& vec_tError() { return tError_; }

protected:
  std::vector<uint> tracksSize_;
  std::vector<bool> isFake_;
  std::vector<float> chi2_;
  std::vector<float> ndof_;
  std::vector<float> x_;
  std::vector<float> y_;
  std::vector<float> z_;
  std::vector<float> xError_;
  std::vector<float> yError_;
  std::vector<float> zError_;
  std::vector<float> t_;
  std::vector<float> tError_;
};

#endif
