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

# Address to jobarray.template and csf.py
current_directory=$(realpath "$(dirname "$0")")
jatemplate="${current_directory}/jobarray.template"
program="${current_directory}/csf.py"

# Creates clean working directory
mkdir -p ${folder}			            # Creates destiantion folder
rm -f ${folder}/*.inputs		        # Makes sure there is no input files inside
rm -f ${folder}/*.jobarray		        # Makes sure there is no other jobarray files inside

#Prepares inputs file
cp $inputsfile ${folder}                # Copies inputs file to destination folder
cd ${folder}                            # Moves to results folder
folder=$(basename ${folder})            # Strips directory from folder
inputsfile=$(basename $inputsfile)      # Strips directory from inputsfile
mv $inputsfile ${folder}.inputs		    # Renames inputs file to match folder name
inputsfile=${folder}.inputs             # Updates variable to match file name
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
jafile=${folder}.jobarray                                           # Defines jobarray filename
export counter inputsfile program                                   # Exports variables to environment
envsubst '$counter $inputsfile $program' < $jatemplate > $jafile    # Substites environment variables into jatemplate and saves as jafile
wait
# Submits job array and saves the confirmation of submission string
JOBID=$(sbatch --parsable "$jafile")
echo "Submitted batch job ${JOBID}"             # Prints confirmation of job array submission
wait
# Submits a job called zip_${folder} which only runs when the jobarray finishes. The job zips all the .o files and sends an e-mail when finished.
ZIPID=$(sbatch --parsable --dependency=afterany:${JOBID} --job-name=zip_${folder} -p serial -t 0-12 --mail-type=END --mail-user=francisco.herreriasazcue@manchester.ac.uk --wrap="zip ${folder}.o.zip ${folder}.inputs ${folder}.jobarray slurm-${JOBID}*")
echo "Submitted zipping job ${ZIPID}"           # Prints confirmation of zip job submission
wait
# Submits a job called delo_${folder} which only runs when the zip_* finishes. The job deletes all the .o files.
DELOID=$(sbatch --parsable --dependency=afterok:${ZIPID} --job-name=delo_${folder} -p serial -t 0-12 --wrap="rm ${folder}.inputs ${folder}.jobarray slurm-${JOBID}* slurm-${ZIPID}* slurm-${SLURM_JOB_ID}*")
echo "Submitted cleanup job ${DELOID}"          # Prints confirmation of cleanup job submission
