####################################
#Take your values from input.data(trained NN) and - a Repulsion in my case that is a LJ
#to run use the following line
#awk -f BuildDelta.awk lj_forces.dump lj_energy.out input.data > input_delta.data
#Ta-da
###############################################
# PASS 1: Read LJ forces from lj_forces.dump
###############################################
FNR==NR {
    if ($1=="ITEM:" && $2=="TIMESTEP") {
        getline
        f++
    }

    if ($1=="ITEM:" && $2=="ATOMS") {
        for (i=1; i<=62; i++) {
            getline
            id=$1
            Frep[f,id,"x"]=$6
            Frep[f,id,"y"]=$7
            Frep[f,id,"z"]=$8
        }
    }
    next
}

###############################################
# PASS 1b: Read LJ energies from lj_energy.out
###############################################
ARGIND==2 {
    # Skip comment/header lines
    if ($1 ~ /^#/) next

    e++
    LJenergy[e] = $1
    next
}

###############################################
# PASS 2: Read DFT frames from input.data
###############################################

$1=="begin" {
    frame++
    print "begin"
    print "comment this contains 10 Ca 12 Si 36 O and 4 H"
    id=0
    next
}

$1=="lattice" {
    print $0
    next
}

$1=="atom" {
    id++

    x=$2; y=$3; z=$4
    elem=$5
    q1=$6; q2=$7
    Fx_dft=$8; Fy_dft=$9; Fz_dft=$10

    Fx = Fx_dft - Frep[frame,id,"x"]
    Fy = Fy_dft - Frep[frame,id,"y"]
    Fz = Fz_dft - Frep[frame,id,"z"]

    printf("atom  %.8f %.8f %.8f %s %d %d %.8f %.8f %.8f\n",
           x, y, z, elem, q1, q2, Fx, Fy, Fz)
    next
}

$1=="energy" {
    DFTenergy = $2
    next
}

$1=="end" {
    E = DFTenergy - LJenergy[frame]
    printf("energy %.12f\n", E)
    print "end"
    id=0
    next
}
#Ta-da