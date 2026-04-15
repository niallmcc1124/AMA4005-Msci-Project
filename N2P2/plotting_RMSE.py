##PLots the SE because it is nicer than looking at a CSV file any day of the week.
##The .csv file produced is incredibly handy to then further add frames into the training set
##just not asthetically pleasing!

import numpy as np
import matplotlib.pyplot as plt

# Load CSV: timestep, rmse
data = np.loadtxt("rmse_results3.0.csv", delimiter=",", skiprows=1)

timesteps = data[:, 0]
rmse = data[:, 1]

# --- Settings ---
start_frame = 0
end_frame   = 2560
chunk       = 1      # sample every 100 frames (change as needed)
# -----------------

# Slice the region, then downsample
timesteps_slice = timesteps[start_frame:end_frame:chunk]
rmse_slice      = rmse[start_frame:end_frame:chunk]

plt.figure(figsize=(8,5))
plt.plot(timesteps_slice, rmse_slice, marker="o", linewidth=1.5)

plt.xlabel("Timestep")
plt.ylabel("S.E (meV/Å)")
#plt.xscale('log')
plt.yscale('log')
#plt.title(f"RMSE from frame {start_frame} to {end_frame}, sampled every {chunk}")
plt.grid(True)

plt.tight_layout()
plt.savefig(f"rmse_{start_frame}_{end_frame}_sampled_log.png")
plt.show()

#print("Ta-da!")
