#!/bin/bash

# Checks that there are enough inputs
if [ $# -lt 2 ]; then
    echo "ERROR: Not enough arguments provided. I need at least the folder name to work on, and the data directory."
    echo "Usage: ./singularity_rip.sh [Directory] [/path/to/WRF/data] [noRDP]"
    echo "For example: "
    echo "./singularity_rip.sh Control /mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
    echo "will create the folder ./Control, pre-process the data from run-zrek with rip-dp, and generate the backtrajectories from the Control.inputs file."
    echo "If you want to skip the pre-processing with rip-dp, make sure your folder already contains the preprocessed data, and trail the command with noRDP, e.g.:"
    echo "./singularity_rip.sh Control /mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/ noRDP"
    echo ""
    exit 1
fi

# Gets inputs
folder=$1				# Saves input 1 (folder to clean)
data=$2                 # Saves input 2 (path to wrfout files)
rdp=$3                  # Saves input 3 (option to skip rip-dp preprocessing)
inputsfile="${4:-$folder.inputs}"   # Saves input 4, file with trajectory inputs

rdp_tpl="Templates/rdp.template"
run_tpl="Templates/run.template"
tplot_tpl="Templates/traj_plot.template"
traj_tpl="Templates/traj.template"


# Checks data folder exists
if [ ! -d "$data" ]; then
    echo "ERROR: Cannot find $data."
    exit 1
else
    if [[ $data = */ ]]; then
        # Deletes trailing /
            data=${data::-1}
    fi    
fi
if [[ $folder = */ ]]; then
    # Deletes trailing /
        folder=${folder::-1}
fi
# Creates directory structure if it does not exist
mkdir -p $folder/RIPDP
mkdir -p $folder/BTrajectories
mkdir -p $folder/WRFData

t_0=0
t_f=169
dt=1
ncarg_type="pdf"

# Pre-processes data with rdp
if [ "$rdp" != "noRDP" ]; then
    # Copies rdp template
    export t_0 t_f dt
    envsubst '$t_0 $t_f $dt' < $rdp_tpl >$folder/RIPDP/rdp_$folder

    # Copies run template
    rip_program="ripdp_wrfarw"
    rip_program_args="all WRFData/wrfout_d01_*"
    export rip_program rip_program_args folder
    envsubst '$rip_program $rip_program_args $folder' < $run_tpl > $folder/run_rdp.sh

    # Runs ripdp inside singularity container
    singularity \
        exec \
            --contain \
            --cleanenv \
            --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/$folder/:/$folder/ \
            --bind $data/:/$folder/WRFData/ \
            --pwd /$folder \
            ripdocker_latest.sif  \
            /bin/bash run_rdp.sh
else
    echo "Skipping ripdp pre-processing..."
fi

#Prepares inputs file
if [ ! -f "$inputsfile" ]; then
    echo "ERROR: Cannot find $inputsfile."
    exit 1
fi
cp $inputsfile $folder/BTrajectories/traj_inputs
inputsfile=$folder/BTrajectories/traj_inputs
sed -i '/^#/d'  $inputsfile             # Deletes header/comment lines
sed -i '/^[[:space:]]*$/d' $inputsfile  # Deletes empty lines
sed -i 's/ *$//; s/[[:space:]]\+/|/g; s/$/|/' $inputsfile   # Replaces spaces with |
sed -i '$a\' $inputsfile                # Makes sure there's an empty line at the end
wait
npoints=$(wc -l < $inputsfile)          # Counts number of input lines

traji=0
# Generates trajectory input files
while IFS='|' read -r traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_z hydrometeor color eol; do    #Reads inputs file line by line
    traji=$((traji+1))
    echo "Traj$traji: col=$color, z: $traj_z"
    # Copies traj template
    export ncarg_type traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_z hydrometeor color
    envsubst '$ncarg_type $traj_t_0 $traj_t_f $traj_dt $file_dt $traj_x $traj_y $traj_z $hydrometeor $color' < $traj_tpl > $folder/BTrajectories/traj$traji.in
done <"$inputsfile"
# Checks that all lines were read
if [ $traji -ne $npoints ]; then
    echo "ERROR: Something weird happened reading the inputsfile. Check structure is correct, and compare with $inputsfile."
    exit 1
fi

# Computes trajectories
for (( traji=1; traji<=$npoints; traji++ )); do
    # Copies run template
    rip_program="rip -f"
    rip_program_args="BTrajectories/traj$traji.in"
    export rip_program rip_program_args folder
    envsubst '$rip_program $rip_program_args $folder' < $run_tpl > $folder/run_traj_i.sh

    # Runs rip inside singularity container
    singularity \
        exec \
            --contain \
            --cleanenv \
            --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/$folder/:/$folder/ \
            --bind $data/:/$folder/WRFData/ \
            --pwd /$folder \
            ripdocker_latest.sif  \
            /bin/bash run_traj_i.sh
done
# Generates plot


# singularity \
#     shell \
#         --contain \
#         --cleanenv \
#         --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/Test/:/Test/ \
#         --bind /mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/:/Test/WRFData/ \
#         --pwd /Test \
#         ripdocker_latest.sif