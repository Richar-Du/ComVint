import os
import time
import re
import json
from tqdm import tqdm

def read_jsonl_file(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as jsonl_file:
        for line in tqdm(jsonl_file):
            data_dict = json.loads(line.strip())
            data.append(data_dict)
    return data

def write_jsonl(datapath, datalist):
    with open(datapath, "w", encoding="utf-8") as fout:
        for item in datalist:
            fout.write(json.dumps(item, ensure_ascii=False) + "\n")

