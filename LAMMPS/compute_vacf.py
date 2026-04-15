##This script reads velocities from a LAMMPS dump file, computes the velocity autocorrelation function (VACF), and saves it to a file.
#  It also generates a plot of the VACF on a logarithmic time scale. 
# The script is designed to handle large datasets by downsampling the velocity data to avoid O(T^2) computational complexity when calculating the VACF.

import numpy as np
import matplotlib.pyplot as plt

dump_file = "dump.traj"

# ------------------------------------------------------------
# 1. Read velocities from LAMMPS dump
# ------------------------------------------------------------

def read_lammps_velocities(filename):
    frames = []
    ids_ref = None

    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break

            if not line.startswith("ITEM: TIMESTEP"):
                continue

            # TIMESTEP
            f.readline()

            # NUMBER OF ATOMS
            f.readline()
            natoms = int(f.readline().strip())

            # BOX BOUNDS (skip)
            f.readline()
            for _ in range(3):
                f.readline()

            # ATOMS header
            header = f.readline().strip().split()
            cols = header[2:]  # skip "ITEM: ATOMS"

            id_idx = cols.index("id")
            vx_idx = cols.index("vx")
            vy_idx = cols.index("vy")
            vz_idx = cols.index("vz")

            ids = []
            vels = []

            for _ in range(natoms):
                parts = f.readline().split()
                ids.append(int(parts[id_idx]))
                vels.append([
                    float(parts[vx_idx]),
                    float(parts[vy_idx]),
                    float(parts[vz_idx]),
                ])

            ids = np.array(ids)
            vels = np.array(vels)

            # Ensure consistent ordering
            if ids_ref is None:
                order = np.argsort(ids)
                ids_ref = ids[order]
            else:
                order = np.argsort(ids)
                if not np.array_equal(ids[order], ids_ref):
                    raise RuntimeError("Atom IDs changed between frames!")

            frames.append(vels[order])

    return np.array(frames)  # shape (T, N, 3)


# ------------------------------------------------------------
# Load and downsample
# ------------------------------------------------------------

vel = read_lammps_velocities(dump_file)
print("Loaded velocities:", vel.shape)

# Downsample to avoid O(T^2) explosion, programs surprsingly dont want to calculate T^12 , will take roughly the dawn of time to cacluate 
#I mean, if you have a supercomputer, maybe you can do it, but for the rest of us, we need to be a bit more practical. 
# 1 trillion seconds is about 31,688 years, so unless you have a time machine, it's best to downsample the data.
# Keep first 200k frames, take every 10th → ~20k frames
start = (len(vel) - 200000) // 2
end = start + 200000
vel = vel[start:end:10]


# ------------------------------------------------------------
# 2. Compute VACF
# ------------------------------------------------------------

T, N, _ = vel.shape
vel_flat = vel.reshape(T, -1)

# Remove drift
vel_flat -= vel_flat.mean(axis=0, keepdims=True)

def compute_vacf(v):
    T, D = v.shape
    vacf = np.zeros(T)

    for t0 in range(T):
        v0 = v[t0]
        max_tau = T - t0
        corr = np.einsum("ij,ij->i", v[t0:t0+max_tau], v0[None, :]) / D
        vacf[:max_tau] += corr

    vacf /= np.arange(T, 0, -1)
    vacf /= vacf[0]  # normalize
    return vacf

vacf = compute_vacf(vel_flat)
np.savetxt("vacf.dat", np.column_stack((np.arange(len(vacf)), vacf)))
print("VACF written to vacf.dat")

# ------------------------------------------------------------
# 3. Quick plot
# ------------------------------------------------------------

# dt_fs = 0.25  # your MD timestep in femtoseconds
# downsample = 10  # you kept every 10th frame
# lag = np.arange(len(vacf))
# time_fs = lag * dt_fs * downsample
# time_log = np.log10(time_fs[1:])
# vacf_log = vacf[1:]

# plt.plot(time_log, vacf_log)
# plt.xlabel("log$_{10}$(time [fs])")
# plt.ylabel("VACF (normalized)")
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("vacf_log_time.png", dpi=300)
# plt.show()

# Convert lag index → time in fs
dt_fs = 0.25
downsample = 10
lag = np.arange(len(vacf))
time_fs = lag * dt_fs * downsample

# Truncate noisy tail (example: first 5 ps)
cutoff_fs = 4000  # 4 ps
cutoff_idx = np.searchsorted(time_fs, cutoff_fs)

vacf_trunc = vacf[:cutoff_idx]
time_fs_trunc = time_fs[:cutoff_idx]

# Avoid log10(0)
time_log = np.log10(time_fs_trunc[1:])
vacf_log = vacf_trunc[1:]

plt.plot(time_log, vacf_log)
plt.xlabel("log$_{10}$(time [fs])")
plt.ylabel("VACF (normalized)")
plt.grid(True)
plt.tight_layout()
plt.savefig("vacf_log_truncated.png", dpi=300)
plt.show()

#print("Ta-da!")