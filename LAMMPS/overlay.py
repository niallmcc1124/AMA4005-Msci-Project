
##Can create a figure to show if the tenoerature calcualted in the Debye_temp.py script is a good fit to the low temperature behavior of Cv.
##This script reads the Cv(T) data, computes the Debye model prediction for Cv using the fitted Debye temperature, and generates a plot comparing the computed Cv from the NNP with the Debye model prediction at low temperatures. 
##You can adjust the temperature range for the plot to focus on the low-temperature region where the Debye model is expected to be valid. 
##This creates some lovely figures
import numpy as np
import matplotlib.pyplot as plt

# Load your computed Cv(T)
data = np.loadtxt("Cv_vs_T.dat")
T = data[:,0]
Cv = data[:,1]

# Constants
kB = 1.380649e-23
N_atoms = 62

# Debye model (low-T cubic form)
def debye_lowT(T, ThetaD):
    pref = (12 * np.pi**4 / 5) * N_atoms * kB
    return pref * (T / ThetaD)**3

# Two Debye temperatures to compare
#Theta_woll = 528.0   # K
theta_80 = 662.7359770126964 # K (80 K fit)
Theta_tober = 546.0  # K (your fitted value)
theta_40 = 506.94271048032823 # K (40 K fit)
theta_30 = 469.29537430358783 # K (30 K fit)

#Cv_woll = debye_lowT(T, Theta_woll)
Cv_tober = debye_lowT(T, Theta_tober)
Cv_40 = debye_lowT(T, theta_40)
Cv_30 = debye_lowT(T, theta_30)
Cv_80 = debye_lowT(T, theta_80)

# Plot only low-T region (0–100 K)
mask = T < 100

plt.plot(T[mask], Cv[mask], label="NNP Cv(T)", linewidth=2)
#plt.plot(T[mask], Cv_woll[mask], "--", label="Debye model (528 K)")
plt.plot(T[mask], Cv_30[mask], "--", label="T<30 K fit (469.3 K)")
plt.plot(T[mask], Cv_40[mask], "--", label="T<40 K fit (506.9 K)")
plt.plot(T[mask], Cv_tober[mask], "--", label="T<50 K fit (546 K)")
plt.plot(T[mask], Cv_80[mask], "--", label="T<80 K fit (662.7 K)")

plt.xlabel("Temperature (K)")
plt.ylabel(r"$C_V$ (J/K per supercell)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("Cv_overlay.png", dpi=300)
plt.show()

#print("Ta-da!")