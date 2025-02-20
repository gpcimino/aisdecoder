import argparse
import pandas as pd

def extract_column(csv_file, column_name, output_file=None):
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Check if column exists
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in {csv_file}")
        return
    
    # Extract column
    column_data = df[column_name].dropna()
    
    # Output to file or print to terminal
    if output_file:
        column_data.to_csv(output_file, index=False, header=True)
    else:
        print(column_data.to_string(index=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract a column from a CSV file by its name.')
    parser.add_argument('csv_file', help='Path to the CSV file')
    parser.add_argument('column_name', help='Name of the column to extract')
    parser.add_argument('--output_file', help='File to save extracted column (optional)')
    
    args = parser.parse_args()
    
    extract_column(args.csv_file, args.column_name, args.output_file)