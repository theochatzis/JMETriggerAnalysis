#!/bin/bash
source env.sh


# directory with input(s) 
# which has reco's as subfolders
INPDIR=/eos/user/t/tchatzis/samples2023

python3 plot_hltRun3EffsData_2023.py -i ${INPDIR} -o ./effPlots_2023Data_NoBPix

