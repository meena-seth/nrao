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
cylAy_slice = slice(0, 256)
cylAy = beam_dset[:,:,cylAy_slice,:]

# Make some (possibly) useful slices 
cylAy_ha0 = cylAy[:, 0, 9, ha_idx]        # Values for every freq at HA=0
cylAy_fre716 = cylAy[freq_idx, 0, 9, :]   # Values for every HA at freq=716

# Potentially make some plots 
fig, ax = plt.subplots(constrained_layout=True, figsize=(8,8))
ax.scatter(has, cylAy_fre716, s=0.5)
ax.legend()
ax.set_xlabel("HA")
ax.set_title("CylA, y pol, beam 9, 716 MHz")
fig.savefig("cylA_HAs_vs_values.png")
print(f"Figure 1 saved")

fig, ax = plt.subplots(constrained_layout=True, figsize=(8,8))
ax.scatter(freqs, cylAy_ha0)
ax.legend()
ax.set_xlabel("Frequencies")
ax.set_title("CylA, y pol, Beam 9, HA=0")
fig.savefig("cylA_freq_vs_values.png")
print(f"Figure 2 saved")