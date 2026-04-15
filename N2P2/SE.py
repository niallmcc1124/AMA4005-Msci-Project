##Basically provides a table for the SE for each timestep calcalted throught teh LAMMPS simulation
##The .csv file produced is incredibly handy to then further add frames into the training set, and see how the SE changes as you add more frames.
##and allows you to selecte that frames that will actually imrove the model 
##from adding to understadn new configurations spaces 


import numpy as np
 
# ---------------------------
# READ EXTXYZ REFERENCE FILE
# ---------------------------
def read_reference_extxyz(filename):
    with open(filename) as f:
        lines = f.readlines()
 
    n_atoms = int(lines[0])    # first line is atom count
    start = 2                  # skip comment line
 
    forces = []
    for i in range(start, start + n_atoms):
        parts = lines[i].split()
        # forces are last 3 columns in EXTXYZ
        fx, fy, fz = map(float, parts[-3:])
        forces.append([fx, fy, fz])
 
    return np.array(forces)
 
 
# ---------------------------
# READ LAMMPS dump.force FILE
# ---------------------------
def read_lammps_dump(filename):
    timesteps = []
    with open(filename) as f:
        lines = f.readlines()
 
    i = 0
    while i < len(lines):
        if lines[i].startswith("ITEM: TIMESTEP"):
            step_number = int(lines[i+1])
            n_atoms = int(lines[i+3])
            i += 9  # move to first atom line
 
            forces = []
            for _ in range(n_atoms):
                parts = lines[i].split()
                fx, fy, fz = map(float, parts[1:4])
                forces.append([fx, fy, fz])
                i += 1
 
            timesteps.append((step_number, np.array(forces)))
        else:
            i += 1
 
    return timesteps
 
 
# ---------------------------
# MAIN RMSE CALCULATION
# ---------------------------
ref = read_reference_extxyz("reference.xyz")
timesteps = read_lammps_dump("dump.force")
 

import csv

with open("rmse_results5.0.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["timestep", "rmse"])

    for step, forces in timesteps:
        rmse = np.sqrt(np.mean((forces - ref)**2))
        writer.writerow([step, rmse])

