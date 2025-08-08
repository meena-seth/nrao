import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import pdb

import datetime

pdb.set_trace()

from iautils import cascade

from datetime import datetime
from astropy.coordinates import SkyCoord

sys.path.insert(0, os.path.abspath('beam-model'))
from beam_model import utils, formed

#### Load in files ####

files = np.load("/arc/projects/chime_frb/mseth/Crab_Filepaths_1.npz")
crab_norescaled_filepaths = files['filepath']

#### Define source coordinates ####

source_name = "TAU_A"
coords = SkyCoord.from_name(source_name)
source_ra = coords.ra.deg
source_dec = coords.dec.deg

#### Getting initial parameters #### 

max_tidxs = []
max_timestamps = []
spectra_at_peak = []
beam_ids = []
has = []
y_at_peak = []


for file in crab_norescaled_filepaths:
    cascade_obj = cascade.load_cascade_from_file(file)
    cascade_obj.dm = 56.7    #Dedisperse 
    
    peaks = []
    
    for beam in cascade_obj.beams: #Find index of max beam
        beam.subband(256,56.7,apply_weights=False)
        mean_ts = np.nanmean(beam.intensity, axis=0)
        mean_ts_masked = mean_ts[400:500]
        offpeak_mean = np.nanmean(mean_ts_masked)
    
        subtracted_ts = mean_ts - offpeak_mean
    
        peak = np.max(subtracted_ts)
        peaks.append(peak)
    
    max_beam_idx = np.argmax(peaks)
    
    pdb.set_trace()
    
    max_beam = cascade_obj.beams[max_beam_idx]
    ts = np.nansum(max_beam.intensity, axis=0)
    
    max_tidx = np.argmax(ts)
    max_timestamp = cascade_obj.event_time 
    spectrum = max_beam.intensity[:, max_tidx]
    beam_id = int(beam.beam_no)
    x, y = utils.get_position_from_equatorial(source_ra, source_dec, max_timestamp)

    max_tidxs.append(max_tidx)
    max_timestamps.append(max_timestamp)
    spectra_at_peak.append(spectrum)
    beam_ids.append(beam_id)
    has.append(x)
    y_at_peak.append(y)
    
    del cascade_obj
    