import h5py
import numpy as np
import matplotlib.pyplot as plt


filename = "/project/rpp-chime/areda26/stuff_for_other_people/hsiu-hsien/TauA_105/2667/TAU_A_2667_20181014T120212.h5"

f = h5py.File(filename, "r")

import pdb; pdb.set_trace()

beam_dset = f["beam"] # beam_dset is an instance of h5py.Dataset

cylDy_slice = slice(1536, 1792)
cylDy = beam_dset[:,:,cylDy_slice,:]


# axes labels are provided in the Dataset attrs if needed
axes_names = beam_dset.attrs["axis"]
# the axis definitions are supplied in `index_map`
index_map = f["index_map"]

# get the hour angle axis
ha = index_map["pix"]["phi"][:]

# get the frequency axis
freqs = index_map["freq"][:]

# if the declination is needed, for instance for calculating degrees on sky from hour angle, there's an attribute for that
dec = f.attrs["dec"]

target_freq = 716
freq_idx = np.argmin( np.abs(freqs - target_freq) )
print(f"716 MHz is at index {freq_idx}")

cylDy_one = cylDy[0, 0, :, :]
print(f"716MHz, pol index 0, all inputs, all ha: {cylDy_one.shape}")

cylDy_three = cylDy[freq_idx, 0, 9, :]


cylDy_two = cylDy_one.sum(axis=0)
print(f"cylDy.sum(axis=0): {cylDy_two.shape}, {len(cylDy_two)}")

## 
output_folder = '/scratch/mseth2/plots'
os.makedirs(output_)