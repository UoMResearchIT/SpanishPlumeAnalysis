#!/bin/bash
set -o errexit

usage()
{
    echo ""
    echo "Usage: ./singularity_rip.sh -od=outputdir -wd=wrfdata [-ti=trajinputs] [options]"
    echo ""
    echo "The output directory and the path to the wrf data are the only necessary inputs. They can be specified in the order indicated above or with the options -od and -wd."
    echo "If the inputs file is not specified, and the trajectgory times (-tt) are not set, the basename of the output directory will be used, and the .inputs file is assumed to exist in the cwd."
    echo ""
    echo "  Options:"
    echo "    -h    --help          Print usage info"
    echo "    -od=* --outputdir=*   Path to output directory"
    echo "    -wd=* --wrfdata=*     Path to wrfout data"
    echo "    -tp=* --trajplot=*    Option to specify a name for the trajectory plot. The default is traj_plot"
    echo "    -ti=* --trajinputs=*  Path to trajectory inputs file"
    echo "    -tt=* --trajtimes=*   Trajectory times specified as a range separated by a dash, e.g. '-tt=0-12'"
    echo "                            *Note that this option will generate a .inputs file from the template, overriding the file specified with -ti."
    echo "                            You may also want to change the default values of traj_dt, file_dt, traj_x, traj_y and hydrometeor."
    echo ""
    echo "    -nr   --noRDP         Skips the ripdp pre-processing of wrfout files. Pre-processed data is expected to be in RIPDP/."
    echo "    -nt   --noTraj        Skips trajectory computation. If a plot will be generated, *.traj files are expected to be in BTrajectory/."
    echo "    -np   --noPlot        Skips plot generation."
    echo "    -i    --interactive   Launches the singularity container on interactive mode at the end of the script."
    echo ""
    echo "      RIPDP:"
    echo "          --t_0=*         Simulation time in which ripdp should start pre-processing data, measured in simulation steps. The default value is 0."
    echo "          --t_f=*         Simulation time in which ripdp should stop pre-processing data, measured in simulation steps.The default value is 168."
    echo "          --dt=*          Simulation step time interval, measured in hours. The default value is 1."
    echo ""
    echo "      Trajectory inputs template:"
    echo "          --traj_dt=*     Timestep for trajectory numerical computation, measured in seconds. The default value is 600."
    echo "          --file_dt=*     Time interval in ripdp preprocessed data files, measured in seconds. The default value is 3600."
    echo "          --traj_x=*      Grid horizontal (east-west) position for tracking particle release. The default value is 195."
    echo "          --traj_y=*      Grid vertical (north-south) position for tracking particle release. The default value is 410."
    echo "          --hydrometeor   The default value is 0."
    echo ""
    echo ""
    echo "Examples:"
    echo "  ./singularity_rip.sh Control /mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
    echo "      The above will create the folder ./Control, pre-process the data from run-zrek with ripdp, compute the backtrajectories from the ./Control.inputs file, generate a plot and save it as traj_plot.pdf"
    echo ""
    echo "  ./singularity_rip.sh -od=Results/Control -wd=/mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/ --noRDP -tt=68-35 -tp=Traj_68"
    echo "      The above look in ./Results/Control/RIPDP for the ripdp pre-processed data, use the template to compute trajectories from simulation time 68 to 35 (backtrajectories), generate a plot and save it as Traj_68.pdf"
    echo ""
    echo "  ./singularity_rip.sh -od=Results/Sample -wd=/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/Sample/WRFData/ -tt=12-0 --traj_dt=600 --file_dt=10800 --traj_x=55 --traj_y=40"
    echo "      The above configures the trajectory inputs template to be able to use it with the sample data."
    echo ""
}

# Defaults
    #ripdp
t_0=0
t_f=168
dt=1
    #plot format
ncarg_type="pdf"
    #traj inputs
traj_dt=600
file_dt=3600
traj_x=195
traj_y=410
hydrometeor=0
    #templates
rdp_tpl="Templates/rdp.template"
run_tpl="Templates/run.template"
tinp_tpl="Templates/traj_inputs.template"
tplot_tpl="Templates/traj_plot.template"
traj_tpl="Templates/traj.template"
POSITIONAL_ARGS=()
posod=1
poswd=1
cwdti=1
trajtimes=""
trajplot="traj_plot"
noRDP=0
noTraj=0
noPlot=0
interactive=0

# Argument parsing
for i in "$@"; do       #cycles through arguments
    case $i in              # Checks each argument to see if it is a positional argument or an option
        -h|--help*)             # If help flag is raised, program wont run.
            usage                   # Prints usage info
            exit                    # Exits without raising a warning
            ;;
        -od=*|--outputdir=*)    # If known option
            folder="${i#*=}"        # Saves value
            posod=0
            ;;
        -wd=*|--wrfdata=*)
            data="${i#*=}"
            poswd=0
            ;;
        -tp=*|--trajplot=*)
            trajplot="${i#*=}"
            ;;
        -ti=*|--trajinputs=*)
            inputsfile="${i#*=}"
            cwdti=0
            ;;
        -tt=*|--trajtimes=*)
            trajtimes="${i#*=}"
            cwdti=0
            ;;
        -nr|--noRDP)
            noRDP=1
            ;;
        -nt|--noTraj)
            noTraj=1
            ;;
        -np|--noPlot)
            noPlot=1
            ;;
        -i|--interactive)
            interactive=1
            ;;
        --t_0=*)
            t_0="${i#*=}"
            ;;
        --t_f=*)
            t_f="${i#*=}"
            ;;
        --dt=*)
            dt="${i#*=}"
            ;;
        --traj_dt=*)
            traj_dt="${i#*=}"
            ;;
        --file_dt=*)
            file_dt="${i#*=}"
            ;;
        --traj_x=*)
            traj_x="${i#*=}"
            ;;
        --traj_y=*)
            traj_y="${i#*=}"
            ;;
        --hydrometeor)
            hydrometeor=1
            ;;
        -*|--*)                 # If option not listed above (invalid)
            echo "ERROR: Unknown option $i."
            usage                   # Prints usage info
            exit 1                  # Exits with warning
            ;;
        *)                      # If not an option
            POSITIONAL_ARGS+=("$i") # Save as positional argument
            ;;
    esac
done
    # Positional arguments
set -- "${POSITIONAL_ARGS[@]}"  # restore positional parameters
if [ $posod -eq 1 ]; then
    folder=$1                   # Saves input 1 (folder to clean)
    echo "outputdir=$folder"
fi
if [ $poswd -eq 1 ]; then
    data=$2                     # Saves input 2 (path to wrfout files)
    echo "wrfdata=$data"
fi
    # Argument processing
name=$(basename ${folder})      # Strips directory from folder

#####

# Checks data path exists
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

# Pre-processes data with rdp
if [ $noRDP -eq 0 ]; then
    # Copies rdp template
    export t_0 t_f dt
    envsubst '$t_0 $t_f $dt' < $rdp_tpl >$folder/RIPDP/rdp_$name

    # Copies run template
    rip_program="ripdp_wrfarw"
    rip_program_args="all WRFData/wrfout_d01_*"
    export rip_program rip_program_args name
    envsubst '$rip_program $rip_program_args $name' < $run_tpl > $folder/run_rdp.sh

    # Runs ripdp inside singularity container
    singularity \
        exec \
            --contain \
            --cleanenv \
            --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/$folder/:/$name/ \
            --bind $data/:/$name/WRFData/ \
            --pwd /$name \
            ripdocker_latest.sif  \
            /bin/bash run_rdp.sh
else
    echo "Skipping ripdp pre-processing..."
fi

#Prepares inputs file
if [ $((noTraj+noPlot)) -lt 2 ]; then
    if [ $cwdti -eq 1 ]; then
        inputsfile=$name.inputs     # Looks for inputs file in cwd
    fi
    if [ $trajtimes = "" ]; then    # Inputs file was either specified or should be in cwd.
        if [ ! -f "$inputsfile" ]; then
            echo "ERROR: Cannot find $inputsfile."
            exit 1
        fi
        cp $inputsfile $folder/BTrajectories/traj_inputs    
    else                            # Inputs file will be generated from template
        traj_t_0=${trajtimes%-*}        # Read first number (everything before -)
        traj_t_f=${trajtimes#*-}        # Read second number (everything after -)
        export traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y hydrometeor
        envsubst '$traj_t_0 $traj_t_f $traj_dt $file_dt $traj_x $traj_y $hydrometeor' < $tinp_tpl > $folder/BTrajectories/traj_inputs
    fi
    inputsfile=$folder/BTrajectories/traj_inputs
    sed -i '/^#/d'  $inputsfile             # Deletes header/comment lines
    sed -i '/^[[:space:]]*$/d' $inputsfile  # Deletes empty lines
    sed -i 's/ *$//; s/[[:space:]]\+/|/g; s/$/|/' $inputsfile   # Replaces spaces with |
    sed -i '$a\' $inputsfile                # Makes sure there's an empty line at the end
    wait
    npoints=$(wc -l < $inputsfile)          # Counts number of input lines
fi

# Calculates trajectories
if [ $noTraj -eq 0 ]; then
    # Generates trajectory input files and trajectory plot file
    traji=0
    while IFS='|' read -r traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_z hydrometeor color; do    #Reads inputs file line by line
        traji=$((traji+1))
        # Copies traj template
        export traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_z hydrometeor
        envsubst '$traj_t_0 $traj_t_f $traj_dt $file_dt $traj_x $traj_y $traj_z $hydrometeor' < $traj_tpl > $folder/BTrajectories/traj$traji.in
    done <"$inputsfile"
    # Checks that all lines were read
    if [ $traji -ne $npoints ]; then
        echo "ERROR: Something weird happened reading the inputsfile. Check structure is correct, and compare with $inputsfile."
        exit 1
    fi

    # Computes trajectories
    traji=0
    while IFS='|' read -r traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_z hydrometeor color; do    #Reads inputs file line by line
        traji=$((traji+1))
        echo "Processing Trajectory $traji: t_0=$traj_t_0 t_f=$traj_t_f x:$traj_x y:$traj_y z:$traj_z color=$color"
        
        # Copies run template
        rip_program="rip -f"
        rip_program_args="BTrajectories/traj$traji.in"
        export rip_program rip_program_args name
        envsubst '$rip_program $rip_program_args $name' < $run_tpl > $folder/run_traj_i.sh

        # Runs rip inside singularity container
        singularity \
            exec \
                --contain \
                --cleanenv \
                --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/$folder/:/$name/ \
                --bind $data/:/$name/WRFData/ \
                --pwd /$name \
                ripdocker_latest.sif  \
                /bin/bash run_traj_i.sh
    done <"$inputsfile"
else
    echo "Skipping trajectory computation..."
fi

# Generates plot
if [ $noPlot -eq 0 ]; then
    Trajectory_Spec_List=""
    traji=0
    while IFS='|' read -r traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_z hydrometeor color; do    #Reads inputs file line by line
        traji=$((traji+1))
        Trajectory_Spec_List=$Trajectory_Spec_List"feld=arrow; ptyp=ht; tjfl=BTrajectories/traj$traji.traj; vcor=s;>"$'\n'
        Trajectory_Spec_List=$Trajectory_Spec_List"    colr=$color; nmsg; tjst=$traj_t_f; tjen=$traj_t_0"$'\n'
        # Copies traj_plot template
        export ncarg_type Trajectory_Spec_List
        envsubst '$ncarg_type $Trajectory_Spec_List' < $tplot_tpl > $folder/traj_plot.in
    done <"$inputsfile"
    sed -i '/^[[:space:]]*$/d' $folder/traj_plot.in  # Deletes empty lines
    # Copies run template
    rip_program="rip -f"
    rip_program_args="traj_plot.in"
    export rip_program rip_program_args name
    envsubst '$rip_program $rip_program_args $name' < $run_tpl > $folder/run_tplot.sh

    # Runs rip inside singularity container
    singularity \
        exec \
            --contain \
            --cleanenv \
            --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/$folder/:/$name/ \
            --bind $data/:/$name/WRFData/ \
            --pwd /$name \
            ripdocker_latest.sif  \
            /bin/bash run_tplot.sh
else
    echo "Skipping plot generation..."
fi

# Enter interactive mode in singularity container
if [ $interactive -eq 1 ]; then
    singularity \
        shell \
            --contain \
            --cleanenv \
            --bind /mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/Singularity/$folder/:/$name/ \
            --bind $data/:/$name/WRFData/ \
            --pwd /$name \
            ripdocker_latest.sif
fi