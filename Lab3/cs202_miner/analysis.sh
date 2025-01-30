#!/bin/bash

# Pre-clean and setup
echo "Performing pre-clean and setup..."

# Remove the existing diff_analysis.csv file if it exists
if [ -f "results/$1/diff_analysis.csv" ]; then
    echo "Deleting existing diff_analysis.csv for project $1..."
    rm -f "results/$1/diff_analysis.csv"
    
    # Check if the file is deleted using 'ls'
    echo "Current files in the results/$1 directory:"
    ls "results/$1"
else
    echo "No existing diff_analysis.csv found for project $1."
fi

# Ensure the results directory exists
mkdir -p "results/$1"

# Collect last 500 non-merge commits
python diff_analysis.py $1

# Run the matching diff analysis
python matching_diff_analysis.py $1

python plots.py $1

python mcc.py $1

# Additional tasks if needed
echo "Analysis completed for project $1."

# Remove temporary files, if any
echo "Cleaning up temporary files..."
rm -rf temp
rm -f *.xml *.dot

if [ -d "$1" ]; then
    echo "Deleting repository $1..."
    rm -rf "$1"
fi

echo "Cleanup completed."./