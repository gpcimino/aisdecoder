import re
import json
from pathlib import Path

def parse_country_line(line):
    """Parse a single line of country data using regex."""
    pattern = r'(\d+)\s+(.*?)\s+([A-Z]{2})$'
    match = re.search(pattern, line.strip())
    if match:
        return {
            'code': match.group(1),
            'country': match.group(2).strip(),
            'abbreviation': match.group(3)
        }
    return None

def convert_to_json(input_file, output_file):
    """Convert the input file to JSON format using country codes as keys."""
    try:
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Process the file
        entries = {}  # Changed from list to dictionary
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                if line.strip():  # Skip empty lines
                    entry = parse_country_line(line)
                    if entry:
                        code = entry.pop('code')  # Remove code from entry since it'll be the key
                        entries[code] = entry
                    else:
                        print(f"Warning: Could not parse line {line_number}: {line.strip()}")
        
        # Write to JSON
        if entries:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
            print(f"Successfully processed {len(entries)} entries")
            print(f"JSON file created: {output_file}")
        else:
            print("No valid entries found to write to JSON")
            
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except PermissionError:
        print(f"Error: Permission denied when accessing files")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_file = "mids.txt"    # Your input file
    output_file = "mids.json"  # Your output file
    convert_to_json(input_file, output_file)