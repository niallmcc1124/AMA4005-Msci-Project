##The Final script in regard to VDOS, this script takes the extended VDOS data and normalizes it so that the integral of the VDOS equals 3N, where N is the number of atoms. 
# This normalization is important for comparing the VDOS to theoretical predictions and experimental data. 
# The script also converts the frequency from THz to cm^-1 for better comparison with experimental spectra, and generates a plot of the normalized VDOS as a function of frequency. 
# Finally you have a piece of code that is useful

import numpy as np
import matplotlib.pyplot as plt

# --- user/system parameters ---
N_atoms = 62
threeN  = 3 * N_atoms

# --- 1. Load VDOS in THz ---
data = np.loadtxt("vdos_extended.dat")
freq_THz = data[:,0]
vdos_raw = data[:,1]

# --- 2. Make spectrum positive ---
vdos_pos = np.abs(vdos_raw)

# --- 3. Convert THz -> cm^-1 ---
# 1 THz = 33.3564095 cm^-1
freq_cm = freq_THz * 33.3564095

# --- 4. Normalize so ∫ D(ω) dω = 3N ---
# Use numpy.trapezoid instead of np.trapz
integral = np.trapezoid(vdos_pos, freq_cm)
vdos_norm = vdos_pos * (threeN / integral)

print(f"Integral after normalization: {np.trapezoid(vdos_norm, freq_cm):.3f}")

# --- 5. Save normalized VDOS ---
np.savetxt("vdos_norm_cm.dat", np.column_stack((freq_cm, vdos_norm)))

# --- 6. Plot ---
plt.plot(freq_cm[::25], vdos_norm[::25], label="NNP VDOS (normalized)")
plt.xlim(0, 4000)
plt.xlabel(r"$\omega\ (\mathrm{cm}^{-1})$")
plt.ylabel(r"$D(\omega)$")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("vdos_norm_cm.png", dpi=300)
plt.show()

#print("Ta-da!")