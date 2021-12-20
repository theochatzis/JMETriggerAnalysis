#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "CorrectedJetAnalyzer.h"

typedef CorrectedJetAnalyzer<reco::CaloJet> CorrectedCaloJetAnalyzer;
DEFINE_FWK_MODULE(CorrectedCaloJetAnalyzer);

typedef CorrectedJetAnalyzer<reco::PFJet> CorrectedPFJetAnalyzer;
DEFINE_FWK_MODULE(CorrectedPFJetAnalyzer);
