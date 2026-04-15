##This script reads the velocity autocorrelation function (VACF) from a file, computes the vibrational density of states (VDOS) using a Fourier transform, and saves the VDOS to a file. 
# It also generates a plot of the VDOS as a function of frequency. 
# The script includes optional windowing to reduce noise in the FFT and normalizes the VDOS for better visualization.

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft, rfftfreq

# --- 1. Load VACF and optionally truncate tail ---
data = np.loadtxt("vacf.dat")
vacf = data[:,1]

# keep first 10000 points to avoid noisy tail
vacf = vacf[:10000]

# --- 2. Define time step (in seconds) ---
dt = 2.5e-15  # 2.5 fs

# --- 3. Windowing (optional but helps) ---
window = np.hanning(len(vacf))
vacf_win = vacf * window

# --- 4. FFT to get VDOS ---
spec = np.real(rfft(vacf_win))
freq_Hz = rfftfreq(len(vacf_win), dt)
freq_THz = freq_Hz * 1e-12

# normalize (up to an overall constant)
vdos = spec / spec.max()

np.savetxt("vdos.dat", np.column_stack((freq_THz, vdos)))

# --- 5. Plot ---
plt.plot(freq_THz, vdos)
plt.xlim(0, 40)  # adjust as needed
plt.xlabel("Frequency (THz)")
plt.ylabel("VDOS (arb. units)")
plt.grid(True)
plt.tight_layout()
plt.savefig("vdos.png", dpi=300)
plt.show()

#print("Ta-da!")