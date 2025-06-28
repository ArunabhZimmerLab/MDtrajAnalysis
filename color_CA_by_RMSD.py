from pymol import cmd
import numpy as np

def color_CA_by_custom_value(pdb_filename):
    value_dict = {}

    # Parse the value from each line in the PDB file
    with open(pdb_filename, 'r') as pdb:
        for line in pdb:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                try:
                    resi = int(line[22:26])
                    value = float(line[62:66])
                    value_dict[resi] = value
                except ValueError:
                    continue

    if not value_dict:
        print("No CA atoms with valid values found.")
        return

    # Normalize values between 0 and 1
    values = np.array(list(value_dict.values()))
    min_val, max_val = np.min(values), np.max(values)
    norm_values = {resi: (val - min_val) / (max_val - min_val) for resi, val in value_dict.items()}

    # Apply color gradients from red → white → blue
    for resi, norm_val in norm_values.items():
        if norm_val < 0.5:
            r = 1.0
            g = b = 2 * norm_val
        else:
            b = 1.0
            r = g = 2 * (1 - norm_val)
        color_name = f"color_{resi}"
        cmd.set_color(color_name, [r, g, b])
        cmd.color(color_name, f"resi {resi} and name CA")

# Example usage inside PyMOL (replace 'your.pdb' with your actual PDB file)
# color_CA_by_RMSD("your.pdb")
