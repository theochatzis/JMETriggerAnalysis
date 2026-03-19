#!/bin/bash

# python3 plotEfficienciesDPNote.py \
#   --input /eos/user/t/tchatzis/DPNoteSubmitterSepV2/ \
#   --merged_file /eos/user/t/tchatzis/DPNoteSubmitterSepV2/merged.root \
#   --config ./plotsEfficiencies_configs/dpnote_config.yaml \
#   --output_dir /eos/user/t/tchatzis/php-plots/DPNotePlots/LatestV2/

# python3 plotEfficienciesDPNote.py \
#   --input /eos/user/t/tchatzis/DPNoteSubmitter2025/Muon/ \
#   --merged_file /eos/user/t/tchatzis/DPNoteSubmitter2025/Muon/merged.root \
#   --config ./plotsEfficiencies_configs/2025data_config.yaml \
#   --output_dir /eos/user/t/tchatzis/php-plots/2025dataTakingPlots/LatestV2/Muon/

python3 plotEfficienciesDPNote.py \
  --input /eos/user/t/tchatzis/kukuvagiaOctober10_2024I_2025CDEF/ \
  --merged_file /eos/user/t/tchatzis/kukuvagiaOctober10_2024I_2025CDEF/merged.root \
  --config ./plotsEfficiencies_configs/2025data_config.yaml \
  --output_dir /eos/user/t/tchatzis/php-plots/2025dataTakingPlots/LatestV4/

# python3 plotEfficienciesDPNote.py \
#   --input /eos/user/t/tchatzis/DPNoteSubmitterNew/ \
#   --merged_file /eos/user/t/tchatzis/DPNoteSubmitterNew/merged.root \
#   --config ./plotsEfficiencies_configs/dpnote_config.yaml \
#   --output_dir /eos/user/t/tchatzis/DPNotePlotsTest/

