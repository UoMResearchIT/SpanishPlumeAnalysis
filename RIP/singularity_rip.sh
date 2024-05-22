#!/bin/bash
#set -o nounset
set -o errexit
set -o pipefail

usage()
{
    echo ""
    echo "  Usage: ./singularity_rip.sh -od=outputdir -wd=wrfdata [-ti=trajinputs] [options]"
    echo ""
    echo "  The output directory is the only necessary input. It can be specified with the option -od, or directly as the first positional parameter."
    echo "  If data will be pre-processed with ripdp, then the path to WRF data is also necessary. It can be specified with the option -wd, or as the second positional parameter."
    echo "  If the inputs file is not specified, and the trajectgory times (-tt) are not set, the basename of the output directory will be used, and the .inputs file is assumed to exist in the cwd."
    echo ""
    echo "  Options:"
    echo "    -h    --help          Print usage info."
    echo "    -od=* --outputdir=*   Path to output directory. The basename of outputdir will be used as prefix in ripdp generated files."
    echo "    -wd=* --wrfdata=*     Path to wrfout data."
    echo "    -tp=* --trajplot=*    Option to specify a name for the trajectory plot. The default is tp_x, where x is the trajectory time range set in -tt."
    echo "    -ti=* --trajinputs=*  Path to trajectory inputs file."
    echo "    -tt=* --trajtimes=*   Trajectory times specified as a range separated by a dash (e.g. '-tt=120-80'), or a single number (the tracking particle release time)."
    echo "                            If a single number is specified, a default backwards interval of 30 hours will be used, that is, '-tt=120' is equivalent to '-tt=120-90'"
    echo "                            *Note that this option will generate a .inputs file from the template, overriding the file specified with -ti."
    echo "                            You may also want to change the default values of traj_dt, file_dt, traj_x, traj_y and hydrometeor."
    echo "    -td=* --trajdiag=*    Option to specify a group of diagnostics to be added to the csv file, which can be g1, g2, none, or all."
    echo "    -pd=* --ripdpdata=*   Path to ripdp input file used to preprocess the data ( which should be the prefix of the ripdp data files)."
    echo "                            This option need only be used when the preprocessed data is not in the default directory or name outputdir/RIPDP/rdp_name."
    echo "                            *Note that this option automatically enables --noRDP, as pre-processing should not be needed."
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
    echo "          --traj_dt=*     Timestep for trajectory numerical computation, measured in seconds. It should be smaller than file_dt. The default value is 600."
    echo "          --file_dt=*     Time interval in ripdp preprocessed data files, measured in seconds. The default value is 3600."
    echo "          --traj_x=*      Grid horizontal (east-west) position for tracking particle release. The default value is 195."
    echo "          --traj_y=*      Grid vertical (north-south) position for tracking particle release. The default value is 410."
    echo "          --hydrometeor   The default value is 0."
    echo ""
    echo ""
    echo "  Examples:"
    echo "    ./singularity_rip.sh Control /mnt/seaes01-data01/dmg/dmg/mbessdl2/Spanish_Plume/WRF/run-zrek/"
    echo "       The above will create the folder ./Control, pre-process the data from run-zrek with ripdp, compute the backtrajectories from the ./Control.inputs file, generate a plot and save it as tp.pdf"
    echo ""
    echo "    ./singularity_rip.sh -od=Results/Control --noRDP -tt=68-35 -tp=Traj_68"
    echo "       The above will look in ./Results/Control/RIPDP for the ripdp pre-processed data, use the template to compute trajectories from simulation time 68 to 35 (backtrajectories), generate a plot and save it as Traj_68.pdf"
    echo ""
    echo "    ./singularity_rip.sh -od=Results/Sample -wd=/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/RIP/Sample/WRFData/ -tt=12-0 --traj_dt=600 --file_dt=10800 --traj_x=55 --traj_y=40"
    echo "       The above configures the trajectory inputs template to be able to use it with the sample data."
    echo ""
}

## Defaults
    # RIPDP
        t_0=0
        t_f=168
        dt=1
    # Plot format
        ncarg_type="pdf"
    # Traj inputs
        traj_dt=600
        file_dt=3600
        traj_x=195
        traj_y=410
        hydrometeor=0
        diagnostics=""
    # Templates
        rip_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/"
        rdp_tpl="$rip_dir""Templates/rdp.template"
        run_tpl="$rip_dir""Templates/run.template"
        tinp_tpl="$rip_dir""Templates/traj_inputs.template"
        tplot_tpl="$rip_dir""Templates/traj_plot.template"
        traj_tpl="$rip_dir""Templates/traj.template"
        tabdiag_tpl="$rip_dir""Templates/tabdiag_format.template"
    # Script
        POSITIONAL_ARGS=()
        posod=1
        porip_dir=1
        cwdti=1
        wrfdata=""
        trajtimes=""
        ripdpdata=""
        trajplot=""
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
            wrfdata="${i#*=}"
            porip_dir=0
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
            if [ "$trajplot" = "" ]; then
                trajplot="tp_$trajtimes"
            fi
            cwdti=0
            ;;
        -td=*|--trajdiag=*)
            diagnostics="${i#*=}"
            ;;
        -pd=*|--ripdpdata=*)
            ripdpdata="${i#*=}"
            noRDP=1
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
if [ $# -gt 0 ]; then
    echo "WARNING: Detected positional arguments. Make sure the values were identified correctly:"
    if [ $posod -eq 1 ]; then
        folder=$1                   # Saves input 1 (folder to clean)
        echo "             outputdir=$folder"
        shift
    fi
    if [ $porip_dir -eq 1 ]; then
        wrfdata=$1                  # Saves input 2 (path to wrfout files)
        echo "             wrfdata=$wrfdata"
        shift
    fi
    echo "         Use options to set the values if you don't want this warning to show up."
    if [ $# -gt 0 ]; then
        echo "ERROR: Unexpected positional parameters: $@"
        exit 1
    fi
fi
    # Argument processing
if [[ $folder = */ ]]; then
    # Deletes trailing /
        folder=${folder::-1}
fi
name=$(basename ${folder})      # Strips directory from folder
if [ "$wrfdata" = "" ]; then
    wrfdata="$folder/WRFData"
fi
if [ "$ripdpdata" = "" ]; then
    ripdpdata_dir=$folder/RIPDP
    ripdpdata="rdp_$name"
else
    # Checks ripdp data exists
    if [ ! -f "$ripdpdata" ]; then
        echo "ERROR: Cannot find $ripdpdata."
        echo "   Remember, rdpdata should be the path to the rdp_name *file*, not just the directory where the data is stored."
        exit 1
    else
        ripdpdata_dir=$(dirname -- "$ripdpdata")
        ripdpdata=$(basename -- "$ripdpdata")
    fi
fi
if [ "$trajplot" = "" ]; then
    trajplot="tp_"
fi

#####

# Creates directory structure if it does not exist
mkdir -p $folder/WRFData
mkdir -p $folder/RIPDP
mkdir -p $folder/BTrajectories

# Pre-processes data with rdp
if [ $noRDP -eq 0 ]; then
    # Checks data path exists
    if [ ! -d "$wrfdata" ]; then
        echo "ERROR: Cannot find $wrfdata."
        exit 1
    else
        if [[ $wrfdata = */ ]]; then
            # Deletes trailing /
                wrfdata=${wrfdata::-1}
        fi    
    fi
    # Copies rdp template
    export t_0 t_f dt
    envsubst '$t_0 $t_f $dt' < $rdp_tpl >$folder/RIPDP/$ripdpdata

    # Copies run template
    rip_program="ripdp_wrfarw  -n RIPDP/$ripdpdata"
    rip_program_args="all WRFData/wrfout_d01_*"
    save_to_csv=""
    export rip_program rip_program_args ripdpdata save_to_csv
    envsubst '$rip_program $rip_program_args $ripdpdata $save_to_csv' < $run_tpl > $folder/run_rdp.sh

    # Runs ripdp inside singularity container
    singularity \
        exec \
            --contain \
            --cleanenv \
            --bind $folder/:/$name/ \
            --bind $wrfdata/:/$name/WRFData/ \
            --bind $ripdpdata_dir/:/$name/RIPDP/ \
            --pwd /$name \
            "$rip_dir"ripdocker_latest.sif  \
            /bin/bash run_rdp.sh
else
    echo "Skipping ripdp pre-processing..."
fi

#Prepares inputs file
if [ $((noTraj+noPlot)) -lt 2 ]; then
    if [ $cwdti -eq 1 ]; then
        inputsfile=$name.inputs     # Looks for inputs file in cwd
    fi
    if [ "$trajtimes" = "" ]; then  # Inputs file was either specified or should be in cwd.
        if [ ! -f "$inputsfile" ]; then
            echo "ERROR: Cannot find $inputsfile."
            echo "You need to either specify the path to another inputs file with -ti, or set the trajectory time interval with -tt."
            exit 1
        fi
        cp $inputsfile $folder/BTrajectories/"$trajplot"_traj_inputs    
    else                            # Inputs file will be generated from template
        traj_t_0=${trajtimes%-*}        # Read first number (everything before -)
        traj_t_f=${trajtimes#*-}        # Read second number (everything after -)
        if [ "$traj_t_f" = "$traj_t_0" ] || [ "$traj_t_f" = "" ]; then
            traj_t_f=$((traj_t_0-30))
            if [ $traj_t_f -lt 0 ]; then
                traj_t_f=0
            fi
        fi
        export traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y hydrometeor
        envsubst '$traj_t_0 $traj_t_f $traj_dt $file_dt $traj_x $traj_y $hydrometeor' < $tinp_tpl > $folder/BTrajectories/"$trajplot"_traj_inputs
    fi
    inputsfile=$folder/BTrajectories/"$trajplot"_traj_inputs
    sed -i '/^#/d'  $inputsfile             # Deletes header/comment lines
    sed -i '/^[[:space:]]*$/d' $inputsfile  # Deletes empty lines
    sed -i 's/ *$//; s/[[:space:]]\+/|/g; s/$/|/' $inputsfile   # Replaces spaces with |
    sed -i '$a\' $inputsfile                # Makes sure there's an empty line at the end
    wait
    npoints=$(wc -l < $inputsfile)          # Counts number of input lines
fi

# Calculates trajectories
if [ $noTraj -eq 0 ]; then
    # Updates trajplot template
    python3 "$rip_dir""Templates/generate_traj_template.py" $diagnostics
    # Copies tabdiag template and tabdiag_to_csv script
    if [ "$diagnostics" != "none" ]; then
        cp $tabdiag_tpl $folder/tabdiag_format.in
        cp "$rip_dir""Templates/tabdiag_to_csv.py" $folder/tabdiag_to_csv.py
    fi
    # Generates trajectory input files and trajectory plot file
    traji=0
    while IFS='|' read -r traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_z hydrometeor color; do    #Reads inputs file line by line
        traji=$((traji+1))
        # Copies traj template
        export traj_t_0 traj_t_f traj_dt file_dt traj_x traj_y traj_z hydrometeor
        envsubst '$traj_t_0 $traj_t_f $traj_dt $file_dt $traj_x $traj_y $traj_z $hydrometeor' < $traj_tpl > $folder/BTrajectories/"$trajplot"_traj_$traji.in
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
        rip_program_args="BTrajectories/"$trajplot"_traj_$traji.in"
        rip_diag_file="BTrajectories/"$trajplot"_traj_$traji"
        if [ "$diagnostics" == "none" ]; then
            save_to_csv=""
        else
            save_to_csv="""
            wait
            # Extract diagnostic data from .diag files and save to csv
            if [ -f "$rip_diag_file.diag" ]; then
                tabdiag $rip_diag_file.diag tabdiag_format.in
                wait
                python tabdiag_to_csv.py $rip_diag_file.tabdiag
            fi
            """
            # Remove intendation
            save_to_csv=$(echo "$save_to_csv" | sed 's/^            //')
        fi
        export rip_program rip_program_args ripdpdata save_to_csv
        envsubst '$rip_program $rip_program_args $ripdpdata $save_to_csv' < $run_tpl > $folder/run_"$trajplot"_traj_i.sh

        # Runs rip inside singularity container
        singularity \
            exec \
                --contain \
                --cleanenv \
                --bind $folder/:/$name/ \
                --bind $wrfdata/:/$name/WRFData/ \
            --bind $ripdpdata_dir/:/$name/RIPDP/ \
                --pwd /$name \
                "$rip_dir"ripdocker_latest.sif  \
                /bin/bash run_"$trajplot"_traj_i.sh
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
        tjst=$(($traj_t_0>$traj_t_f ? $traj_t_f : $traj_t_0))   # Min of t_0 and t_f
        tjen=$(($traj_t_0>$traj_t_f ? $traj_t_0 : $traj_t_f))   # Max of t_0 and t_f
        trajectory_title=$traj_z"_hPa_from_hour_"$traj_t_0"_to_$traj_t_f"
        Trajectory_Spec_List=$Trajectory_Spec_List"feld=arrow; ptyp=ht; tjfl=BTrajectories/"$trajplot"_traj_$traji.traj; vcor=p;>"$'\n'
        Trajectory_Spec_List=$Trajectory_Spec_List"    colr=$color; tjar=0.002,0.012; vwin=1000,500; tjst=$tjst; tjen=$tjen;>"$'\n'
        Trajectory_Spec_List=$Trajectory_Spec_List"    nolb; titl=$trajectory_title"$'\n'
        # Copies traj_plot template
        export ncarg_type Trajectory_Spec_List
        envsubst '$ncarg_type $Trajectory_Spec_List' < $tplot_tpl > $folder/$trajplot.in
    done <"$inputsfile"
    sed -i '/^[[:space:]]*$/d' $folder/$trajplot.in  # Deletes empty lines
    # Copies run template
    rip_program="rip -f"
    rip_program_args="$trajplot.in"
    save_to_csv=""
    export rip_program rip_program_args ripdpdata save_to_csv
    envsubst '$rip_program $rip_program_args $ripdpdata $save_to_csv' < $run_tpl > $folder/run_$trajplot.sh

    # Runs rip inside singularity container
    singularity \
        exec \
            --contain \
            --cleanenv \
            --bind $folder/:/$name/ \
            --bind $wrfdata/:/$name/WRFData/ \
            --bind $ripdpdata_dir/:/$name/RIPDP/ \
            --pwd /$name \
            "$rip_dir"ripdocker_latest.sif  \
            /bin/bash run_$trajplot.sh
else
    echo "Skipping plot generation..."
fi

# Enter interactive mode in singularity container
if [ $interactive -eq 1 ]; then
    singularity \
        shell \
            --contain \
            --cleanenv \
            --bind $folder/:/$name/ \
            --bind $wrfdata/:/$name/WRFData/ \
            --bind $ripdpdata_dir/:/$name/RIPDP/ \
            --pwd /$name \
            "$rip_dir"ripdocker_latest.sif
fi
