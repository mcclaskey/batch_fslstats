#!/bin/bash

# Define the CSV file name
echo -e "\nRunning run_fslstats.sh\n"
echo "Enter the full path, including the extension, of the input csv datalist"
echo "(recall: must have input_file as column header), use tab for completion"
echo "and do not use the ~ shortcut for home directory: "
read -r -e -p "" datalist_fullfile

# Check if the CSV file exists
if [[ ! -f "$datalist_fullfile" ]]; then
  echo "datalist not found!"
  exit 1
fi
echo -e "\nrunning fslstats -M on files listed: $datalist_fullfile"

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
echo -e "filename as the original .nii, but with the suffix '*_mean.txt'\n"