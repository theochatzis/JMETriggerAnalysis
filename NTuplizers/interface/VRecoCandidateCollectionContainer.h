#ifndef JMETriggerAnalysis_VRecoCandidateCollectionContainer_h
#define JMETriggerAnalysis_VRecoCandidateCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VCollectionContainer.h>

#include <numeric>
#include <algorithm>

template <class T>
class VRecoCandidateCollectionContainer : public VCollectionContainer<T> {
public:
  explicit VRecoCandidateCollectionContainer(const std::string&,
                                             const std::string&,
                                             const edm::EDGetToken&,
                                             const std::string& strCut = "",
                                             const bool orderByHighestPt = false);
  virtual ~VRecoCandidateCollectionContainer() {}

  virtual void fill(const std::vector<T>&, const bool clear_before_filling = true);

  virtual void clear() = 0;
  virtual void reserve(const size_t) = 0;
  virtual void emplace_back(const T&) = 0;

  void orderByHighestPt(const bool foo) { orderByHighestPt_ = foo; }
  int  &getCollectionSize() {  return jetCollectionSize_; }

protected:
  // ordering
  std::vector<size_t> idxs_;  // vector of indeces (used for ordering)
  bool orderByHighestPt_;     // order objects by decreasing pT values
  // this is the size of the collection - used for multiplicity of objects
  int jetCollectionSize_;     
};

template <class T>
VRecoCandidateCollectionContainer<T>::VRecoCandidateCollectionContainer(const std::string& name,
                                                                        const std::string& inputTagLabel,
                                                                        const edm::EDGetToken& token,
                                                                        const std::string& strCut,
                                                                        const bool orderByHighestPt)
    : VCollectionContainer<T>(name, inputTagLabel, token, strCut), orderByHighestPt_(orderByHighestPt) {
  idxs_.clear();
}

template <class T>
void VRecoCandidateCollectionContainer<T>::fill(const std::vector<T>& coll, const bool clear_before_filling) {
  if (clear_before_filling) {
    this->clear();
  }
  
  jetCollectionSize_ = coll.size();
  
  this->reserve(coll.size());

  if (orderByHighestPt_) {
    idxs_.clear();
    idxs_.reserve(coll.size());

    // initialize indeces
    for (uint idx = 0; idx < coll.size(); ++idx) {
      idxs_.emplace_back(idx);
    }

    // sort indeces based on pt-ordering
    std::sort(idxs_.begin(), idxs_.end(), [&coll](const size_t& i1, const size_t& i2) {
      return coll.at(i1).pt() > coll.at(i2).pt();
    });
  }

  for (uint idx = 0; idx < coll.size(); ++idx) {
    const auto& i_obj = coll.at(orderByHighestPt_ ? idxs_.at(idx) : idx);

    if (not this->stringCutObjectSelector_(i_obj)) {
      continue;
    }

    this->emplace_back(i_obj);
  }
}

#endif
