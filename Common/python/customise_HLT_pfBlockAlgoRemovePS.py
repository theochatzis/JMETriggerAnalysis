import FWCore.ParameterSet.Config as cms

def customise_HLT_pfBlockAlgoRemovePS(process):

    listHltPFBlock=['hltParticleFlowBlock',
                    'hltParticleFlowBlockForTaus',
                    'hltParticleFlowBlockReg']
    for att in listHltPFBlock:
        if hasattr(process,att):
            prod = getattr(process, att)
            vpset_linkdef = prod.linkDefinitions
            for pset in reversed(vpset_linkdef):
                if pset.linkType == 'PS1:ECAL' or pset.linkType == 'PS2:ECAL':
                    vpset_linkdef.remove(pset)
            vpset_elemimport = prod.elementImporters
            for pset in reversed(vpset_elemimport):
                if pset.source == cms.InputTag( "hltParticleFlowClusterPSUnseeded" ):
                    vpset_elemimport.remove(pset)

    return process
