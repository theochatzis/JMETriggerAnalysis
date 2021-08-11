all: NtupleAnalysis

NtupleAnalysis::
	+(cd NtupleAnalysis/NtupleObjects; make)
	+(cd NtupleAnalysis; make; make par;)

clean::
	(cd NtupleAnalysis/NtupleObjects; make clean)
	(cd NtupleAnalysis; make clean)
