#!/bin/bash

# Define the CSV file name
echo "Enter the full path, including the extension, of the input csv datalist"
echo "(recall: must have input_file as column header), use tab for completion"
echo "and do not use the ~ shortcut for home directory: "
read -r -e -p "" datalist_fullfile

# Check if the CSV file exists
if [[ ! -f "$datalist_fullfile" ]]; then
  echo "datalist not found!"
  exit 1
fi

echo "running FSLstats on file listed in datalist: $datalist_fullfile"
col1="test"
echo $col1

col1='/mnt/z/Data_Processed/DKI/BIDS/derivatives/raw/sub-1221/ses-Plasticity/dwi_preprocessed/metrics/dki_kfa.nii'
echo $col1

# Read the CSV file line by line
while IFS=, read -r col1 || [ -n "$col1" ]; do
  # Skip empty lines
  if [[ -z "$col1" ]]; then
    continue
  fi

  input_file="${col1//$'\r'/}"
  echo $input_file
  echo "Processing: '$input_file'"  # Debugging line

  # Trim any leading/trailing spaces
  col1=$(echo "$col1" | xargs)

  # Process each row
  
  echo "input_file: $input_file"

  # Replace .nii with _mean.txt in the file path
  output_file="${input_file/.nii/_mean.txt}"
  echo "output_file: $output_file"

  # Construct and echo the FSL command
  fslcmd="fslstats ${input_file} -M > $output_file"
  echo "FSL command: ${fslcmd}"

  # Run the FSL command
  eval $fslcmd

done < "$datalist_fullfile"
