#!/usr/bin/env python3
import sys
import numpy as np

def create_histogram(data):
    # Handle edge cases
    if len(data) == 0:
        print("No valid numeric data")
        return

    # Intelligent binning
    bins = min(len(data), 10)
    
    # Prevent division by zero
    data_range = max(data) - min(data) or 1
    bucket_width = data_range / bins

    # Calculate histogram
    hist, bin_edges = np.histogram(data, bins=bins)
    max_count = hist.max()

    # Print text histogram
    for i in range(bins):
        print(f"{bin_edges[i]:6.2f} - {bin_edges[i+1]:6.2f} | ", end='')
        bar_length = int(50 * hist[i] / max_count)
        print('#' * bar_length, end='')
        print(f" ({hist[i]})")

def main():
    # Read and filter numeric data
    data = []
    for line in sys.stdin:
        try:
            value = float(line.strip())
            data.append(value)
        except ValueError:
            continue

    create_histogram(data)

if __name__ == '__main__':
    main()