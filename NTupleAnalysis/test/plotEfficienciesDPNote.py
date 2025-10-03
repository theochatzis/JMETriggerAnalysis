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
from multiprocessing import Pool
import re 
from scipy.optimize import curve_fit
from scipy.special import erf
from scipy.optimize import minimize

hep.style.use("CMS")

#  _   _      _                  ______                _   _                 
# | | | |    | |                 |  ___|              | | (_)                
# | |_| | ___| |_ __   ___ _ __  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ 
# |  _  |/ _ \ | '_ \ / _ \ '__| |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | | | |  __/ | |_) |  __/ |    | | | |_| | | | | (__| |_| | (_) | | | \__ \
# \_| |_/\___|_| .__/ \___|_|    \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#              | |                                                           
#              |_|                                                           

# Error function for turn-on fit
def erf_turnon(x, A, mu, sigma):
    return 0.5 * A * (1 + erf((x - mu) / (np.sqrt(2) * sigma)))

def jacobian_erf(x, A, mu, sigma):
    arg = (x - mu) / (np.sqrt(2) * sigma)
    dA = 0.5 * (1 + erf(arg))
    dmu = -(A / (np.sqrt(2*np.pi) * sigma)) * np.exp(-arg**2)
    dsigma = -(A * (x - mu) / (np.sqrt(2*np.pi) * sigma**2)) * np.exp(-arg**2)
    return np.array([dA, dmu, dsigma])

def prediction_with_uncertainty(x_vals, popt, cov):
    A, mu, sigma = popt
    y = erf_turnon(x_vals, A, mu, sigma)
    y_err = []
    for x in x_vals:
        J = jacobian_erf(x, A, mu, sigma)
        var = J @ cov @ J.T   # matrix multiplication
        y_err.append(np.sqrt(var) if var > 0 else 0)
    return y, np.array(y_err)

def prediction_with_uncertainty_uncorr(x_vals, popt, cov):
    """
    Compute prediction and uncertainty ignoring correlations between parameters.

    Parameters:
    - x_vals: array-like of x values
    - popt: fitted parameters [A, mu, sigma]
    - cov: covariance matrix (3x3)

    Returns:
    - y: predicted values
    - y_err: uncertainties ignoring off-diagonal correlations
    """
    A, mu, sigma = popt
    y = erf_turnon(x_vals, A, mu, sigma)

    # Extract standard deviations
    sigma_A, sigma_mu, sigma_sigma = np.sqrt(np.diag(cov))

    y_err = []
    for x in x_vals:
        arg = (x - mu) / (np.sqrt(2) * sigma)
        # partial derivatives
        dA = 0.5 * (1 + erf(arg))
        dmu = -(A / (np.sqrt(2*np.pi) * sigma)) * np.exp(-arg**2)
        dsigma = -(A * (x - mu) / (np.sqrt(2*np.pi) * sigma**2)) * np.exp(-arg**2)
        # Uncorrelated error propagation
        var = (dA * sigma_A)**2 + (dmu * sigma_mu)**2 + (dsigma * sigma_sigma)**2
        y_err.append(np.sqrt(var) if var > 0 else 0)
    
    return y, np.array(y_err)

def nll(params, x, k, N, model):
    """Negative log-likelihood for binomial efficiencies"""
    p = model(x, *params)
    # avoid log(0)
    p = np.clip(p, 1e-9, 1-1e-9)
    return -np.sum(k * np.log(p) + (N - k) * np.log(1 - p))


def trigger_pattern(trigger):
    """
    Find the trigger type and main threshold (first number).
    
    Inputs:
    - trigger: The name of the trigger as a string, e.g. 'HLT_PFJet60'
    
    Returns a dictionary with the type of trigger, and the threshold { "type": str, "threshold": int }
    """
    trigger_types = ["PFJetFwd", "PFJet", "PFHT", "PFMETNoMu", "PFMET"]
    
    for type_ in trigger_types:
        match = re.search(rf"{type_}(\d+)", trigger)
        if match:
            return {"type": type_, "threshold": int(match.group(1))}
    
    return {"type": None, "threshold": None}

# def FixHist(passed, total):
#         """Functions that ennsures passed <= total for all bins..."""
#         nbins = passed.GetNbinsX()
#         for i in range(1, nbins + 1):
#             p = passed.GetBinContent(i)
#             t = total.GetBinContent(i)
#             if p > t:
#                 print(f"[FixHist] Bin {i}: passed={p} > total={t}, setting passed=total")
#                 passed.SetBinContent(i, t)
#             # Optional: fix negative totals
#             if t < 0:
#                 print(f"[FixHist] Bin {i}: total={t} < 0, setting total=0 and passed=0")
#                 total.SetBinContent(i, 0)
#                 passed.SetBinContent(i, 0)

def efficiencies_plotter(file_name, hist_label_pairs, output_name="output_efficiency.png", plot_label_name="",
                         x_range=None, rebin=None, trigger_name=None, lumi=0):
    """
    Plots multiple efficiencies using TEfficiency from pairs of TH1D histograms with custom labels and saves the plot as a .png file.
    
    Parameters:
    - file_name: Path to the ROOT file.
    - hist_label_pairs: List of (hist_num_key, hist_den_key, label_name) tuples for efficiency curves.
    - output_name: Name of the output .png file.
    - x_range: Range for the x-axis (xmin, xmax). Default is None.
    - trigger_name: Name of the trigger for labeling the vertical line at x = 1. Default is None.
    - rebin: None (no rebin), int (uniform rebin factor), or list of bin edges (variable-width rebinning).
    """
    import array

    # Open the ROOT file
    root_file = ROOT.TFile.Open(file_name)
    
    threshold = ""
    x_axis_quantity = ""
    y_axis_quantity = ""
    
    trigger_pattern_ = trigger_pattern(trigger_name)
    typeOfTrigger_ = trigger_pattern_["type"]
    threshold = str(trigger_pattern_["threshold"])
    
    for hist_num_key, hist_den_key, label_name in hist_label_pairs:
        # Get the numerator and denominator histograms as ROOT TH1D
        hist_num_root = root_file.Get(hist_num_key)
        hist_den_root = root_file.Get(hist_den_key)
        if not hist_num_root or not hist_den_root:
            print(f"Warning: histograms '{hist_num_key}' or '{hist_den_key}' not found in {file_name}")
            continue
        
        if hist_num_root.GetEntries() < 100:
            print(f"Warning: Numerator '{hist_num_key}' has less than 100 entries... Skipping this pair...")
            continue

        # Optional rebinning
        if rebin is not None:
            if isinstance(rebin, int):
                # Uniform rebinning by factor
                hist_num_root = hist_num_root.Rebin(rebin)
                hist_den_root = hist_den_root.Rebin(rebin)
            elif isinstance(rebin, (list, tuple, np.ndarray)):
                # Variable-width rebinning with new bin edges
                bin_edges_arr = array.array('d', rebin)
                nbins_new = len(bin_edges_arr) - 1
                hist_num_root = hist_num_root.Rebin(nbins_new, hist_num_root.GetName() + "_rebinned", bin_edges_arr)
                hist_den_root = hist_den_root.Rebin(nbins_new, hist_den_root.GetName() + "_rebinned", bin_edges_arr)
            else:
                raise ValueError("`rebin` must be None, int, or a sequence of bin edges.")
        
        # Fix inconsistencies (if any) - this was used to fix entries where numerator is bigger than denominator.
        #FixHist(hist_num_root, hist_den_root)

        # Create the TEfficiency object
        eff = ROOT.TEfficiency(hist_num_root, hist_den_root)
        
        # Extract bin edges and centers for plotting
        x_edges = [hist_num_root.GetBinLowEdge(i+1) for i in range(hist_num_root.GetNbinsX())]
        x_edges.append(hist_num_root.GetBinLowEdge(hist_num_root.GetNbinsX()) + hist_num_root.GetBinWidth(hist_num_root.GetNbinsX()))
        x_mid = 0.5 * (np.array(x_edges[:-1]) + np.array(x_edges[1:]))
        x_err_low = np.array(x_mid) - np.array(x_edges[:-1]) 
        x_err_high = np.array(x_edges[1:]) - np.array(x_mid)

        # Retrieve efficiency values and errors
        eff_values = [eff.GetEfficiency(i + 1) for i in range(hist_num_root.GetNbinsX())]
        eff_errors_low = [eff.GetEfficiencyErrorLow(i + 1) for i in range(hist_num_root.GetNbinsX())]
        eff_errors_up = [eff.GetEfficiencyErrorUp(i + 1) for i in range(hist_num_root.GetNbinsX())]
        
        # Plot efficiency with error bars and custom label
        #plt.errorbar(x_mid, eff_values, xerr=[x_err_low, x_err_high], yerr=[eff_errors_low, eff_errors_up], fmt='o', label=label_name)
         # Plot efficiency points
        points = plt.errorbar(
            x_mid, eff_values, 
            xerr=[x_err_low, x_err_high], 
            yerr=[eff_errors_low, eff_errors_up],
            fmt='o', label=label_name
        )

        x_fit = x_mid # range to fit
        # if "MET" in typeOfTrigger_:
        #     x_fit = x_fit[x_fit>150] # fit from 170 GeV and above
        # Perform fit with error the larger from the low and up.
        # chi^2 fit

        # eff_errors = np.maximum(eff_errors_low, eff_errors_up)

        # popt, pcov = curve_fit(
        #     erf_turnon, x_mid, eff_values, sigma=eff_errors, 
        #     p0=[1.0, np.median(x_mid), 10.0],  # Initial parameters guesses
        #     bounds=([0, np.min(x_mid), 0], [1.2, np.max(x_mid)*2, np.max(x_mid)]) # lower upper limits for parameters
        # ) 
        # perr = np.sqrt(np.diag(pcov))

        # ML fit with binomials (k,N) per bin
        # Extract numerator and denominator counts
        k = np.array([hist_num_root.GetBinContent(i+1) for i in range(hist_num_root.GetNbinsX())])
        N = np.array([hist_den_root.GetBinContent(i+1) for i in range(hist_den_root.GetNbinsX())])
        threshold_value = float(threshold)
        # if "MET" in typeOfTrigger_:
        #     k = k[len(k)-len(x_fit)-1:-1]
        #     N = N[len(N)-len(x_fit)-1:-1]
        res = minimize(
            nll,
            x0=[1.0, threshold_value, 0.1*threshold_value],
            args=(x_fit, k, N, erf_turnon),
            method="L-BFGS-B",
            bounds=[(0.9, 1.0), (0.5*threshold_value, 1.5*threshold_value), (0.001*threshold_value, 0.5*threshold_value)]
        )
        
        popt = res.x # results of fitted params
        
        # Hessian erros
        if res.hess_inv is not None:
            # Convert to dense matrix
            cov = res.hess_inv.todense() if hasattr(res.hess_inv, "todense") else res.hess_inv
            perr = np.sqrt(np.diag(cov))   # 1 sigma errors
        else:
            perr = None
        #print(perr)
        # Correlation matrix
        corr = cov / np.outer(np.sqrt(np.diag(cov)), np.sqrt(np.diag(cov)))
        print(corr)
        
        # Generate smooth fit curve
        x_fit = np.linspace(np.min(x_fit), np.max(x_fit), 500)

        # Get color assigned by matplotlib to the points
        curve_color = points[0].get_color()
        
        y_fit, y_err = prediction_with_uncertainty_uncorr(x_fit, popt, cov)
        
        # Plot fit curve with same color
        plt.plot(
            x_fit, y_fit, '-', color=curve_color,
            label=r"plateau="+f"{popt[0]:.2f}"+r" $\mu$="+f"{popt[1]:.0f}"+r" $\sigma$="+f"{popt[2]:.0f}"+r" $\sigma/\mu$="+f"{popt[2]/popt[1]:.2f}"
        )
        # Draw uncertainty band
        #plt.fill_between(x_fit, y_fit - y_err, y_fit + y_err, color=curve_color, alpha=0.3, linewidth=0)

        # # Plot fit with same color
        # plt.plot(
        #     x_fit, erf_turnon(x_fit, *popt), '-', color=curve_color,
        #     label=r"plateau="+f"{popt[0]:.2f}"+r" $\mu$="+f"{popt[1]:.0f}"+r" $\sigma$="+f"{popt[2]:.0f}"+r" $\sigma/\mu$="+f"{popt[2]/popt[1]:.2f}"
        # )

        # Draw vertical dashed line at fitted midpoint (p1), same color
        plt.axvline(
            x=popt[1], color=curve_color, linestyle='--', alpha=0.7
        )

    # Set the x-axis range if provided else will automatically find the range to have data...
    xmin = 0.
    xmax = 1.
    if x_range is not None:
        xmin = x_range[0]
        xmax = x_range[1]
        #plt.xlim(x_range)
    else:
        # Auto-range from histogram content
        first_bin = None
        last_bin = None
        for i in range(1, hist_den_root.GetNbinsX() + 1):
            if hist_den_root.GetBinContent(i) > 0:
                if first_bin is None:
                    first_bin = i
                last_bin = i
        if first_bin is not None and last_bin is not None:
            xmin = hist_den_root.GetBinLowEdge(first_bin)
            xmax = hist_den_root.GetBinLowEdge(last_bin) + hist_den_root.GetBinWidth(last_bin)
    plt.xlim(xmin, xmax)


    
    x_axis_quantity_dict = {
        'PFJet' : "Leading Offline Jet $p_T$ (GeV)",
        'PFJetFwd' : "Leading Forward Offline Jet $p_T$ (GeV)",
        'PFHT' : "Offline $H_T$ (GeV)",
        'PFMET' : "Offline $p^{miss}_T$ (GeV)",
        'PFMETNoMu' : "Offline $p^{miss}_{T,no-\mu}$ (GeV)"
    }
    x_axis_quantity = x_axis_quantity_dict[typeOfTrigger_]
    y_axis_quantity = "HLT Efficiency"
    if 'IsoMu' in hist_label_pairs[0][1]:
        y_axis_quantity = "L1T+HLT Efficiency"
    
    # Vertical line of threshold...
    if threshold != "":
        plt.axvline(x=float(threshold), color='red', linestyle='-', label='Threshold')

    # Horizontal line with 1.0 efficiency...
    plt.axhline(y=1.0, color='black', linestyle='--')

    # If trigger_name is provided, add a label above the vertical line
    # if trigger_name is not None:
    #     plt.text(1.0, 1.05, trigger_name, 
    #      horizontalalignment='center',  # Adjust the horizontal alignment (left, center, right)
    #      verticalalignment='bottom',    # Adjust the vertical alignment (top, middle, bottom)
    #      color='red', 
    #      fontsize=12)  # Adjust fontsize if needed

    # Add plot labels and CMS styling....
    hep.cms.label("Preliminary",
                   data=True,
                   com=13.6,
                   lumi=lumi, # set to zero as a placeholder, can be also string with LaTex...
                   loc=0
                   )
    

    plt.xlabel(x_axis_quantity)
    plt.ylabel(y_axis_quantity)
    plt.ylim(0, 1.2)
    

    trigger_description_dict = {
        'PFJet' : f"HLT PF Jet $p_T > {threshold}$ GeV",
        'PFJetFwd' : f"HLT PF Jet with $|\eta|>3.0$ and $p_T > {threshold}$ GeV",
        'PFHT' : f"HLT PF $H_T > {threshold}$ GeV",
        'PFMET' : "HLT $p^{miss}_T > "+str(threshold)+"$ GeV and $H^{miss}_T >"+str(threshold)+"$ GeV",
        'PFMETNoMu' : "HLT $p^{miss}_{T,no-\mu} > "+str(threshold)+"$ GeV \nand $H^{miss}_{T,no-\mu} >"+str(threshold)+"$ GeV"
    }

    # Adding text with trigger cuts etc...
    trigger_description = ""
    trigger_description = trigger_description_dict[typeOfTrigger_] + " "+ plot_label_name
    if trigger_description != "":
        plt.text(
            0.02, 0.95, trigger_description,
            transform=plt.gca().transAxes,   # use axes coordinates (0,0 = bottom left, 1,1 = top right)
            ha='left', va='top',             # align relative to that point
            fontsize=20
        )
        #plt.text(0.30*(xmax-xmin), 1.1, trigger_description)
    
    #plt.legend(loc="right", title="")  # Use bbox for a text box with labels
    #plt.legend(loc="upper left", bbox_to_anchor=(1, 1), title=trigger_name)  # Use bbox for a text box with labels
    plt.legend(fontsize=14, frameon=False, loc="best")

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
    """
    Recursively add histograms and other ROOT objects from in_dir into out_dir.
    how it works:
      - TH1 objects are cloned & detached from input files
      - If histogram exists in output -> then you add
      - If not -> then you clone and register once
      - Only write at the very end (out_file.Write())
    """
    for key in in_dir.GetListOfKeys():
        obj_name = key.GetName()
        obj = key.ReadObj()

        if obj.InheritsFrom("TDirectory"):
            # Handle subdirectories
            out_subdir = out_dir.GetDirectory(obj_name)
            if not out_subdir:
                out_subdir = out_dir.mkdir(obj_name)
            add_histograms(obj, out_subdir)

        elif obj.InheritsFrom("TH1"):
            out_hist = out_dir.Get(obj_name)
            if out_hist:
                # Add directly
                out_hist.Add(obj)
            else:
                # First time -> clone and detach
                obj_clone = obj.Clone(obj_name)
                obj_clone.SetDirectory(0)  # detach from input file
                out_dir.Append(obj_clone)  # register in output

        else:
            # For other objects, only copy if not already present
            if not out_dir.Get(obj_name):
                obj_clone = obj.Clone(obj_name)
                obj_clone.SetDirectory(0)
                out_dir.Append(obj_clone)



def process_chunk(args):
    """
    Process a chunk of ROOT files and merge them into a temporary ROOT file.
    """
    chunk_files, temp_file = args
    out_file = ROOT.TFile.Open(temp_file, "RECREATE")
    if not out_file or out_file.IsZombie():
        print(f"Error: Could not create temp file {temp_file}")
        return None

    for fpath in chunk_files:
        in_file = ROOT.TFile.Open(fpath, "READ")
        if not in_file or in_file.IsZombie():
            print(f"Warning: could not open {fpath}")
            continue
        add_histograms(in_file, out_file)
        in_file.Close()

    out_file.Write()
    out_file.Close()
    return temp_file


def chunky_merging(input_files, output_file, chunk_size=100, n_workers=4):
    """
    Merge ROOT files in chunks in parallel using multiprocessing.
    Inputs:
    - input_files: list of ROOT file paths to merge
    - output_file: final merged ROOT file path
    - chunk_size: number of files per chunk
    - n_workers: number of parallel workers
    """
    n_files = len(input_files)
    n_chunks = math.ceil(n_files / chunk_size)

    chunks = []
    temp_files = []

    for i in range(n_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, n_files)
        chunk_files = input_files[start:end]
        temp_file = f"temp_merge_{i}.root"
        temp_files.append(temp_file)
        chunks.append((chunk_files, temp_file))

    print(f"Starting parallel processing of {n_chunks} chunks with {n_workers} workers...")
    with Pool(processes=n_workers) as pool:
        for _ in tqdm(pool.imap_unordered(process_chunk, chunks), total=n_chunks, unit="chunk"):
            pass

    print(f"Merging {len(temp_files)} chunk files into final output {output_file}...")
    final_out = ROOT.TFile.Open(output_file, "RECREATE")
    if not final_out or final_out.IsZombie():
        raise RuntimeError(f"Could not create final output file: {output_file}")

    for temp_f in tqdm(temp_files, unit="chunk file"):
        temp_in = ROOT.TFile.Open(temp_f, "READ")
        if not temp_in or temp_in.IsZombie():
            print(f"Warning: could not open {temp_f}")
            continue
        add_histograms(temp_in, final_out)
        temp_in.Close()

    final_out.Write()
    final_out.Close()

    # Clean up temporary files
    for temp_f in temp_files:
        try:
            os.remove(temp_f)
        except Exception as e:
            print(f"Could not remove temp file {temp_f}: {e}")

    print("Chunky merging complete!")

def merging_exec(input_dir, merged_file, chunk_size):
    '''
    Takes a directory and merges all files. Merges means it adds histograms and keeps the structure intact.
    '''
    # Chasing the directories to find all ROOT files...
    all_root_files = root_files_hunter(input_dir)
    if len(all_root_files) == 0:
        print(f"No ROOT files found in {input_dir}")
        exit(1)
    # Create a root file from combining all ROOT files into one with chunky merging...
    n_cores = os.cpu_count() or 1
    n_workers = max(1, n_cores // 2)
    chunky_merging(all_root_files, merged_file, chunk_size=chunk_size, n_workers=n_workers)

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
    parser.add_argument("--chunk_size", default=50, type=int, help="Number of files to merge per chunk")
    parser.add_argument("--merged_file", default="merged.root", help="Merged ROOT file path. If it does exist will just use that instead or inputs in directory.")
    parser.add_argument("--is-miniaod", default=True, type=bool, help="Declares if the file input is from MiniAOD or RAW. If its RAW will use NoSelection as denominator.")
    args = parser.parse_args()

    # Load configuration from YAML file.
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    triggers_list = config["triggers_list"]
    comparisonPeriods = config["comparisonPeriods"]
    regions_labels = config["regions_labels"]
    x_range_dict = config["x_range_dict"]
    rebin_dict = config["rebin_dict"]

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
        user_input = input("Do you want to keep this file? (y/n): ").strip().lower()
        if user_input in ("y", "yes"):
            print("Keeping existing merged file. Skipping merging.")
        else:
            try:
                os.remove(args.merged_file)
                print(f"Deleted existing file {args.merged_file}. Starting merge.")
                merging_exec(args.input_dir, args.merged_file, args.chunk_size)
            except Exception as e:
                print(f"Error while trying deleting the file {args.merged_file}: {e}")
                exit(1)
    else:
        merging_exec(args.input_dir, args.merged_file, args.chunk_size)
    
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
        
        # Define denominator
        den_trigger_name = None
        merged_file_ = ROOT.TFile.Open(args.merged_file)
        if args.is_miniaod: # Only then it will consider this otherwise will need NoSelection folder.
            den_trigger_name = f"{trigger_name}_HLTDenominatorPathAccept"
            if 'MET' in trigger_name:
                den_trigger_name = 'HLT_IsoMu27_HLTPathAccept'
        else:
            den_trigger_name = "NoSelection"

        for comparisonPeriodCategory, comparisonPeriodsDict in comparisonPeriods.items():
            hist_label_pairs = []
            lumi = 0
            for period in comparisonPeriodsDict.keys():
                hist_label_pairs.append([
                    f"{trigger_name}_HLTPathAccept_{period}/{offlineQuantity}",
                    f"{den_trigger_name}_{period}/{offlineQuantity}",
                    comparisonPeriodsDict[period]["label"]
                ])
                lumi += comparisonPeriodsDict[period]["lumi"]

            output_dir = os.path.join(args.output_dir, trigger_name, comparisonPeriodCategory)
            os.makedirs(output_dir, exist_ok=True)
            output_name = os.path.join(output_dir, f"{trigger_name}_{comparisonPeriodCategory}.png")
            efficiencies_plotter(args.merged_file,
                                          hist_label_pairs,
                                          output_name,
                                          comparisonPeriodCategory,
                                          x_range_dict.get(trigger_name),
                                          rebin_dict.get(trigger_name),
                                          trigger_name,
                                          lumi)
            
            if ("PFJet" in trigger_name) and ("Fwd" not in trigger_name):
                for eta_region in regions_labels.keys():
                    hist_pairs_tmp = []
                    for period in comparisonPeriodsDict.keys():
                        hist_pairs_tmp.append([f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_{eta_region}_pt0",
                                                f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_{eta_region}_pt0",
                                                comparisonPeriodsDict[period]["label"]])
                    output_name = os.path.join(output_dir, f"{trigger_name}_{eta_region}_periods.png")
                    efficiencies_plotter(args.merged_file,
                                        hist_pairs_tmp,
                                        output_name,
                                        regions_labels[eta_region],
                                        x_range_dict.get(trigger_name),
                                        rebin_dict.get(trigger_name),
                                        trigger_name,
                                        lumi)
            
            if ("PFJetFwd" in trigger_name):# also partition for forward triggers the two eta regions
                for eta_region in ["HF1","HF2"]:
                    hist_pairs_tmp = []
                    for period in comparisonPeriodsDict.keys():
                        hist_pairs_tmp.append([f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_{eta_region}_pt0",
                                                f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_{eta_region}_pt0",
                                                comparisonPeriodsDict[period]["label"]])
                    output_name = os.path.join(output_dir, f"{trigger_name}_{eta_region}_periods.png")
                    efficiencies_plotter(args.merged_file,
                                        hist_pairs_tmp,
                                        output_name,
                                        regions_labels[eta_region],
                                        x_range_dict.get(trigger_name),
                                        rebin_dict.get(trigger_name),
                                        trigger_name,
                                        lumi)

            for period in comparisonPeriodsDict.keys():
                if ("PFJet" in trigger_name) and ("Fwd" not in trigger_name):
                    if args.is_miniaod:
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
                        efficiencies_plotter(args.merged_file,
                                            hist_label_pairs,
                                            output_name,
                                            period,
                                            x_range_dict.get(trigger_name),
                                            rebin_dict.get(trigger_name),
                                            trigger_name,
                                            lumi)

                        hist_label_pairs = [
                            [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPix_pt0",
                            f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPix_pt0", regions_labels['BPix']],
                            [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPixVeto_pt0",
                            f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPixVeto_pt0", regions_labels['BPixVeto']]
                        ]
                        output_name = os.path.join(output_dir, f"{trigger_name}_{period}_bpix.png")
                        efficiencies_plotter(args.merged_file,
                                            hist_label_pairs,
                                            output_name,
                                            period,
                                            x_range_dict.get(trigger_name),
                                            rebin_dict.get(trigger_name),
                                            trigger_name,
                                            lumi)

                        hist_label_pairs = [
                            [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPix_pt0",
                            f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPix_pt0", regions_labels['FPix']],
                            [f"{trigger_name}_HLTPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPixVeto_pt0",
                            f"{trigger_name}_HLTDenominatorPathAccept_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPixVeto_pt0", regions_labels['FPixVeto']]
                        ]
                        output_name = os.path.join(output_dir, f"{trigger_name}_{period}_fpix.png")
                        efficiencies_plotter(args.merged_file,
                                            hist_label_pairs,
                                            output_name,
                                            period,
                                            x_range_dict.get(trigger_name),
                                            rebin_dict.get(trigger_name),
                                            trigger_name,
                                            lumi)
                    else:
                        hist_label_pairs = [
                            [f"{trigger_name}_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HB_pt0",
                            f"NoSelection/offlineAK4PFPuppiJetsCorrected_leadJet_HB_pt0", regions_labels['HB']],
                            [f"{trigger_name}_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HE1_pt0",
                            f"NoSelection/offlineAK4PFPuppiJetsCorrected_leadJet_HE1_pt0", regions_labels['HE1']],
                            [f"{trigger_name}_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HE2_pt0",
                            f"NoSelection/offlineAK4PFPuppiJetsCorrected_leadJet_HE2_pt0", regions_labels['HE2']],
                            [f"{trigger_name}_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_HF_pt0",
                            f"NoSelection/offlineAK4PFPuppiJetsCorrected_leadJet_HF_pt0", regions_labels['HF']]
                        ]
                        output_name = os.path.join(output_dir, f"{trigger_name}_{period}_eta_ranges.png")
                        efficiencies_plotter(args.merged_file,
                                            hist_label_pairs,
                                            output_name,
                                            period,
                                            x_range_dict.get(trigger_name),
                                            rebin_dict.get(trigger_name),
                                            trigger_name,
                                            lumi)

                        hist_label_pairs = [
                            [f"{trigger_name}_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPix_pt0",
                            f"NoSelection/offlineAK4PFPuppiJetsCorrected_leadJet_BPix_pt0", regions_labels['BPix']],
                            [f"{trigger_name}_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_BPixVeto_pt0",
                            f"NoSelection/offlineAK4PFPuppiJetsCorrected_leadJet_BPixVeto_pt0", regions_labels['BPixVeto']]
                        ]
                        output_name = os.path.join(output_dir, f"{trigger_name}_{period}_bpix.png")
                        efficiencies_plotter(args.merged_file,
                                            hist_label_pairs,
                                            output_name,
                                            period,
                                            x_range_dict.get(trigger_name),
                                            rebin_dict.get(trigger_name),
                                            trigger_name,
                                            lumi)

                        hist_label_pairs = [
                            [f"{trigger_name}_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPix_pt0",
                            f"NoSelection/offlineAK4PFPuppiJetsCorrected_leadJet_FPix_pt0", regions_labels['FPix']],
                            [f"{trigger_name}_{period}/offlineAK4PFPuppiJetsCorrected_leadJet_FPixVeto_pt0",
                            f"NoSelection/offlineAK4PFPuppiJetsCorrected_leadJet_FPixVeto_pt0", regions_labels['FPixVeto']]
                        ]
                        output_name = os.path.join(output_dir, f"{trigger_name}_{period}_fpix.png")
                        efficiencies_plotter(args.merged_file, 
                                            hist_label_pairs, 
                                                output_name, 
                                                period,
                                                x_range_dict.get(trigger_name), 
                                                rebin_dict.get(trigger_name),
                                                trigger_name,
                                                lumi)

                


