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

# Get index of frequency we want
target_freq = 716
freq_idx = np.argmin(np.abs(freqs- target_freq))

# Slice out just the data for Cylinder D, y polarization
cylDy_slice = slice(1536, 1792)
cylDy = beam_dset[:,:,cylDy_slice,:]

# Make the slice I want 
cylDy_fre716 = cylDy[freq_idx, 0, 9, :]  # Values for every HA at freq=716
cylDy_fre716 = np.abs(cylDy_fre716)/np.max(np.abs(cylDy_fre716))

# Plot 
fig, ax = plt.subplots(constrained_layout=True, figsize=(10,5))
ax.scatter(has, cylDy_fre716, s=0.5)
ax.set_xlabel("HA")
ax.set_ylabel("Relative sensitivity?")
ax.set_yscale("log")
ax.set_title("CylD, yy pol, beam 9, 716 MHz")
fig.savefig("Plot_One")
