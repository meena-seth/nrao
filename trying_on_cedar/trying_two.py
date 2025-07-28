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
ha_idx = np.argmin(nb.abs(has - center_HA))

# Slice out just the data for Cylinder D, y polarization
cylDy_slice = slice(1536, 1792)
cylDy = beam_dset[:,:,cylDy_slice,:]

# Make some useful slices 
cylDy_ha0 = cylDy[:, 0, 9, ha_idx]
cylDy_fre716 = cylDy[freq_idx, 0, 9, :]

# Potentially make some plots 
