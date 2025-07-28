import h5py

filename = "/project/rpp-chime/areda26/stuff_for_other_people/hsiu-hsien/TauA_105/2667/TAU_A_2667_20181014T120212.h5"

f = h5py.File(filename, "r")

beam_dset = f["beam"] # beam_dset is an instance of h5py.Dataset
beam = beam_dset[:] # using the square brackets, beam is now a numpy array of shape (1024, 2, 2048, 2160)

# axes labels are provided in the Dataset attrs if needed
axes_names = beam_dset.attrs["axis"]

# there is a corresponding weight dataset if needed:
weight = f["weight"][:] # same shape as above; weight is defined as 1 / sigma^2 i.e. inverse variance

# individual cylinder and polarization slices; these go into the third axis above
#cylAy = slice(0, 256)
#cylBy = slice(512, 768)
#cylCy = slice(1024, 1280)
cylDy = slice(1536, 1792)

#cylAx = slice(256, 512)
#cylBx = slice(768, 1024)
#cylCx = slice(1280, 1536)
#cylDx = slice(1792, 2048)

# the axis definitions are supplied in `index_map`
index_map = f["index_map"]

# get the hour angle axis
ha = index_map["pix"]["phi"][:]

# get the frequency axis
freq = index_map["freq"][:]

# if the declination is needed, for instance for calculating degrees on sky from hour angle, there's an attribute for that
dec = f.attrs["dec"]

#print(f" The beam is an array with shape {beam.shape}.")
#print(f" The axes names are {axes_names}.")
#print(f"The weight dataset is an array with shape {weight.shape}.")
#print(f"The index map is {index_map}.")
#print(f"The ha is {ha}, the dec is {dec}, and the frequency axis is {freq}.")

#print(f"cylDy is: {cylDy}.")

cylinder_D = beam[:, :, cylDy, :]
#print(cylinder_D)
#print(cylinder_D.shape)

import matplotlib.pyplot as plt

cylD_freq = cylinder_D[0]
cylD_pol = cylinder_D[1]
cylD_input = cylinder_D[2]
cylD_pix = cylinder_D[3]

print(f''' freq: {cylD_freq}, {cylD_freq.shape}, {len(cylD_frew)}
           pol:  {cylD_pol}, {cylD_pol.shape}, {len(cylD_pol)}
           input = {cylD_input}, {cylD_input.shape}, {len(cylD_input)}
           pix = {cylD_pix}, {cylD_pix.shape}, {len(cylD_pix)}
''')
