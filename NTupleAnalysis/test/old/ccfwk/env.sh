#!/bin/bash

export TTBSM_ENV="$PWD"

export LD_LIBRARY_PATH="$TTBSM_ENV"/NtupleAnalysis/NtupleObjects/lib:"$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="$TTBSM_ENV"/NtupleAnalysis/lib:"$LD_LIBRARY_PATH"

export PROOF_SANDBOX="$TTBSM_ENV"/PROOF_sandbox
export TMPDIR="$TTBSM_ENV"/tmp
