#/bin/bash

# Checks that there are enough inputs
if [ $# -lt 2 ]; then
    echo "Not enough arguments provided. The input file and destination folder name are needed."
    echo "For example, the command: "
    echo "--- Submit Test.inputs MySub ---"
    echo "will make the 'MySub' folder, copy the inputs to a MySub.inputs, create "
    echo "a MySub.jobarray and submit it as 'MySub'."
    echo ""
    exit 1
fi

# Gets inputs
inputsfile=$1				            # Saves input 1 (inputs file)
folder=$2				                # Saves input 2 (folder in which to run the program)
zrek=$3                                 # Saves input 3 (option to submit in zrek)

short="-l short"                        # Short job option used for cleanup jobs in csf
if [ ! -z $zrek ]; then                 # Checks if option to submit at zrek is not empty
    if [ $zrek == "zrek" ]; then            # Checks if it is the correct flag
        echo "Submit to zrek atmos-c.q"
        z1="#$ -S /bin/bash"                    # Saves additional jobscript lines needed for zrek
        z2="#$ -q atmos-c.q"
        short=""                                # Removes short job option, not available in zrek
    else
        echo "Third argument is not zrek. I will submit to csf normally."
    fi
fi

# Address to jobarray.template and csf.py
jatemplate="/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/CSF/jobarray.template"
program="/mnt/seaes01-data01/dmg/dmg/mbcxpfh2/SpanishPlume/Analysis/CSF/csf.py"

# Creates clean working directory
mkdir -p $folder			            # Creates destiantion folder
rm -f $folder/*.inputs		            # Makes sure there is no input files inside
rm -f $folder/*.jobarray		        # Makes sure there is no other jobarray files inside

#Prepares inputs file
cp $inputsfile $folder                  # Copies inputs file to destination folder
cd $folder                              # Moves to results folder
folder=$(basename ${folder})            # Strips directory from folder
inputsfile=$(basename $inputsfile)      # Strips directory from inputsfile
mv $inputsfile $folder.inputs		    # Renames inputs file to match folder name
inputsfile=$folder.inputs               # Updates variable to match file name
wait				                    # Makes sure it has finished doing previous instructions
sed -i '/^[[:space:]]*$/d' $inputsfile  # Deletes empty lines
sed -i '$a\' $inputsfile                # Makes sure there's an empty line at the end
wait
counter=$(wc -l < $inputsfile)          # Counts number of input lines

# Creates output folders
awk -F '--outdir=' '{print "mkdir -p " $2}' $inputsfile > dirs.sh   # Gets all the paths from inputs file
awk '!visited[$0]++' dirs.sh > deduplicated_dirs.sh                 # Removes duplicates
chmod +x deduplicated_dirs.sh                                       # Makes folder creation file executable
./deduplicated_dirs.sh                                              # Executes the file, creating folders
rm dirs.sh deduplicated_dirs.sh                                     # Removes temp files

# Generates jobarray file
jafile=$folder.jobarray                                                     # Defines jobarray filename
export counter inputsfile program z1 z2                                     # Exports variables to environment
envsubst '$z1 $z2 $counter $inputsfile $program' < $jatemplate > $jafile    # Substites environment variables into jatemplate and saves as jafile

wait
# Submits job array and saves the confirmation of submission string
JOBID1=$(qsub -j y "$jafile")
echo $JOBID1				                # Prints confirmation of submission (e.g. "Your job-array 1392990.1-10:1 ("dummy.jobarray") has been submitted")
wait
JOBID2=$(echo $JOBID1 | cut -d' ' -f 3 )	# Cuts JOBID1 with delimiter ' ', and saves third element in JOBID2 (e.g. "1392990.1-10:1")
wait
JOBID3=$(echo $JOBID2 | cut -d'.' -f 1 )	# Cuts JOBID2 with delimiter '.', and saves first element in JOBID3 (e.g. "1392990")
wait

# Submits a job called zip_$folder which only runs when the jobarray finishes. The job zips all the .o files and sends an e-mail when finished.
qsub -b y -j y -hold_jid $JOBID3 -N zip_$folder -cwd $short -m e -M francisco.herreriasazcue@manchester.ac.uk zip $folder.o.zip $folder.inputs $folder.jobarray $folder.jobarray.o$JOBID3.*
# Submits a job called delo_$folder which only runs when the zip_* finishes. The job deletes all the .o files.
qsub -b y -j y -hold_jid zip_$folder -N delo_$folder -cwd $short rm $folder.inputs $folder.jobarray $folder.jobarray.o$JOBID3.* zip_$folder* delo_$folder* 
