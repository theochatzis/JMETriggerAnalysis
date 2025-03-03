#include <JMETriggerAnalysis/NTupleAnalysis/interface/Utils.h>
#include <cmath>

float utils::deltaPhi(const float phi1, const float phi2) {
  auto dphi(std::abs(phi1 - phi2));
  if (dphi > M_PI)
    dphi -= 2 * M_PI;
  return dphi;
}

float utils::deltaR2(const float eta1, const float phi1, const float eta2, const float phi2) {
  auto const dphi(deltaPhi(phi1, phi2));
  return ((eta1 - eta2) * (eta1 - eta2)) + (dphi * dphi);
}

std::vector<std::string> utils::stringTokens(const std::string& str, const std::string& delimiter) {
  std::vector<std::string> toks;

  std::size_t last(0), next(0);
  while ((next = str.find(delimiter, last)) != std::string::npos) {
    std::string substr = str.substr(last, next - last);
    if (!substr.empty())
      toks.emplace_back(substr);
    last = next + delimiter.size();
  }

  if (!str.substr(last).empty()) {
    toks.emplace_back(str.substr(last));
  }

  return toks;
}

bool utils::stringContains(const std::string& str, const std::string& substr) {
  return (str.find(substr) != std::string::npos);
}

bool utils::stringStartsWith(const std::string& str, const std::string& substr) { return (str.find(substr) == 0); }

bool utils::stringEndsWith(const std::string& str, const std::string& substr) {
  if (str.length() >= substr.length()) {
    return (str.compare(str.length() - substr.length(), substr.length(), substr) == 0);
  }

  return false;
}
