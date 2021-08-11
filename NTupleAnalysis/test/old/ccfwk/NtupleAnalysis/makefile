PROJNAME = NtupleAnalysis

DIR = .
INCDIR = $(DIR)/inc
SRCDIR = $(DIR)/src
SELDIR = $(DIR)/selectors
OBJDIR = $(DIR)/obj
LIBDIR = $(DIR)/lib

CXX = g++

OPT = -g
OPT2 = -g

RC := $(ROOTSYS)/bin/root-config
ROOTCFLAGS := $(shell $(RC) --cflags)
ROOTLDFLAGS := $(shell $(RC) --ldflags)
ROOTGLIBS := $(shell $(RC) --glibs)

CXXFLAGS = $(OPT2) -Wall -fPIC
CXXFLAGS += -std=c++0x -O3 -pipe
CXXFLAGS += -Wextra -Werror=overflow -Werror=maybe-uninitialized -Wdeprecated-declarations
CXXFLAGS += $(ROOTCFLAGS)

LDFLAGS = $(OPT) $(ROOTLDFLAGS)

INCLUDES = -I$(DIR) -I$(DIR)/NtupleObjects -I$(ROOTSYS)/include

SRC_cc = $(wildcard $(SRCDIR)/*.cc)
SEL_cc = $(wildcard $(SELDIR)/*.cc)
SEL_h  = $(filter-out $(SELDIR)/linkdef.h, $(wildcard $(SELDIR)/*.h))
SRC_o  = $(patsubst %.cc, %.o, $(notdir $(SRC_cc)))
SEL_o  = $(patsubst %.cc, %.o, $(notdir $(SEL_cc)))

LIBNTPOBJ = -L$(DIR)/NtupleObjects/lib -lNtupleObjects

LIBNAME = $(LIBDIR)/lib$(PROJNAME).so

all: $(LIBNAME)

$(LIBNAME): $(LIBDIR)/dict_selec.cxx $(SRC_o) $(SEL_o)
	@echo "Making shared library: $@"
	@mkdir -p $(LIBDIR)
	@$(CXX) -shared $(CXXFLAGS) $(LDFLAGS) $(INCLUDES) $< $(addprefix $(OBJDIR)/, $(SRC_o)) $(addprefix $(OBJDIR)/, $(SEL_o)) -o $@ $(ROOTGLIBS) $(LIBNTPOBJ)

$(LIBDIR)/dict_selec.cxx: $(SEL_h) $(SELDIR)/linkdef.h
	@echo "Making dictionary for selectors: $@"
	@mkdir -p $(LIBDIR)
	@rootcint -f $@ -c -p $(INCLUDES) $^

%.o: $(SELDIR)/%.cc
	@echo "Compiling $<"
	@mkdir -p $(OBJDIR)
	@$(CXX) $(CXXFLAGS) -c $(INCLUDES) $< -o $(OBJDIR)/$(notdir $@)

%.o: $(SRCDIR)/%.cc
	@echo "Compiling $<"
	@mkdir -p $(OBJDIR)
	@$(CXX) $(CXXFLAGS) -c $(INCLUDES) $< -o $(OBJDIR)/$(notdir $@)

par:
	./make_par.sh

clean:
	rm -rf $(OBJDIR) $(LIBDIR)
