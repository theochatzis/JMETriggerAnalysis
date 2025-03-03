#ifndef JMETriggerAnalysis_VCollectionContainer_h
#define JMETriggerAnalysis_VCollectionContainer_h

#include <FWCore/Utilities/interface/EDGetToken.h>
#include <CommonTools/Utils/interface/StringCutObjectSelector.h>

#include <string>
#include <vector>

template <class T>
class VCollectionContainer {
public:
  explicit VCollectionContainer(const std::string&,
                                const std::string&,
                                const edm::EDGetToken&,
                                const std::string& strCut = "");
  virtual ~VCollectionContainer() {}

  virtual void fill(const std::vector<T>&, const bool clear_before_filling = true);

  virtual void clear() = 0;
  virtual void reserve(const size_t) = 0;
  virtual void emplace_back(const T&) = 0;

  void setStringCutObjectSelector(const std::string&);

  void setName(const std::string& str) { name_ = str; }

  const std::string& name() const { return name_; }
  const std::string& inputTagLabel() const { return inputTagLabel_; }
  const edm::EDGetToken& token() const { return token_; }

protected:
  std::string name_;
  const std::string inputTagLabel_;
  const edm::EDGetToken token_;

  StringCutObjectSelector<T, true> stringCutObjectSelector_;
};

template <class T>
VCollectionContainer<T>::VCollectionContainer(const std::string& name,
                                              const std::string& inputTagLabel,
                                              const edm::EDGetToken& token,
                                              const std::string& strCut)
    : name_(name), inputTagLabel_(inputTagLabel), token_(token), stringCutObjectSelector_(strCut) {}

template <class T>
void VCollectionContainer<T>::setStringCutObjectSelector(const std::string& strCut) {
  stringCutObjectSelector_ = StringCutObjectSelector<T, true>(strCut);
}

template <class T>
void VCollectionContainer<T>::fill(const std::vector<T>& coll, const bool clear_before_filling) {
  if (clear_before_filling) {
    this->clear();
  }

  this->reserve(coll.size());

  for (uint idx = 0; idx < coll.size(); ++idx) {
    const auto& i_obj = coll.at(idx);

    if (not stringCutObjectSelector_(i_obj)) {
      continue;
    }

    this->emplace_back(i_obj);
  }
}

#endif
