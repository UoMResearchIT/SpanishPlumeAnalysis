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
export inputsfile=$1				    # Saves input 1 (inputs file)
export folder=$2				        # Saves input 2 (folder in which to run the program)

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
wait				                    # Makes sure it has finished doing previous instructions
sed -i '/^[[:space:]]*$/d' $inputsfile  # Deletes empty lines
wait
sed -i '$a\' $inputsfile                # Makes sure there's an empty line at the end
wait
counter=$(wc -l < $inputsfile)          # Counts number of input lines
wait
mv $inputsfile $folder.inputs		    # Renames inputs file to match folder name
inputsfile=$folder.inputs

# Generates jobarray file by substituting environment variables into jatemplate and saving as jafile
jafile=$folder.jobarray
envsubst '$counter $inputsfile $program' < $jatemplate > $jafile

wait
# Submits job array and saves the confirmation of submission string
JOBID1=$(qsub -j y "$jafile")
echo $JOBID1				                # Prints confirmation of submission (e.g. "Your job-array 1392990.1-10:1 ("dummy.jobarray") has been submitted")
wait
JOBID2=$(echo $JOBID1 | cut -d' ' -f 3 )	# Cuts JOBID1 with delimiter ' ', and saves third element in JOBID2 (e.g. "1392990.1-10:1")
wait
JOBID3=$(echo $JOBID2 | cut -d'.' -f 1 )	# Cuts JOBID2 with delimiter '.', and saves first element in JOBID3 (e.g. "1392990")
wait
