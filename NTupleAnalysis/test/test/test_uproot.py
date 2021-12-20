import glob

nevt = 0

run = 3

## test 1
#import uproot
#INPUT_FILES = glob.glob('/pnfs/desy.de/cms/tier2/store/user/missirol/jme_trigger/jmeTriggerNtuples/pfMET/v02/191103/Data_Run2018B_EGamma/*/*/*/*/*.root')
#for idx, inpf in enumerate(INPUT_FILES):
#    if idx > 9: break
#    tree = uproot.open(inpf)['JMETriggerNTuple/Events']
#    for arrays in tree.iterate(entrystart=None, entrystop=None):
#        a = 0 #print len(arrays), len(arrays['event'])

# test 2
if run == 2:
   import uproot
   for arrays in uproot.iterate('/pnfs/desy.de/cms/tier2/store/user/missirol/jme_trigger/jmeTriggerNtuples/pfMET/v02/191103/Data_Run2018B_EGamma/*/*/*/*/*.root', 'JMETriggerNTuple/Events'):
       nevt += len(arrays['event'])
       if nevt > 100000: break

## test 3
if run == 3:
   import ROOT
   INPUT_FILES = glob.glob('/pnfs/desy.de/cms/tier2/store/user/missirol/jme_trigger/jmeTriggerNtuples/pfMET/v02/191103/Data_Run2018B_EGamma/*/*/*/*/*.root')
   for idx, inpf in enumerate(INPUT_FILES):
       ifile = ROOT.TFile.Open(inpf)
       itree = ifile.Get('JMETriggerNTuple/Events')
       for i_evt in itree:
           nevt += 1
           if nevt > 100000: break
       if nevt > 100000: break
       ifile.Close()

print nevt

#for arrays in uproot.iterate('/pnfs/desy.de/cms/tier2/store/user/missirol/jme_trigger/jmeTriggerNtuples/pfMET/v02/191103/Data_Run2018B_EGamma/*/*/*/*/*.root', 'JMETriggerNTuple/Events'):
#    print len(arrays), len(arrays['event'])

#for arrays in tree.iterate():
#    print len(arrays), tree.numentries


#    i_firstEvent = 0
#    i_lastEvent = min(num_maxEvents - NUM_EVENTS_PROCESSED, i_ttree.numentries) if (num_maxEvents >= 0) else i_ttree.numentries
#
#    hltPuppiMET_pt = i_ttree.arrays('*', entrystart=i_firstEvent, entrystop=i_lastEvent)

#    for i_ent in range(i_firstEvent, i_lastEvent):
#
#        a = hltPuppiMET_pt['hltPuppiMET_pt'][i_ent]
#
#        if (num_maxEvents >= 0) and (NUM_EVENTS_PROCESSED >= num_maxEvents):
#           break
#
#        NUM_EVENTS_PROCESSED += 1
#
#        if not (NUM_EVENTS_PROCESSED % 1e5):
#           print('\033[1m'+'\033[93m'+'['+str(output)+']'+'\033[0m', 'processed events:', NUM_EVENTS_PROCESSED)
