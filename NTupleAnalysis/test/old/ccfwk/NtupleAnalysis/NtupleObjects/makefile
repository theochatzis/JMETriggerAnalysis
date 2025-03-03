PROJNAME = NtupleObjects

DIR = .
INCDIR = $(DIR)/inc
SRCDIR = $(DIR)/src
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
CXXFLAGS += -Wno-overloaded-virtual -Wno-unused
CXXFLAGS += $(ROOTCFLAGS)

LDFLAGS = $(OPT) $(ROOTLDFLAGS)

INCLUDES = -I$(DIR) -I$(ROOTSYS)/include

INC_h  = $(wildcard $(INCDIR)/*.h)
SRC_cc = $(wildcard $(SRCDIR)/*.cc)
SRC_o  = $(patsubst %.cc, %.o, $(notdir $(SRC_cc)))

LIBNAME = $(LIBDIR)/lib$(PROJNAME).so

all: $(LIBNAME)

$(LIBNAME): $(LIBDIR)/dict.cxx $(SRC_o)
	@echo "Making shared library: $@"
	@mkdir -p $(LIBDIR)
	@$(CXX) -shared $(CXXFLAGS) $(LDFLAGS) $(INCLUDES) $< $(addprefix $(OBJDIR)/, $(SRC_o)) -o $@ $(ROOTGLIBS)

$(LIBDIR)/dict.cxx: $(INC_h) linkdef.h
	@mkdir -p $(LIBDIR)
	@rootcint -f $@ -c $(INCLUDES) -p $^

%.o: $(SRCDIR)/%.cc
	@echo "Compiling $<"
	@mkdir -p $(OBJDIR)
	@$(CXX) $(CXXFLAGS) -c $(INCLUDES) $< -o $(OBJDIR)/$(notdir $@)

clean:
	rm -rf $(OBJDIR) $(LIBDIR)
