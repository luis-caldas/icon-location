# -*- coding: utf-8 -*-

import json

from os import path
from os import makedirs


def check_dir(received_path: str):
    return path.isdir(received_path)

def check_file(received_path: str):
    # a file can only exist as a file and nothing more
    return not path.exists(received_path) or path.isfile(received_path)

def write(json_data, received_path):

    absolute_path = path.abspath(received_path)

    # create the dir structure if not already present
    makedirs(path.dirname(absolute_path), exist_ok=True)

    # write to file
    with open(absolute_path, 'w') as file_d:
        file_d.write(json.dumps(json_data))

def read(received_path):
    absolute_path = path.abspath(received_path)

    with open(absolute_path) as file_d:
        return file_d.read().decode()
