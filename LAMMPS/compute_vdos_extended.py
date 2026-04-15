##Similar to compute_vdos.py but uses more points from the VACF to reach Higher frequencies. 
# Adjust the number of points based on noise levels in the VACF. 
# The script also includes windowing to reduce noise in the FFT and normalizes the VDOS for better visualization. 
# Finally, it saves the extended VDOS data to a file and generates a plot of the VDOS as a function of frequency.

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft, rfftfreq

# --- 1. Load VACF ---
data = np.loadtxt("vacf.dat")
vacf = data[:,1]

# --- 2. Use more points to reach OH stretch ---
vacf = vacf[:80000]   # adjust to 50000–100000 depending on noise

# --- 3. Time step (2.5 fs) ---
dt = 2.5e-15

# --- 4. Windowing ---
window = np.hanning(len(vacf))
vacf_win = vacf * window

# --- 5. FFT ---
spec = np.real(rfft(vacf_win))
freq_Hz = rfftfreq(len(vacf_win), dt)
freq_THz = freq_Hz * 1e-12

# Normalize
vdos = spec / spec.max()

np.savetxt("vdos_extended.dat", np.column_stack((freq_THz, vdos)))

# --- 6. Plot ---
plt.plot(freq_THz, vdos)
plt.xlim(0, 150)  # show up to 150 THz
plt.xlabel("Frequency (THz)")
plt.ylabel("VDOS (arb. units)")
plt.grid(True)
plt.tight_layout()
plt.savefig("vdos_extended.png", dpi=300)
plt.show()

#print("Ta-da!")