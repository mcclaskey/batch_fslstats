#!/bin/bash

# Bash script to call FSLstats and save the output to a text file. Bash
# is used rather than python in fsl because this is adapted from prior 
# code and because  FSLstats called from terminal can't return output, 
# thus we save to text files instead.
#
# The fslstats command that is called is "fslstats <input_file> -M"
#
# To use, generate a .csv file with a single column titled "input_file" 
# where each row contains the full filepath to a .nii file. Then run 
# the script and when prompted, specify the path to the input csv file.
# Requires FSL.
#
# For full protocol, see https://github.com/mcclaskey/batch_fslstats
#
# After running this code, run the python script compile_fsl_data.py to 
# save the contents of each text file into a csv.
#
# CMcC 4.9.2025


# Define the CSV file name
echo -e "\nRunning run_fslstats.sh\n"
echo "Enter the full path, including the extension, of the input .csv"
echo "file (recall: it must have input_file as 1 column header). Use " 
echo -e "tab for completion and do not use the ~ shortcut for home:\n"
read -r -e -p "" datalist_fullfile

# Check if the CSV file exists
if [[ ! -f "$datalist_fullfile" ]]; then
  echo "datalist not found!"
  exit 1
fi
echo -e "\nRunning fslstats -M on .nii files:"

# Read the CSV file line by line
while IFS=, read -r input_file || [ -n "$input_file" ]; do
  # Skip empty lines
  if [[ -z "$input_file" ]]; then
    continue
  fi
  
  # remove carriage returns and trailing/leading whitespace
  input_file="${input_file//$'\r'/}"
  input_file=$(echo "$input_file" | xargs)



  # report to user
  echo "$input_file"
  
  # Replace .nii with _mean.txt in the file path
  output_file="${input_file/.nii/_mean.txt}"

  # Construct and echo the FSL command
  fslcmd="fslstats ${input_file} -M > $output_file"
  
  # Run the FSL command
  eval $fslcmd

done < "$datalist_fullfile"

echo -e "\nProgram complete. Output text files are saved with the same"
echo -e "filename as the original .nii, but with suffix '*_mean'.\n"