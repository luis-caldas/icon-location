# -*- coding: utf-8 -*-

from os import path


def check_dir(received_path: str):
    return path.isdir(received_path)

def check_file(received_path: str):
    # a file can only exist as a file and nothing more
    return not path.exists(received_path) or path.isfile(received_path)
