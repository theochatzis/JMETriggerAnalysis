#!/usr/bin/env python
"""
python -i test/verticesFit.py [TFILE] 180:0:1800000:60:60:240 offlinePrimaryVerticesMultiplicity hltOuterTrackerClustersMultiplicity
"""
import sys
import ROOT

tfile = ROOT.TFile(sys.argv[1])

ttree = tfile.Get('JMETriggerNTuple/Events')

# pileupInfo_BX0_numPUInteractions
# hltPixelClustersMultiplicity
# hltOuterTrackerClustersMultiplicity
# hltPixelTracksMultiplicity
# hltPixelTracksCleanerMultiplicity
# hltPixelTracksMergerMultiplicity
# hltPixelVerticesMultiplicity
# hltTracksMultiplicity
# hltPrimaryVerticesMultiplicity
# offlinePrimaryVerticesMultiplicity
# offlineFixedGridRhoFastjetAll

th2_binning = sys.argv[2].split(':')
th2_xnbins = int(th2_binning[0])
th2_xmin = float(th2_binning[1])
th2_xmax = float(th2_binning[2])
th2_ynbins = int(th2_binning[3])
th2_ymin = float(th2_binning[4])
th2_ymax = float(th2_binning[5])

h2 = ROOT.TH2D('h2', 'h2', th2_xnbins, th2_xmin, th2_xmax, th2_ynbins, th2_ymin, th2_ymax)
ttree.Draw(sys.argv[4]+':'+sys.argv[3]+'>>h2','','goff')

print 'correlation factor =', h2.GetCorrelationFactor()

h2_py = h2.ProfileY('h2_py')
h2_py.Draw()

h2_py_pol1 = ROOT.TF1('h2_py_pol1', 'pol1')
h2_py.Fit(h2_py_pol1)
