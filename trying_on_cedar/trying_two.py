import h5py 
import numpy as np
import matplotlib.pyplot as plt

# Load in the data file
filename = "/project/rpp-chime/areda26/stuff_for_other_people/hsiu-hsien/TauA_105/2667/TAU_A_2667_20181014T120212.h5"
f = h5py.File(filename, "r")
import pdb; pdb.set_trace()
beam_dset = f["beam"] 

# Read axes names & make array for freqs and HAs
axes_names = beam_dset.attrs["axis"]
index_map = f["index_map"]

has = index_map["pix"]["phi"][:]
freqs = index_map["freq"][:]

# Get indices for target freqs & center HA 
target_freq = 716
freq_idx = np.argmin(np.abs(freqs- target_freq))

center_HA = 0
ha_idx = np.argmin(np.abs(has - center_HA))

# Slice out just the data for Cylinder D, y polarization
cylDy_slice = slice(1536, 1792)
cylDy = beam_dset[:,:,cylDy_slice,:]

# Make some (possibly) useful slices 
cylDy_ha0 = cylDy[:, 0, 9, ha_idx]        # Values for every freq at HA=0
cylDy_fre716 = cylDy[freq_idx, 0, 9, :]   # Values for every HA at freq=716

# Potentially make some plots 
fig, ax = plt.subplots(constrained_layout=True, figsize=(8,8))
ax.scatter(has, cylDy_fre716, s=0.5)
ax.legend()
ax.set_xlabel("HA")
ax.set_title("CylD, y pol, beam 9, 716 MHz")
fig.savefig("HAs_vs_values.png")
print(f"Figure 1 saved")

fig, ax = plt.subplots(constrained_layout=True, figsize=(8,8))
ax.scatter(freqs, cylDy_ha0)
ax.legend()
ax.set_xlabel("Frequencies")
ax.set_title("CylD, y pol, Beam 9, HA=0")
fig.savefig("freq_vs_values.png")
print(f"Figure 2 saved")