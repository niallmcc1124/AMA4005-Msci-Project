#!/bin/bash
##ASSUMES you have the gpumdkit.sh installed
##frames.txt contains the frame numbers you want to include in the training set (one per line)
##See SE.py for how to select these frames based on the SE, and also to see how the SE changes as you add more frames into the training set.

# # 1. Clone the repository
 git clone https://github.com/zhyan0603/GPUMDkit.git

# # 2. Add to your ~/.bashrc
 export GPUMDkit_path=/path/to/GPUMDkit
 export PATH=${GPUMDkit_path}:${PATH}
 source ${GPUMDkit_path}/Scripts/utils/completion.sh

# # 3. Reload your shell
 source ~/.bashrc

# # 4. Make executable
 cd ${GPUMDkit_path}
 chmod +x gpumdkit.sh

# # Read allowed frame numbers into an array
# mapfile -t frames < Frames.txt

# # Loop over all POSCAR_* files
# for poscar in POSCAR_*; do
#     #Extract the frame number from the filename
    
#     echo "Processing $poscar"
#     num="${poscar#POSCAR_}"
#     num="${num%.vasp}"

#     # Check if this frame number is in frames.txt
#     if printf '%s\n' "${frames[@]}" | grep -qx "$num"; then
#         echo "Processing allowed frame: $num"

#         dirname="include_frames/Frame_${num}"
#         mkdir -p "$dirname"
#         mv "$poscar" "$dirname/POSCAR"
#         echo "Ta-da"
#     else
#         echo "removing frame $num (when its gone its gone)"
#       rm $poscar
#     fi
# done

# for frames in include_frames/Frame_*; do
#     echo "Submitting VASP: $frames"
#     cp  include_frames/INCAR include_frames/KPOINTS include_frames/POTCAR include_frames/Single_Point_AIMD.job $frames
#     cd $frames
#     sbatch Single_Point_AIMD.job
#     cd ../../
# done

# for dir in include_frames/Frame_*; do
#     cd $dir
#     #change to .xyz
#     echo "convert to .xyz $dir"
#     python3 -c $'from ase.io import read,write;write("tobermorite_9A.xyz",read("OUTCAR"))'
#     egrep "free_energy=" tobermorite_9A.xyz
#     cd ../../
# done