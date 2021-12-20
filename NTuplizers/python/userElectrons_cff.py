import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi import selectedPatElectrons

from EgammaUser.EgammaPostRecoTools.EgammaPostRecoTools import setupEgammaPostRecoSeq

def userElectrons(process, era):
    ###
    ### setupEgammaPostRecoSeq: EGamma-POG routine to apply IDs + Energy-Scale/Smearing Corrections
    ###
    ###  - https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2
    ###  - https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPostRecoRecipes
    ###  - https://hypernews.cern.ch/HyperNews/CMS/get/egamma/2204/1/1.html (because of PUPPI MET, added 'phoIDModules=[]')
    ###
    if   era == '2016': setupEgammaPostRecoSeq(process, runVID=True, phoIDModules=[], runEnergyCorrections=True, applyEnergyCorrections=False, era='2016-Legacy')
    elif era == '2017': setupEgammaPostRecoSeq(process, runVID=True, phoIDModules=[], runEnergyCorrections=True, applyEnergyCorrections=False, era='2017-Nov17ReReco')
    elif era == '2018': setupEgammaPostRecoSeq(process, runVID=True, phoIDModules=[], runEnergyCorrections=True, applyEnergyCorrections=False, era='2018-Prompt')
    else:
       raise RuntimeError('userElectrons(process, era="'+str(era)+'") -- invalid value for argument "era"')

    process.userPreselectedElectrons = selectedPatElectrons.clone(
      src = 'slimmedElectrons',
      cut = '(pt > 10.) && (abs(superCluster.eta) < 2.5) && !((1.4442 < abs(superCluster.eta)) && (abs(superCluster.eta) < 1.5660))',
    )

    _elecID_dxydzCuts  =     '((abs(superCluster.eta) < 1.4442) && (abs(userFloat("dxyPV")) < 0.05) && (abs(userFloat("dzPV")) < 0.10))'
    _elecID_dxydzCuts += ' || ((abs(superCluster.eta) > 1.5660) && (abs(userFloat("dxyPV")) < 0.10) && (abs(userFloat("dzPV")) < 0.20))'

    process.userElectronsWithUserData = cms.EDProducer('ElectronPATUserData',
      src = cms.InputTag('userPreselectedElectrons'),
      primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
      effAreas_file = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt'),
      rho = cms.InputTag('fixedGridRhoFastjetAll'),

      userFloat_copycat = cms.PSet(
        mva_Iso   = cms.string('ElectronMVAEstimatorRun2Fall17'+  'IsoV2Values'),
        mva_NoIso = cms.string('ElectronMVAEstimatorRun2Fall17'+'NoIsoV2Values'),
      ),

      userInt_stringSelectors = cms.PSet(

        IDCutBasedVeto   = cms.string('('+_elecID_dxydzCuts+') && (electronID("cutBasedElectronID-Fall17-94X-V2-veto") > 0.5)'),
        IDCutBasedLoose  = cms.string('('+_elecID_dxydzCuts+') && (electronID("cutBasedElectronID-Fall17-94X-V2-loose") > 0.5)'),
        IDCutBasedMedium = cms.string('('+_elecID_dxydzCuts+') && (electronID("cutBasedElectronID-Fall17-94X-V2-medium") > 0.5)'),
        IDCutBasedTight  = cms.string('('+_elecID_dxydzCuts+') && (electronID("cutBasedElectronID-Fall17-94X-V2-tight") > 0.5)'),

        IDMVAIsoWP80 = cms.string('(electronID("mvaEleID-Fall17-iso-V2-wp80") > 0.5)'),
        IDMVAIsoWP90 = cms.string('(electronID("mvaEleID-Fall17-iso-V2-wp90") > 0.5)'),
      ),
    )

    if era == '2016':
       process.userElectronsWithUserData.effAreas_file = 'RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt'

    process.userIsolatedElectrons = selectedPatElectrons.clone(
      src = 'userElectronsWithUserData',
      cut = 'userInt("IDCutBasedLoose") > 0',
    )

    process.userElectronsTask = cms.Task(
      process.userPreselectedElectrons,
      process.userElectronsWithUserData,
      process.userIsolatedElectrons,
    )

    process.userElectronsSeq = cms.Sequence(process.egammaPostRecoSeq, process.userElectronsTask)

    return process, 'userIsolatedElectrons'
