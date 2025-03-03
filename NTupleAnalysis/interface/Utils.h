#ifndef NTupleAnalysis_JMETrigger_Utils_h
#define NTupleAnalysis_JMETrigger_Utils_h

#include <string>
#include <vector>
#include <map>

namespace utils {

  float deltaPhi(const float phi1, const float phi2);
  float deltaR2(const float eta1, const float phi1, const float eta2, const float phi2);

  std::vector<std::string> stringTokens(const std::string&, const std::string&);
  bool stringContains(const std::string& str, const std::string& substr);
  bool stringStartsWith(const std::string& str, const std::string& substr);
  bool stringEndsWith(const std::string& str, const std::string& substr);

  template <typename T1, typename T2>
  std::vector<T1> mapKeys(std::map<T1, T2> const&);
}  // namespace utils

template <typename T1, typename T2>
std::vector<T1> utils::mapKeys(std::map<T1, T2> const& aMap) {
  std::vector<T1> ret;
  ret.reserve(aMap.size());
  for (auto const& mapEntry : aMap) {
    ret.emplace_back(mapEntry.first);
  }

  return ret;
}

#endif
