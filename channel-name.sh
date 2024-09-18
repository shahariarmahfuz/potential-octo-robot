#!/bin/bash
# This script runs the Python file to extract m3u8 links

# Define the Python script to run
python3 channel-name.py

# Log the output or errors
if [ $? -eq 0 ]; then
  echo "Script ran successfully"
else
  echo "Error occurred while running the script" >&2
fi
