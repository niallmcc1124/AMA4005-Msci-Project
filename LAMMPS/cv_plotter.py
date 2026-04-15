###This script reads the normalized vibrational density of states (VDOS) from a file,
#  computes the specific heat capacity at constant volume (Cv) as a function of temperature using the VDOS, and saves the Cv data to a file.
# It also generates a plot of Cv as a function of temperature.
# The script uses the quantum harmonic oscillator model to calculate Cv from the VDOS, 
# and includes a numerical integration step to perform the necessary calculations.
##Assumes you have ran the vacf and vdos python scripts first which is what you would do obviously, but just to be clear you need to have the vdos_norm_cm.dat file in the same directory as this script for it to work.
import numpy as np
import matplotlib.pyplot as plt

# constants
hbar = 1.054571817e-34       # J·s
kB   = 1.380649e-23          # J/K
c    = 2.99792458e10         # cm/s

# load normalized VDOS in cm^-1
data = np.loadtxt("vdos_norm_cm.dat")
nu_cm = data[:,0]
Dnu   = data[:,1]            # ∫ Dnu d(nu_cm) = 3N

# convert to angular frequency ω and D(ω)
omega = 2 * np.pi * c * nu_cm          # rad/s
Domega = Dnu / (2 * np.pi * c)         # so ∫ Domega dω = 3N

T = np.linspace(5, 1000, 400)
Cv = np.zeros_like(T)

def integrand(omega, T):
    x = (hbar * omega) / (kB * T)
    out = np.zeros_like(x)

    small = x < 1e-3
    xs = x[small]
    out[small] = 1 - xs/2 + xs**2/12

    mid = (x >= 1e-3) & (x < 50)
    xm = x[mid]
    exm = np.exp(-xm)
    out[mid] = xm**2 * exm / (1 - exm)**2

    return out

for i, Ti in enumerate(T):
    Cv[i] = kB * np.trapezoid(Domega * integrand(omega, Ti), omega)

np.savetxt("Cv_vs_T.dat", np.column_stack((T, Cv)))

plt.plot(T, Cv)
plt.xlabel("Temperature (K)")
plt.ylabel(r"$C_V$ (J/K per supercell)")
plt.grid(True)
plt.tight_layout()
plt.savefig("Cv_vs_T.png", dpi=300)
plt.show()

#print("Ta-da!")