import numpy as np
import pandas as pd

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
    if pd.isna(text):
        return np.nan
    else:
        return ",".join([func(word) for word in text.split(",")])
    

def apply_word_level(series, func):
    return series.apply(lambda x: apply_wordlist(x, func))