import h5py
import numpy as np
import matplotlib.pyplot as plt


filename = "/project/rpp-chime/areda26/stuff_for_other_people/hsiu-hsien/TauA_105/2667/TAU_A_2667_20181014T120212.h5"

f = h5py.File(filename, "r")

import pdb; pdb.set_trace()

beam_dset = f["beam"] # beam_dset is an instance of h5py.Dataset
axes_names = beam_dset.attrs["axis"]
index_map = f["index_map"]

ha = index_map["pix"]["phi"][:]
freq = index_map["freq"][:]

freq_idx = np.where(freq==716)


cylDy_slice = slice(1536, 1792)
cylDy_data = beam_dset[:,:,cylDy_slice,:]

cylDy = cylDy_data[freq_idx, 0, 9, :]
cylDy = np.squeeze(cylDy)
