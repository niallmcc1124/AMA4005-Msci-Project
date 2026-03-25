#!/bin/bash
#SBATCH --job-name=Tober9A_OSZICAR_AIMD
#SBATCH --output=output_%x_%j
#SBATCH --ntasks=256
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=500M
#SBATCH --time=02:59:00 
#SBATCH --partition=k2-hipri
#SBATCH --mail-user=nmccallion05@qub.ac.uk
#SBATCH --mail-type=BEGIN,END,FAIL

# Avoid any unintentional OpenMP threading by setting OMP_NUM_THREADS
export OMP_NUM_THREADS=1

module purge

module load vasp/6.5.1/gcc-14.1.0+openmpi-5.0.3+openblas-0.3.27+scalapack-2.2.0+fftw3-3.3.10+wannier90_serial-3.1.0+hdf5_serial-1.14.4

# module list

# starting
date=`date`
echo "# Doing script: started on ${date}..."

echo "# JOBNAME   = ${SLURM_JOB_NAME}"
echo "# JOBID     = ${SLURM_JOB_ID}"
echo "# PARTITION = ${SLURM_JOB_PARTITION}"
echo "# NODELIST  = ${SLURM_JOB_NODELIST}"
echo "# CPUS      = ${SLURM_TASKS_PER_NODE}"

#MPIJOB="mpirun -np ${SLURM_NTASKS}"
MPIJOB="mpirun"
echo "# MPIJOB    = ${MPIJOB}"

VASP_STD="${MPIJOB} vasp_std"
echo "# VASP_STD  = ${VASP_STD}"

VASP_GAM="${MPIJOB} vasp_gam"
echo "# VASP_GAM  = ${VASP_GAM}"

# copy this script
cp ${0} job_pid${SLURM_JOB_ID}.sh

##################
# MD calculation #
##################

date=`date`
echo "# Doing MD calculation: started on ${date}..."

# label_root
label_md="Tober9A_pid${SLURM_JOB_ID}"

# execute
#${VASP_STD} >& out.${label_md}
${VASP_GAM} >& out.${label_md} # for AIMD

date=`date`
echo "# Doing MD calculation: ... ended on ${date}"

