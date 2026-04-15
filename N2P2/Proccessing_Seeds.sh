##use this to do the same stuff inside each seed within this directory
##e.g to submit the jobs in each T9A_s folder, use this script in one directory above
##Assumes you have the strucure Seed_1/T9A_P/R/S/T, Seed_2/T9A_P/R/S/T, etc. and that you want to do the same thing in each T9A_ folder, for example.
#!/bin/bash
##currently set to submit the jobs in each T9A_s folder (scaling)
#but can be changed for pruning and training 
# and also for moving files, etc.
j=$((j+1))
for seed in Seed_*; do
    if [[ -d "$seed/T9A_S" ]]; then
    ##Scaling
        # echo "Submitting in: $seed/T9A_S"
        # cp input.data "$seed/T9A_S"
        # cp input.nn "$seed/T9A_S"
        # cp scaling.job "$seed/T9A_S"
        # (cd "$seed/T9A_S" && sbatch scaling.job)
    ##Pruning
        # echo "Submitting in: $seed/T9A_P"
        # cd "$seed/T9A_S" && cp input.data input.nn scaling.data ../T9A_P && cd ../../
        # cp prune.job "$seed/T9A_P"
        # (cd "$seed/T9A_P" && sbatch prune.job)
    ##Rescaling
        # echo "Submitting in: $seed/T9A_R"    
        # cd "$seed/T9A_P"
        # cp input.data ../T9A_R
        # cp output-prune-range.nn ../T9A_R/input.nn
        # cd ../../
        # cp scaling.job "$seed/T9A_R"
        # (cd "$seed/T9A_R" && sbatch scaling.job)
    ##Training  
        # echo "Submitting in: $seed/T9A_T"
        # cd "$seed/T9A_R" && cp input.data input.nn scaling.data ../T9A_T && cd ../../
        # cp train.job "$seed/T9A_T"
        # (cd "$seed/T9A_T" && sbatch train.job)

    ##Creating Committee Models
    ###Note only works if all models run to full completion and have 10 epochs of training, otherwise you will need to change the code to copy the correct files.
        echo "Copying  files in: $seed/T9A_T to ../../../Delta_Model/cnn-$j"
        cd "$seed/T9A_T" && cp learning-curve.out ../../../Delta_Model/cnn-$j
        cp input.nn scaling.data ../../../Delta_Model/cnn-$j 
        cp weights.001.000010.out ../../../Delta_Model/cnn-$j/weights.001.data
        cp weights.008.000010.out ../../../Delta_Model/cnn-$j/weights.008.data
        cp weights.014.000010.out ../../../Delta_Model/cnn-$j/weights.014.data
        cp weights.020.000010.out ../../../Delta_Model/cnn-$j/weights.020.data
        cd ../../   
        j=$((j+1))
        echo $j
        #echo "Ta da"
    fi
done
