
import os
import sys
import json
import wave
import math
import numpy
import random
import datetime
import collections


def write_json(data, filename, output_path, sort=True, indent=4):
    file_path = os.path.join(output_path, filename + '.json')

    with open(file_path, 'w') as fp:
        json.dump(data, fp, sort_keys = sort, indent = indent)


def write_text(input_data, filename, output_path):
    
    file_path = os.path.join(output_path, filename + '.txt')
    with open(file_path, 'w') as fp:
        fp.write(input_data)
        fp.close()


def format_filter(file_path, allowed_ext):
    filename, extension = os.path.splitext(str(file_path))

    return str(extension).lower() in allowed_ext


def list_files(input_data_path, allowed_ext):
    data_paths = []

    if len(allowed_ext) > 0:
        if os.path.isfile(input_data_path):
            if format_filter(input_data_path, allowed_ext):
                data_paths.append(str(os.path.abspath(input_data_path)))
        else:
            for root, dirs, files in os.walk(input_data_path):
                for file in files:
                    data_path = str(os.path.join(root, file))
                    if format_filter(data_path, allowed_ext):
                        data_paths.append(os.path.abspath(data_path))
    else:
        if os.path.isfile(input_data_path):
            data_paths.append(str(os.path.abspath(input_data_path)))
        else:
            for root, dirs, files in os.walk(input_data_path):
                for file in files:
                    data_path = str(os.path.join(root, file))
                    data_paths.append(os.path.abspath(data_path))

    return data_paths