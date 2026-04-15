##Right youve got your VDOS you have a heat cacapity and thinking what else can I do with it
##Well, you can extract the Debye temperature from the low-temperature behavior of Cv.
##The Debye model predicts that at low temperatures, Cv ~ (T/ThetaD)^3, where ThetaD is the Debye temperature. 
##By fitting the low-T portion of the Cv vs T data to this form, you can estimate ThetaD, which gives insight into the vibrational properties of the material. 
##This script performs that fitting and prints out the estimated Debye temperature. You can adjust the temperature range used for fitting based on where the low-T behavior is most apparent in your Cv data.

import numpy as np
from scipy.optimize import curve_fit

# load Cv(T)
data = np.loadtxt("Cv_vs_T.dat")
T = data[:,0]
Cv = data[:,1]

N_atoms = 62
kB = 1.380649e-23

# use low-T region
mask = T < 80
T_low = T[mask]
Cv_low = Cv[mask]

def debye_lowT(T, ThetaD):
    pref = (12 * np.pi**4 / 5) * N_atoms * kB
    return pref * (T / ThetaD)**3

popt, pcov = curve_fit(debye_lowT, T_low, Cv_low)
ThetaD = popt[0]

print("Debye temperature (K):", ThetaD)
#print("Ta-da!")