import uproot
import ROOT
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import os
import yaml
import argparse
from tqdm import tqdm
import math

hep.style.use("CMS")

#  _   _      _                  ______                _   _                 
# | | | |    | |                 |  ___|              | | (_)                
# | |_| | ___| |_ __   ___ _ __  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ 
# |  _  |/ _ \ | '_ \ / _ \ '__| |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | | | |  __/ | |_) |  __/ |    | | | |_| | | | | (__| |_| | (_) | | | \__ \
# \_| |_/\___|_| .__/ \___|_|    \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#              | |                                                           
#              |_|                                                           

def efficiencies_plotter(file_name, hist_label_pairs, output_name="output_efficiency.png", x_range=None, trigger_name=None):
    """
    Plots multiple efficiencies using TEfficiency from pairs of TH1D histograms with custom labels and saves the plot as a .png file.
    
    Parameters:
    - file_name: Path to the ROOT file.
    - hist_label_pairs: List of (hist_num_key, hist_den_key, label_name) tuples for efficiency curves.
    - output_name: Name of the output .png file.
    - x_range: Range for the x-axis (xmin, xmax). Default is None.
    - trigger_name: Name of the trigger for labeling the vertical line at x = 1. Default is None.
    """
    # Open the ROOT file
    root_file = ROOT.TFile.Open(file_name)

    for hist_num_key, hist_den_key, label_name in hist_label_pairs:
        # Get the numerator and denominator histograms as ROOT TH1D
        hist_num_root = root_file.Get(hist_num_key)
        hist_den_root = root_file.Get(hist_den_key)
        if not hist_num_root or not hist_den_root:
            print(f"Warning: histograms '{hist_num_key}' or '{hist_den_key}' not found in {file_name}")
            continue
        
        # Create the TEfficiency object
        eff = ROOT.TEfficiency(hist_num_root, hist_den_root)
        
        # Extract bin edges and centers for plotting
        x_edges = [hist_num_root.GetBinLowEdge(i+1) for i in range(hist_num_root.GetNbinsX())]
        x_edges.append(hist_num_root.GetBinLowEdge(hist_num_root.GetNbinsX()) + hist_num_root.GetBinWidth(hist_num_root.GetNbinsX()))
        x_mid = 0.5 * (np.array(x_edges[:-1]) + np.array(x_edges[1:]))
        
        # Retrieve efficiency values and errors
        eff_values = [eff.GetEfficiency(i + 1) for i in range(hist_num_root.GetNbinsX())]
        eff_errors_low = [eff.GetEfficiencyErrorLow(i + 1) for i in range(hist_num_root.GetNbinsX())]
        eff_errors_up = [eff.GetEfficiencyErrorUp(i + 1) for i in range(hist_num_root.GetNbinsX())]
        
        # Plot efficiency with error bars and custom label
        plt.errorbar(x_mid, eff_values, yerr=[eff_errors_low, eff_errors_up], fmt='o', label=label_name)
    
    # Set the x-axis range if provided
    if x_range is not None:
        plt.xlim(x_range)

    threshold = ""
    x_axis_quantity = ""
    y_axis_quantity = ""
    if trigger_name:
        if 'PFJet' in trigger_name:
            if 'Fwd' in trigger_name:
                threshold = float(trigger_name.split('PFJetFwd')[1])
                x_axis_quantity = "Leading Forward Offline Jet $p_T$ (GeV)"
            else:
                threshold = float(trigger_name.split('PFJet')[1])
                x_axis_quantity = "Leading Offline Jet $p_T$ (GeV)"
            y_axis_quantity = "HLT Efficiency"
        elif 'PFHT' in trigger_name:
            threshold = float(trigger_name.split('PFHT')[1])
            x_axis_quantity = "Offline $H_T$ (GeV)"
            y_axis_quantity = "HLT Efficiency"
        elif 'PFMET' in trigger_name:
            threshold = 120.0
            x_axis_quantity = "Offline $p^{miss}_T$ (GeV)"
            y_axis_quantity = "L1T+HLT Efficiency"
        elif 'PFMETNoMu' in trigger_name:
            threshold = 120.0
            x_axis_quantity = "Offline $p^{miss}_{T,no-\mu}$ (GeV)"
            y_axis_quantity = "L1T+HLT Efficiency"

    if threshold != "":
        plt.axvline(x=threshold, color='red', linestyle='-', label='Threshold')

    # Vertical line with 1.0 efficiency...
    plt.axhline(y=1.0, color='black', linestyle='--')

    # If trigger_name is provided, add a label above the vertical line
    # if trigger_name is not None:
    #     plt.text(1.0, 1.05, trigger_name, 
    #      horizontalalignment='center',  # Adjust the horizontal alignment (left, center, right)
    #      verticalalignment='bottom',    # Adjust the vertical alignment (top, middle, bottom)
    #      color='red', 
    #      fontsize=12)  # Adjust fontsize if needed

    # Add plot labels and CMS styling....
    hep.cms.label("Preliminary", data=True, com=13.6, lumi=0.0)
    plt.xlabel(x_axis_quantity)
    plt.ylabel(y_axis_quantity)
    plt.ylim(0, 1.2)

    if ('PFMETNoMu120_' in trigger_name) and ('FilterHF' in trigger_name):
        trigger_name = 'PF MET$(no-\mu)$ > 120GeV (Filter HF)'
    
    if 'PFMETNoMu120_' in trigger_name:
        trigger_name = 'PF MET$(no-\mu)$ > 120GeV'

    if 'PFMET120_' in trigger_name:
        trigger_name = 'PFMET120'
    
    plt.legend(loc="right", title=trigger_name)  # Use bbox for a text box with labels
    #plt.legend(loc="upper left", bbox_to_anchor=(1, 1), title=trigger_name)  # Use bbox for a text box with labels
    
    # Adding a grid to both x and y axes
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=1, color='gray', alpha=0.2)
    # Save the figure as a .png file.
    os.makedirs(os.path.dirname(output_name), exist_ok=True)
    plt.savefig(output_name, dpi=300, bbox_inches='tight')
    
    plt.clf() # Clear figure after saving
    
    print(f"Efficiency plot saved as {output_name}")

    # Close the ROOT file after processing
    root_file.Close()


def root_files_hunter(base_dir):
    '''
    Function that "hunts" to find every ROOT file in sub-directories of a base_dir...
    '''
    root_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".root"):
                root_files.append(os.path.join(root, file))
    return root_files


def add_histograms(in_dir, out_dir):
    '''
    adding histos in directories in recursive way... 
    '''
    for key in in_dir.GetListOfKeys():
        obj_name = key.GetName()
        obj = key.ReadObj()
        # Check if it's a directory and do the same...
        if obj.InheritsFrom("TDirectory"):
            # Create subdir if not exists
            out_subdir = out_dir.GetDirectory(obj_name)
            if not out_subdir:
                out_dir.mkdir(obj_name)
                out_subdir = out_dir.GetDirectory(obj_name)
            add_histograms(obj, out_subdir)
        elif obj.InheritsFrom("TH1"):  # Histogram type ( this includes also TH2Fs they inherit from TH1 - note this for 2D efficiencies if needed)
            # Check if histogram already exists in output dir
            out_hist = out_dir.Get(obj_name)
            if out_hist: 
                out_hist.Add(obj)  # Add histo...
            else:
                out_dir.cd()
                obj_clone = obj.Clone()
                obj_clone.SetDirectory(out_dir)
                obj_clone.Write()
        else:
            # For other objects, just write if not exist
            if not out_dir.Get(obj_name):
                out_dir.cd()
                obj_clone = obj.Clone()
                obj_clone.SetDirectory(out_dir)
                obj_clone.Write()

def chunky_merging(input_files, output_file, chunk_size=100):
    """
    Merge ROOT files in chunks, adding histograms with the same name.

    Inputs:
    - input_files: list of ROOT file paths to merge
    - output_file: final merged ROOT file path
    - chunk_size: number of files to use per chunk
    """
    n_files = len(input_files)
    n_chunks = math.ceil(n_files / chunk_size)
    temp_files = []

    # Merge in chunks
    for i in range(n_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, n_files)
        chunk_files = input_files[start:end]

        temp_file = f"temp_merge_{i}.root"
        temp_files.append(temp_file)

        out_file = ROOT.TFile.Open(temp_file, "RECREATE")

        print(f"Merging chunk {i+1}/{n_chunks} with {len(chunk_files)} files...")
        for fpath in tqdm(chunk_files, unit="file"):
            in_file = ROOT.TFile.Open(fpath, "READ")
            if not in_file or in_file.IsZombie():
                print(f"Warning: could not open {fpath}")
                continue

            add_histograms(in_file, out_file)

            in_file.Close()

        out_file.Write()
        out_file.Close()

    # Merge chunk files into final output
    print(f"Merging {len(temp_files)} chunk files into final output file {output_file} ...")
    final_out = ROOT.TFile.Open(output_file, "RECREATE")
    for temp_f in tqdm(temp_files, unit="chunk file"):
        temp_in = ROOT.TFile.Open(temp_f, "READ")
        if not temp_in or temp_in.IsZombie():
            print(f"Warning: could not open {temp_f}")
            continue

        add_histograms(temp_in, final_out)

        temp_in.Close()
    final_out.Write()
    final_out.Close()

    # Clean up temp files
    for temp_f in temp_files:
        try:
            os.remove(temp_f)
        except Exception as e:
            print(f"Could not remove temp file {temp_f}: {e}")

    print("Chunky merging complete!")

if __name__ == "__main__":
#  _   _                ______      __ _       _ _   _                 
# | | | |               |  _  \    / _(_)     (_) | (_)                
# | | | |___  ___ _ __  | | | |___| |_ _ _ __  _| |_ _  ___  _ __  ___ 
# | | | / __|/ _ \ '__| | | | / _ \  _| | '_ \| | __| |/ _ \| '_ \/ __|
# | |_| \__ \  __/ |    | |/ /  __/ | | | | | | | |_| | (_) | | | \__ \
#  \___/|___/\___|_|    |___/ \___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/

    parser = argparse.ArgumentParser(description="Plot trigger Efficiencies.")
    parser.add_argument("--input_dir", required=True, help="Input base directory containing ROOT files, or have them in subdirs")
    parser.add_argument("--config", required=True, help="YAML config file path with parameters like paths ranges etc.")
    parser.add_argument("--output_dir", default="plots_output", help="Output directory for plots to be stored.")
    parser.add_argument("--chunk_size", default=250, type=int, help="Number of files to merge per chunk")
    parser.add_argument("--merged_file", default="merged.root", help="Merged ROOT file path. If it does exist will just use that instead or inputs in directory.")

    args = parser.parse_args()

    # Load configuration from YAML file.
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    triggers_list = config["triggers_list"]
    comparisonPeriods = config["comparisonPeriods"]
    regions_labels = config["regions_labels"]
    x_range_dict = config["x_range_dict"]

#  _____                  _    ______ _ _      
# |_   _|                | |   |  ___(_) |     
#   | | _ __  _ __  _   _| |_  | |_   _| | ___ 
#   | || '_ \| '_ \| | | | __| |  _| | | |/ _ \
#  _| || | | | |_) | |_| | |_  | |   | | |  __/
#  \___/_| |_| .__/ \__,_|\__| \_|   |_|_|\___|
#            | |                               
#            |_|                               
    # Creating the input by merging the sub-dirs ROOT files, or using the already merged ROOT file.
    if os.path.exists(args.merged_file):
        print(f"Using as input existing merged file: {args.merged_file}")
    else:
        # Chasing the directories to find all ROOT files...
        all_root_files = root_files_hunter(args.input_dir)
        if len(all_root_files) == 0:
            print(f"No ROOT files found in {args.input_dir}")
            exit(1)
        # Create a root file from combining all ROOT files into one with chunky merging...
        chunky_merging(all_root_files, args.merged_file, chunk_size=args.chunk_size)

# ___  ___      _          _____ __  __ _      _                 _           
# |  \/  |     | |        |  ___/ _|/ _(_)    (_)               (_)          
# | .  . | __ _| | _____  | |__| |_| |_ _  ___ _  ___ _ __   ___ _  ___  ___ 
# | |\/| |/ _` | |/ / _ \ |  __|  _|  _| |/ __| |/ _ \ '_ \ / __| |/ _ \/ __|
# | |  | | (_| |   <  __/ | |__| | | | | | (__| |  __/ | | | (__| |  __/\__ \
# \_|  |_/\__,_|_|\_\___| \____/_| |_| |_|\___|_|\___|_| |_|\___|_|\___||___/

    # Now process the merged ROOT file for plots for all triggers...
    for trigger_name in triggers_list:
        # Define the offline quantity to be used per type of trigger.
        offlineQuantity = "offlineAK4PFPuppiJetsCorrected_EtaIncl_pt0"
        if 'PFHT' in trigger_name:
            offlineQuantity = "offlineAK4PFPuppiJetsCorrected_Eta2p5_HT"
        if 'PFJetFwd' in trigger_name:
            offlineQuantity = "offlineAK4PFPuppiJetsCorrected_HF_pt0"
        if 'MET' in trigger_name:
            offlineQuantity = "offlinePFPuppiMET_Type1_pt"
        if 'METNoMu' in trigger_name:
            offlineQuantity = "offlinePFPuppiMET_Type1_ptNoMu"

        den_trigger_name = trigger_name + "_HLTDenominatorPathAccept"
        if 'MET' in trigger_name:
            den_trigger_name = 'HLT_IsoMu27_HLTPathAccept'

        for comparisonPeriodCategory, comparisonPeriodsDict in comparisonPeriods.items():
            hist_label_pairs = []
            for period in comparisonPeriodsDict.keys():
                hist_label_pairs.append([
                    f"{trigger_name}_HLTPathAccept_{period}/{offlineQuantity}",
                    f"{den_trigger_name}_{period}/{offlineQuantity}",
                    comparisonPeriodsDict[period]
                ])

            output_dir = os.path.join(args.output_dir, trigger_name, comparisonPeriodCategory)
            os.makedirs(output_dir, exist_ok=True)
            output_name = os.path.join(output_dir, f"{trigger_name}_{comparisonPeriodCategory}.png")
            efficiencies_plotter(args.merged_file, hist_label_pairs, output_name, x_range_dict.get(trigger_name), trigger_name)

            for period in comparisonPeriodsDict.keys():
                if ("PFJet" in trigger_name) and ("Fwd" not in trigger_name):
                    hist_label_pairs = [
                        [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HB_pt0",
                         f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HB_pt0", regions_labels['HB']],
                        [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HE1_pt0",
                         f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HE1_pt0", regions_labels['HE1']],
                        [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HE2_pt0",
                         f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HE2_pt0", regions_labels['HE2']],
                        [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HF_pt0",
                         f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HF_pt0", regions_labels['HF']]
                    ]
                    output_name = os.path.join(output_dir, f"{trigger_name}_{period}_eta_ranges.png")
                    efficiencies_plotter(args.merged_file, hist_label_pairs, output_name, x_range_dict.get(trigger_name), trigger_name)

                    hist_label_pairs = [
                        [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPix_pt0",
                         f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPix_pt0", regions_labels['BPix']],
                        [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPixVeto_pt0",
                         f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPixVeto_pt0", regions_labels['BPixVeto']]
                    ]
                    output_name = os.path.join(output_dir, f"{trigger_name}_{period}_bpix.png")
                    efficiencies_plotter(args.merged_file, hist_label_pairs, output_name, x_range_dict.get(trigger_name), trigger_name)

                    hist_label_pairs = [
                        [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPix_pt0",
                         f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPix_pt0", regions_labels['FPix']],
                        [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPixVeto_pt0",
                         f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPixVeto_pt0", regions_labels['FPixVeto']]
                    ]
                    output_name = os.path.join(output_dir, f"{trigger_name}_{period}_fpix.png")
                    efficiencies_plotter(args.merged_file, hist_label_pairs, output_name, x_range_dict.get(trigger_name), trigger_name)

    # clean up merged ROOT file (not needed can keep it to re-run why not...)
    # os.remove(args.merged_file)
