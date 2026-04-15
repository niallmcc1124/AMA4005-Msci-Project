#!/usr/bin/awk -f
# ============================================================
# Extract trajectory in extended XYZ format from VASP OUTCAR
# Get eleemnts and number of elements from POSCAR 
# WHEN using this awk -f AWK_Trajectories.awk POSCAR OUTCAR need both remember that 
# ============================================================

{
    
    # Start of a new 64-line block
    if ((NR - 1) % 64 == 0) {
	print"Beginning"
	print "begin" > "input.data"
    print "comment " "this contains 10 Ca 12 Si 36 O and 4 H" >> "input.data"
    print NR
	getline; 
    # moves me to the next line, which contains the lattice and the energy 
	#on this line NF 1-9 is lattice, 11 is energy 
	gsub(/Lattice="/, ""); # removes the fact that $1 is Lattice=Number so it reads as just number
	gsub(/"/, ""); # removes the " on the 9th input file
	print "lattice " $1,$2,$3 >> "input.data"
	print "lattice " $4,$5,$6 >> "input.data"
	print "lattice " $7,$8,$9 >> "input.data"
    print "lattice is done"
	gsub(/energy=/, ""); #removes the energy= from $11 so just the number
	Temp_energy = $11
	# Next lines are about the atoms, so the line should look like atom,x,y,z, element,0,0,fx,fy,fz
	getline; # now onto the atomic lines
	while(NF==7)
	{
	  print "atom ", $2,$3,$4,$1,0.0,0.0,$5,$6,$7 >> "input.data"
      getline;
	}
    print "atoms are done"
    print "energy " Temp_energy >> "input.data"
	print "end" >> "input.data"
    }
}
#TA-DA
