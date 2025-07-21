# Let's just try to load in the data we need to plot power beam vs. HA for:
# CylD, y polarization, and a freq of 600 MHz.

import h5py

filename = "/project/rpp-chime/areda26/stuff_for_other_people/hsiu-hsien/TauA_105/2667/TAU_A_2667_20181014T120212.h5"

f = h5py.File(filename, "r")

beam_dset = f["beam"] # beam_dset is an instance of h5py.Dataset
beam = beam_dset[:] # using the square brackets, beam is now a numpy array of shape (1024, 2, 2048, 2160)

# axes labels are provided in the Dataset attrs if needed
axes_names = beam_dset.attrs["axis"]

# individual cylinder and polarization slices; these go into the third axis above
cylDy = slice(1536, 1792)
# Take a look at what's in the slice 
print(f"cylDy is: {cylDy}")
