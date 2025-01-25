#!/bin/bash

# Optional: Set histogram parameters
BINS=10
MIN=$(cat | awk 'BEGIN{min=999999} {if($1<min) min=$1} END{print min}')
MAX=$(cat | awk 'BEGIN{max=-999999} {if($1>max) max=$1} END{print max}')

cat | awk -v bins=$BINS -v min=$MIN -v max=$MAX '
    BEGIN { 
        bucket_width = (max - min) / bins 
        for (i = 0; i < bins; i++) { 
            buckets[i] = 0 
        }
    }
    {
        bucket_index = int(($1 - min) / bucket_width)
        if (bucket_index == bins) bucket_index = bins - 1
        buckets[bucket_index]++
    }
    END {
        max_count = 0
        for (i = 0; i < bins; i++) {
            if (buckets[i] > max_count) max_count = buckets[i]
        }
        
        for (i = 0; i < bins; i++) {
            printf "%6.2f - %6.2f | ", min + i*bucket_width, min + (i+1)*bucket_width
            count = int(50 * buckets[i] / max_count)
            for (j = 0; j < count; j++) printf "#"
            printf " (%d)\n", buckets[i]
        }
    }
' | sort -n