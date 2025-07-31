import numpy as np
import sys
from matplotlib import pyplot as plt
fn = sys.argv[1]

data = np.load(fn,allow_pickle=True)
spectra = data['spectra']
median_timeseries = data['median_timeseries']
median_ts = np.mean(spectra, axis=0)
plt.figure()
plt.plot(median_ts, label='Median Spectrum')
plt.plot(median_timeseries, label='Median Timeseries in data')
#plot the spectra at the beam
peak_ind = np.argmax(median_ts)
spectra_at_peak = spectra[:, peak_ind]
spectra_at_peak[spectra_at_peak==0] = np.nan  # Replace zeros with NaN for better visualization
plt.figure()
plt.scatter(np.arange(len(spectra_at_peak)), spectra_at_peak, label='Spectra at Peak',s=1)
# plt.show()
# plt.yscale('log')

from beam_model import composite
from beam_model import utils as u
cbm = composite.CompositeBeamModel()
CygA_RA = 299.8681525
CygA_Dec = 40.7339156
from datetime import datetime
from datetime import timedelta
#create a datetime array for all of 2020-02-17
# 1 second steps
from frb_calibration import intensity_calibration_helpers as ich
time, beam = ich.get_calibrator_transit(CygA_RA, CygA_Dec, "20200217")
#convert time to datetime
start_date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f UTC+0000')- timedelta(minutes=10)
date_time_arr = [start_date + timedelta(seconds=i) for i in range(1200)]
x_arr = []
y_arr = []
sensitivity_arr = []
for date_time in date_time_arr:
    x, y = cbm.get_position_from_equatorial(CygA_RA, CygA_Dec, date_time)
    x_arr.append(x)
    y_arr.append(y)

x_arr = np.array(x_arr)
y_arr = np.array(y_arr)
freq_low = 400.390625 # MHz
freq_high = 800 # MHz
#there's 16384 channels in the band
freqs = np.linspace(freq_low, freq_high, 16384)/1000 # convert to GHz
sensitivity = cbm.get_sensitivity([1105], np.array([x_arr, y_arr]).T, freqs*1000).squeeze()
#average over the spectra axis
mean_sensitivity = np.nanmean(sensitivity, axis=1)
#find the peak of the mean sensitivity
peak_sensitivity_ind = np.argmax(mean_sensitivity)
#get response at the peak
sensitivity_at_peak = sensitivity[peak_sensitivity_ind, :]
#divide the spectra at peak by the sensitivity at peak
spectra_at_peak *= sensitivity_at_peak
plt.figure()
plt.plot(freqs, sensitivity_at_peak, label='Sensitivity at Peak')

#correct to jansky units
spectra_at_peak /= (1024*0.8)**2*128/4/4/0.806745/400
#get the spectrum of cyga
a0 = 3.34598
a1 = -1.0022
a2 = -0.225
a3 = 0.023
a4= 0.043
log_flux = a0 + a1 * np.log10(freqs) + a2 * np.log10(freqs)**2 + a3 * np.log10(freqs)**3 + a4 * np.log10(freqs)**4
#correct the spectra at peak by the beam model

plt.figure()
plt.plot(freqs, 10**log_flux, label='CygA Spectrum')
plt.plot(freqs, spectra_at_peak, label='CygA Spectrum at Peak')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Flux Density (Jy)')
plt.show()
plt.imshow(sensitivity, aspect='auto', extent=(freq_low, freq_high, 0, 1200), origin='lower')
plt.show()