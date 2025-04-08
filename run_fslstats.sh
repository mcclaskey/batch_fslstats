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

echo ""
echo "running FSLstats -M command on files listed in datalist: $datalist_fullfile"
echo ""
echo ""

# Read the CSV file line by line
while IFS=, read -r col1 || [ -n "$col1" ]; do
  # Skip empty lines
  if [[ -z "$col1" ]]; then
    continue
  fi

  input_file="${col1//$'\r'/}"

  # Trim any leading/trailing spaces
  col1=$(echo "$col1" | xargs)

  # report to user
  echo "$input_file"
  
  # Replace .nii with _mean.txt in the file path
  output_file="${input_file/.nii/_mean.txt}"

  # Construct and echo the FSL command
  fslcmd="fslstats ${input_file} -M > $output_file"
  
  # Run the FSL command
  eval $fslcmd

done < "$datalist_fullfile"
