#!/bin/bash
##Calculate the RMSE for the test set for each seed, and then calculate the average RMSE across all seeds. 
#This is done by finding the lowest test RMSE for each seed, and then averaging those values across all seeds.
#The test RMSE is converted from eV to meV, and the test force RMSE is converted from eV/A to meV/A.
###This code assumes you have 8 seeds, and that the learning curve files are located in cnn-1/learning-curve.out, cnn-2/learning-curve.out, etc.
echo 'E Test pa / meV | F Test / meV/A'

#awk 'NF==25{print $1,"|", $2*27211.4, "|", $3*27211.4,"|", $4*27211.4 ,"|", $5*27211.4 , "|", $10*51422.1 ,"|", $11*51422.1}' learning-curve.out

for j in {1..8};
do  
	i=$(awk 'NF==13 && $1>=10{print $1, $11}' cnn-$j/learning-curve.out | sort -k2n | head -1 | awk '{print $1}')
	awk -v i=$i 'NF==13 && $1==i{print $1, $3, $11}' cnn-$j/learning-curve.out

done | awk '{tes+=$2**2 ; tfs+=$3**2}END {print sqrt(tes/8)*1000, sqrt(tfs/8)*1000}'

