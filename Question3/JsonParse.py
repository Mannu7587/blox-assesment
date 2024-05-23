import json
from decimal import Decimal

def parse_json_file(json_file):
    def decimal_decoder(obj):
        if isinstance(obj, str):
            try:
                return Decimal(obj)
            except:
                return obj
        return obj

    try:
        with open(json_file, 'r') as file:
            json_str = file.read()
            parsed_json = json.loads(json_str, parse_float=Decimal, parse_int=Decimal, object_hook=decimal_decoder)
            return parsed_json
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return None

# Example usage:
file_path = "data.json"
parsed_data = parse_json_file(file_path)
if parsed_data:
    print(parsed_data)





