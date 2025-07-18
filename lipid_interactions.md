# PDB Trajectory Lipid and Protein Interaction Analysis

This repository contains a Jupyter Notebook (`.ipynb`) designed for analyzing molecular dynamics (MD) PDB trajectories. It focuses on characterizing lipid membrane properties (phosphorus atom distributions, lipid Centers of Geometry) and quantifying protein-lipid interactions. for efficient processing of large trajectory files. It should work on Google Colab as well, although I haven't tested it yet.

## What does this script do?

* To efficiently reade large PDB trajectory files by distributing the workload across multiple CPU cores, the script is parallelized using Python's `multiprocessing` module. 
* A user can specify any lipid residue IDs present in their PDB file for analysis.
* Eventually it generates 2D density heatmaps (X-Y, X-Z, Y-Z planes) of phosphorus atoms for each specified lipid type, providing insights into membrane organization.
* It also calculates and visualizes the 2D density heatmaps (X-Y plane) of lipid COGs for each specified lipid type, both with and without an overlay of the protein's CA atoms' trace from the first model, offering structural context. A standalone CA trace plot is also generated, in case one needs it.
* Quantifies the contact frequency between protein residues and specified lipid types based on a distance cutoff. This has to be refined, but the user can use the csv output for their own visualization.
* All generated numerical data (heatmap densities, bin edges, CA coordinates, interaction frequencies) are automatically exported to CSV files.
* The script has a dedicated block in which user can edit some of the parameters, so that they don't have to edit the entire script. 
* I have also included an optional "test mode" for quickly running the analysis on a subset of frames for debugging or previewing results.

## Requirements

* Python 3.x
* `numpy`
* `matplotlib`
* `seaborn`

You can install these dependencies using pip:

```bash
pip install numpy matplotlib seaborn
How to Use
Clone the Repository:

Bash

git clone https://github.com/ArunabhZimmerLab/MDtrajAnalysis.git
cd MDtrajAnalysis

Download your PDB Trajectory:
Place your .pdb trajectory file (e.g., EMT_t5.pdb) in the same directory as the Jupyter Notebook, or provide its full path.

Launch Jupyter Notebook:

Bash

jupyter notebook
This will open a browser window with the Jupyter interface.

Open and Run the Notebook:

Navigate to and open the lipid_analysis.ipynb file.

Run the cells sequentially.

Provide Inputs when Prompted:

The notebook will prompt you to enter the path to your PDB trajectory file.

Example: EMT_t5.pdb (if in the same directory) or /path/to/your/EMT_t5.pdb

It will then prompt you to enter the lipid residue IDs you wish to analyze, separated by spaces.

Example: POPG POPE PMCL or PMPC POPC CHOL

Output
The script will generate several plots (saved as .png files) and corresponding data files (saved as .csv files) in a newly created csv_data directory.

Generated Files Include:

Heatmaps:

heatmap_{LIPID_ID}_COG_XY_*.png: 2D density heatmap of lipid COGs (X-Y plane). The first lipid's heatmap will also include an overlay of the protein's CA trace.

heatmap_{LIPID_ID}_P_atom_XY/XZ/YZ_*.png: 2D density heatmaps of phosphorus atoms for each lipid (X-Y, X-Z, and Y-Z planes).

CA Trace:

plot_ca_trace_xy_only_transparent_*.png: A standalone plot of the protein's alpha-carbon trace.

Interaction Frequencies:

interaction_frequency_{LIPID_ID}_chain_{CHAIN_ID}_*.png: Plots showing the contact frequency of each specified lipid with protein residues per chain.

CSV Data Files (in csv_data directory):

heatmap_{LIPID_ID}_COG_XY_density_*.csv: Raw density data for lipid COG heatmaps.

heatmap_{LIPID_ID}_COG_XY_x_edges_*.csv: X-axis bin edges for lipid COG heatmaps.

heatmap_{LIPID_ID}_COG_XY_y_edges_*.csv: Y-axis bin edges for lipid COG heatmaps.

heatmap_{LIPID_ID}_P_atom_XY/XZ/YZ_density_*.csv: Raw density data for phosphorus atom heatmaps.

heatmap_{LIPID_ID}_P_atom_XY/XZ/YZ_x_edges_*.csv: X-axis bin edges for phosphorus atom heatmaps.

heatmap_{LIPID_ID}_P_atom_XY/XZ/YZ_y_edges_*.csv: Y-axis bin edges for phosphorus atom heatmaps.

ca_trace_model1_chain_{CHAIN_ID}_coords_*.csv: X, Y, Z coordinates of alpha-carbon atoms for each protein chain in Model 1.

interaction_frequency_{LIPID_ID}_chain_{CHAIN_ID}_*.csv: Residue number and corresponding contact frequency for protein-lipid interactions.

(Note: * in filenames will be replaced by _full_data if running on all frames, or _first_{MAX_TEST_FRAMES}_frames_per_chunk if TEST_MODE_ENABLED is True.)

Configuration Parameters
You can modify the following parameters in the first code cell of the notebook:

num_heatmap_bins: Number of bins for the 2D histograms (heatmaps). Higher values mean finer resolution but more computation.

interaction_cutoff: Distance (in Angstroms) used to define a contact between a protein atom and a lipid phosphorus atom.

NUM_CORES: Number of CPU cores to use for parallel processing. Defaults to your system's available cores.

TEST_MODE_ENABLED: Set to True to process only a subset of frames for quick testing.

MAX_TEST_FRAMES: The number of frames to process per worker in TEST_MODE_ENABLED.

protein_chains_to_monitor: A set of chain IDs that correspond to your protein(s).

non_protein_resnames_base: A base list of residue names to exclude when identifying protein atoms (e.g., water, ions). The user-specified lipids are dynamically removed from this list to ensure they are treated as lipids, not non-protein.

Example Usage (Conceptual)
After running the notebook, you would see output similar to this in your Jupyter environment and generated files in the csv_data folder:

--- Starting Parallel PDB Parsing with 12 cores ---
Analyzing PDB file: EMT_t5.pdb
Lipids to analyze: POPG, POPE, PMCL
Found 1000 MODEL records (frames).
Worker 1 will process frames from MODEL 1 to MODEL 84
...
Parallel file parsing completed. Total frames processed by workers: 1000 in 123.4567 seconds.

--- Calculating Centers of Geometry for specified lipids ---
Calculated COGs for 50000 POPG residues.
Calculated COGs for 30000 POPE residues.
Calculated COGs for 20000 PMCL residues.
Prepared CA data for chains: ['A', 'B', 'C', 'D'] from Model 1.

--- Generating Plots and Exporting Data ---

--- Generating Lipid COG Heatmaps and CA Trace Overlays ---
Exported POPG COG Heatmap (X-Y) data to CSV: /path/to/csv_data/heatmap_POPG_COG_XY_full_data.csv
Overlaying CA trace on POPG COG heatmap...
Exported CA Trace Model 1 Chain A data to CSV: /path/to/csv_data/ca_trace_model1_chain_A_coords_full_data.csv
... (plot for POPG COG with CA trace) ...

Exported POPE COG Heatmap (X-Y) data to CSV: /path/to/csv_data/heatmap_POPE_COG_XY_full_data.csv
... (plot for POPE COG without CA trace) ...

--- CA Trace XY Only Plot ---
... (standalone CA trace plot) ...

--- Generating Phosphorus Atom Heatmaps for all specified lipids ---
Exported POPG P Atom Heatmap (X-Y) data to CSV: /path/to/csv_data/heatmap_POPG_P_atom_xy_full_data.csv
... (plots and CSV exports for all P-atom heatmaps for all lipids) ...

--- Generating Protein-Lipid Interaction Frequency Plots and Exporting Data ---
Processing interaction data for POPG...
Exported interaction frequency for POPG Chain A to CSV: /path/to/csv_data/interaction_frequency_POPG_chain_A_full_data.csv
... (plots and CSV exports for all protein-lipid interactions) ...

--- All Plots Generated and Data Exported ---
License
(Optional: Add your preferred license, e.g., MIT, Apache 2.0, etc.)

Contact
For any questions or issues, please open an issue on this GitHub repository.
