DIR = .
SRCDIR = $(DIR)
BINDIR = $(DIR)/bin

BASEDIR = $(DIR)/..
NTPANADIR = $(BASEDIR)/NtupleAnalysis
NTPOBJDIR = $(BASEDIR)/NtupleAnalysis/NtupleObjects

CXX = g++

OPT = -g
OPT2 = -g

RC := $(ROOTSYS)/bin/root-config
ROOTCFLAGS := $(shell $(RC) --cflags)
ROOTLDFLAGS := $(shell $(RC) --ldflags)
ROOTGLIBS := $(shell $(RC) --glibs)
ROOTPROOFLIBS := -lProof -lProofPlayer 

CXXFLAGS = $(OPT2) -Wall -fPIC
CXXFLAGS += -Wno-overloaded-virtual -Wno-unused
CXXFLAGS += $(ROOTCFLAGS)

LDFLAGS = $(OPT) $(ROOTLDFLAGS)

INCLUDES = -I$(BASEDIR) -I$(NTPANADIR) -I$(NTPOBJDIR)

SRC_cc := $(wildcard $(SRCDIR)/*.cc)
SRC_cc := $(filter-out $(SRCDIR)/tester.cc   , $(SRC_cc))
SRC_cc := $(filter-out $(SRCDIR)/TTbarSR.cc  , $(SRC_cc))
SRC_cc := $(filter-out $(SRCDIR)/TTbarRECO.cc, $(SRC_cc))
SRC_bin = $(patsubst %.cc,%,$(notdir $(SRC_cc)))

LIBLIST := -L$(NTPOBJDIR)/lib -lNtupleObjects
LIBLIST += -L$(NTPANADIR)/lib -lNtupleAnalysis
#LIBLIST += -L$(NTPANADIR)/lib -lNtupleSelectors
LIBLIST += $(ROOTPROOFLIBS)

all: $(addprefix $(BINDIR)/, $(SRC_bin))

$(BINDIR)/%: $(SRCDIR)/%.cc
	@echo "Compiling executable $<"
	@mkdir -p $(BINDIR)
	@$(CXX) $(CXXFLAGS) -Wl,--no-as-needed $(ROOLDFLAGS) $(INCLUDES) $< -o $@ $(ROOTGLIBS) $(LIBLIST)

clean:
	rm -rf $(BINDIR)
