import json


def read_file(filename):
    with open(filename, 'r') as f:
        data = json.loads(f.read())
        return data['candidates'], data['utilities']
    return None