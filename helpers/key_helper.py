import json

def read_key_from_file(file_path, input_name):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data[input_name]["key"]