#uv run python scripts/vdm2json.py ~/data/ais/20210919-extract.log 2>errors.log | jq -c --unbuffered '.[] | {mmsi, speed}'
import json
import ais
import sys
import csv
from typing import Dict, Optional, Set, List
from collections.abc import Iterable

def get_csv_fields_for_message_type(msg_type: int) -> List[str]:
    """
    Return relevant CSV fields for different message types.
    """
    common_fields = ['msg_type', 'mmsi', 'timestamp']
    
    type_specific_fields = {
        1: ['lat', 'lon', 'speed', 'course', 'heading', 'status'],
        2: ['lat', 'lon', 'speed', 'course', 'heading', 'status'],
        3: ['lat', 'lon', 'speed', 'course', 'heading', 'status'],
        5: ['imo_num', 'name', 'callsign', 'ship_type', 'destination', 'dim_a', 'dim_b', 'dim_c', 'dim_d'],
        18: ['lat', 'lon', 'speed', 'course', 'heading'],
        19: ['lat', 'lon', 'speed', 'course', 'heading', 'name', 'ship_type'],
        24: ['name', 'callsign', 'ship_type', 'dim_a', 'dim_b', 'dim_c', 'dim_d']
    }
    
    return common_fields + type_specific_fields.get(msg_type, [])

def decode_nmea_message(nmea_message: str, allowed_types: Set[int] = None) -> Optional[Dict]:
    """
    Decode a single NMEA VDM/VDO message to dictionary format.
    
    Args:
        nmea_message (str): NMEA VDM/VDO message string
        allowed_types (Set[int]): Set of message types to process
        
    Returns:
        dict: Decoded AIS data
        None: If message cannot be decoded or message type not in allowed_types
    """
    try:
        vdm_parts = []
        fill_bits = 0
        
        for line in nmea_message.strip().split('\n'):
            line = line.strip()
            if not line.startswith('!') and not line.startswith('$'):
                continue
                
            try:
                parts = line.split(',')
                vdm_parts.append(parts[5])
                if len(parts) >= 7:
                    fill_bits = int(parts[6].split('*')[0])
            except (IndexError, ValueError):
                continue

        if not vdm_parts:
            return None

        payload = ''.join(vdm_parts)
        decoded = dict(ais.decode(payload, fill_bits))
        
        # Filter by message type if specified
        if allowed_types and decoded.get('msg_type') not in allowed_types:
            return None
            
        return decoded
        
    except (ais.DecodeError, ValueError, IndexError) as e:
        #print(f"Error decoding message: {e}", file=sys.stderr)
        return None

def write_csv_header(writer, msg_types: Set[int]):
    """Write CSV header based on selected message types."""
    fields = set()
    for msg_type in msg_types:
        fields.update(get_csv_fields_for_message_type(msg_type))
    writer.writerow(sorted(list(fields)))
    return sorted(list(fields))

def process_nmea_file(file_path: str, output_path: str, output_format: str = 'json', 
                     msg_types: Set[int] = None) -> None:
    """
    Process NMEA file and output to specified format.
    
    Args:
        file_path (str): Input NMEA file path
        output_path (str): Output file path
        output_format (str): 'json' or 'csv'
        msg_types (Set[int]): Set of message types to process
    """
    message_count = 0
    current_message = []
    
    try:
        with open(file_path, 'r') as f_in:
            if output_format == 'json':
                with open(output_path, 'w') as f_out:
                    print("[", file=f_out)
                    
                    for line in f_in:
                        line = line.strip()
                        
                        if line.startswith('!') or line.startswith('$'):
                            if current_message:
                                decoded = decode_nmea_message('\n'.join(current_message), msg_types)
                                if decoded:
                                    if message_count > 0:
                                        print(",", file=f_out)
                                    json.dump(decoded, f_out, indent=2)
                                    message_count += 1
                                current_message = []
                            
                        current_message.append(line)
                    
                    # Process last message
                    if current_message:
                        decoded = decode_nmea_message('\n'.join(current_message), msg_types)
                        if decoded:
                            if message_count > 0:
                                print(",", file=f_out)
                            json.dump(decoded, f_out, indent=2)
                            message_count += 1
                    
                    print("\n]", file=f_out)
                    
            else:  # CSV format
                with open(output_path, 'w', newline='') as f_out:
                    writer = csv.writer(f_out)
                    header_written = False
                    fields = None
                    
                    for line in f_in:
                        line = line.strip()
                        
                        if line.startswith('!') or line.startswith('$'):
                            if current_message:
                                decoded = decode_nmea_message('\n'.join(current_message), msg_types)
                                if decoded:
                                    if not header_written:
                                        fields = write_csv_header(writer, msg_types)
                                        header_written = True
                                    
                                    # Write row with ordered fields
                                    row = [str(decoded.get(field, '')) for field in fields]
                                    writer.writerow(row)
                                    message_count += 1
                                current_message = []
                            
                        current_message.append(line)
                    
                    # Process last message
                    if current_message:
                        decoded = decode_nmea_message('\n'.join(current_message), msg_types)
                        if decoded:
                            if not header_written:
                                fields = write_csv_header(writer, msg_types)
                                header_written = True
                            row = [str(decoded.get(field, '')) for field in fields]
                            writer.writerow(row)
                            message_count += 1
                    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found", file=sys.stderr)
        return
        
    print(f"Processed {message_count} messages", file=sys.stderr)

def main():
    """
    Main function with enhanced command line options.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Decode NMEA VDM/VDO messages to JSON or CSV')
    parser.add_argument('input_file', help='Path to input file containing NMEA messages')
    parser.add_argument('output_file', help='Path to output file')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json',
                      help='Output format (default: json)')
    parser.add_argument('-m', '--messages', nargs='+',
                      help='Message types to process (e.g., 1 5 18 for position and static reports)',
                      default=1)
    args = parser.parse_args()
    print(args.messages)
    if args.messages is None:
        args.messages = 1
    if isinstance(args.messages, Iterable):
        args.messages = set([int(msg) for msg in args.messages])
    else:
        args.messages =set([int(args.messages)])

    # Process the input file
    process_nmea_file(args.input_file, args.output_file, args.format, args.messages)

if __name__ == "__main__":
    main()