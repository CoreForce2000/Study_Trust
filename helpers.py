path_json = "../json/"
path_data = "../data/"

def read_json(filepath):
    import json

    with open(filepath, 'r') as f:
        return json.load(f)
    

def invert_one_to_many_dict(d):

    result = {}
    for k, v_list in d.items():
        for v in v_list:
            result[v] = k

    return result

def apply_wordlist(text, func):
    return ",".join([func(word) for word in text.split(",")])