import argparse
import pandas as pd
import numpy as np

def plot_histograms(csv_file, bins=10):
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Generate histograms for numeric columns
    for column in df.select_dtypes(include=['number']).columns:
        print(f'Histogram of {column}:')
        hist, bin_edges = np.histogram(df[column].dropna(), bins=bins)
        
        # Print histogram as text
        max_bar_length = 50
        max_count = max(hist) if hist.size > 0 else 1
        
        for count, edge in zip(hist, bin_edges[:-1]):
            bar = '#' * int((count / max_count) * max_bar_length)
            print(f'{edge:>10.2f} | {bar} ({count})')
        print('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate text-based histograms for each numerical column in a CSV file.')
    parser.add_argument('csv_file', help='Path to the CSV file')
    parser.add_argument('--bins', type=int, default=10, help='Number of bins for histograms (default: 10)')
    
    args = parser.parse_args()
    
    plot_histograms(args.csv_file, args.bins)
