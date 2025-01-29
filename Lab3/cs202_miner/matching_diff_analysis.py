import pandas as pd
import os
import sys

# Get the project name passed from the shell script
project_name = sys.argv[1]

# Define the file path dynamically
file_path = f'C:/Users/bhanu/OneDrive/Desktop/courses/STT_Lab/Lab3/cs202_miner/results/{project_name}/diff_analysis.csv'

# Check if the file exists before proceeding
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df['Matches'] = df.apply(lambda row: 'Yes' if row['diff_myers'] == row['diff_hist'] else 'No', axis=1)

    # Save the modified dataframe to a new CSV file
    output_path = f'C:/Users/bhanu/OneDrive/Desktop/courses/STT_Lab/Lab3/cs202_miner/results/{project_name}/matching_diff_analysis.csv'
    df.to_csv(output_path, index=False)
    
    print("File processed successfully.")
    print(df.head())
else:
    print(f"Error: {file_path} does not exist. Please check if the file was generated correctly.")
