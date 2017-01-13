import os
import json
import wave
import numpy
import random
import datetime
import collections


def json_to_dict(json_request):
    j_content = {}

    with open(json_request) as json_data:
        j_content = json.load(json_data)

    return j_content


def get_date_name():
    now = datetime.datetime.now()

    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    clock = str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)

    return str(date + '_' + clock)


def write_json(data_dict, filename, output_data_path):
    file_path = os.path.join(output_data_path, filename + '.json')

    with open(file_path, 'w') as fp:
        json.dump(data_dict, fp, sort_keys = True, indent = 4)


def write_audio(file_path, filename, audio_data, num_chan, s_rate, num_samples):
    n_chan = numpy.clip(num_chan, 1, 2)

    out_path = os.path.join(file_path, filename)
    f = wave.open(out_path, 'w')
    f.setparams((n_chan, 2, s_rate, num_samples, "NONE", "Uncompressed"))
    f.writeframes(audio_data.tostring())
    f.close()


def write_text(input_data, filename, output_data_path):
    file_path = os.path.join(output_data_path, filename + '.txt')
    with open(file_path, 'w') as fp:
        fp.write(input_data)
        fp.close()


def char_filter(word):
    out = ''
    for c in word:
        if c.isalpha():
            out += c

    return out


def get_ordinal(raw_string):
    ordinal = 0

    for i in str(raw_string):
        ordinal += int(ord(i))

    return ordinal


def get_full_ordinal(raw_string):
    ordinal = 0

    for i in range(len(raw_string)):
        ordinal += int(ord(raw_string[i]))

    return ordinal


def walk_dir(data_paths):
    text_data = ''
    filename = ''

    if len(data_paths) > 0:
        for i in range(len(data_paths)):
            text_data = str(format_data(data_paths[i]))
            filename = str(os.path.splitext(str(data_paths[i]))[0]) + '_0' + str(i) + '_.wav'
    else:
        print('No textfiles found in inputdata-path')

    return [text_data, filename]


def convert_range(raw_val, raw_min, raw_max, new_min, new_max):
    raw_range = int(raw_max) - raw_min
    new_range = int(new_max) - new_min
    new_value = (float(raw_val) - float(raw_min)) / float(raw_range)

    return int(new_min + (new_value * new_range))


def scale_data_avg(raw_data, min_data, max_data, min_note, max_note, min_max):
    notes = []

    c = collections.Counter(raw_data)
    most_com = c.most_common(int(len(c) * 0.5))     # Removes duplicates:

    if min_max:
        min_val = min(raw_data)
        max_val = max(raw_data)

    else:
        min_val = min_data
        max_val = max_data

    for i in range((len(most_com))):
        item_tuple = most_com[i]
        com_value = item_tuple[0]
        com_score = item_tuple[1]

        note_val = convert_range(com_value, min_val, max_val,
                                 min_note, int(max_note))

        if i % 10000 == 0:
            print('Bytevalue: ' + str(com_value) +
                  ' -> NoteValue: ' + str(note_val))

        notes.append(abs(note_val))

    return notes


def scale_data_raw(raw_data, min_data, max_data, min_note, max_note, range_from_input):
    notes = []

    if range_from_input:
        max_val = max(raw_data)
        min_val = min(raw_data)
    else:
        min_val = min_data
        max_val = max_data

    for i in range((len(raw_data))):
        note_val = convert_range(raw_data[i], min_val, max_val,
                                 min_note, int(max_note))

        if i % int(len(raw_data) * 0.1) == 0:
            print('Bytevalue: ' + str(raw_data[i]) + ' -> NoteValue: ' + str(note_val))

        notes.append(abs(note_val))

    return notes


def format_data(data_path):
    data_list = []
    raw_book = open(data_path).read()
    raw_string = raw_book.split()

    for w in range(len(raw_string)):
        if len(str(w)) > 0:
            data_list.append(char_filter(str(raw_string[w])).lower())

    return data_list


def format_filter(file_path, allowed_ext):
    filename, extension = os.path.splitext(str(file_path))

    if str(extension).lower() in allowed_ext:
        return True
    else:
        return False


def ordinal_filter(input_data):
    ordinal_data = []

    for b in range(len(input_data)):
        byte_str = str(input_data[b])

        if len(byte_str) > 0:
            orval = get_full_ordinal(byte_str)
            ordinal_data.append(orval)

    return ordinal_data


def get_data_sample(input_data, data_resolution):
    sp_data = []

    r_val = int(len(input_data) * (1 / data_resolution))
    min_v = 1
    max_v = int(len(input_data) * 0.5)

    step_size = numpy.clip(r_val, min_v, max_v)
    step_range = abs(int(len(input_data) / step_size) - 1)

    idx = 0

    for i in range(step_range):
        idx += step_size
        val = input_data[idx]

        sp_data.append(val)

    return sp_data


def get_bin_data(input_data_paths):
    bin_data = []
    idx = 0

    for i in range(len(input_data_paths)):
        data_source = open(input_data_paths[i], 'rb')
        data__bytes = data_source.read()
        byte__count = len(data__bytes)

        for b in range(byte__count):
            byte_str = str(data__bytes[b])

            if len(byte_str) > 0:
                bin_data.append(byte_str)

            if b % 10000 == 0:
                print('Reading byte: ' + str(b) + '/' + str(byte__count))

        print('Loading: ' + str(i) + ' / ' + str(len(input_data_paths)))
        data_source.close()

    return bin_data


def gather_any_data(input_data_path, allowed_ext):
    data_paths = []

    if len(allowed_ext) > 0:
        if os.path.isfile(input_data_path):
            if format_filter(input_data_path, allowed_ext):
                data_paths.append(str(input_data_path))
        else:
            for root, dirs, files in os.walk(input_data_path):
                for file in files:
                    data_path = str(os.path.join(root, file))
                    if format_filter(data_path, allowed_ext):
                        data_paths.append(data_path)
    else:
        if os.path.isfile(input_data_path):
            data_paths.append(str(input_data_path))
        else:
            for root, dirs, files in os.walk(input_data_path):
                for file in files:
                    data_path = str(os.path.join(root, file))
                    data_paths.append(data_path)

    return data_paths


def get_seed_number(num_list):
    seednum = 0

    for i in range(len(num_list)):
        if seednum < 1000000000000:
            seednum += num_list[i]

    return seednum


def seed_from_bin_data(input_data_path, seed_resolution):
    seed_number = 0

    if len(input_data_path) > 2 and os.path.isfile(input_data_path):
        raw_bin_data = get_bin_data([input_data_path])
        data_sample = get_data_sample(raw_bin_data, seed_resolution)
        ordinal_data = ordinal_filter(data_sample)
        seed_number = get_seed_number(ordinal_data)
        return seed_number
    else:
        return seed_number


def get_composite_seed(seed_int, seed_string, seed_data_path, data_res):
    strig_num = 0
    data_num = 0
    max_part_size = int(9223372036854775807 * 0.3)

    if len(seed_string) > 0:
        strig_num = numpy.clip(get_full_ordinal(seed_string), 0, max_part_size)

    if len(seed_data_path) > 0:
        data_num = numpy.clip(seed_from_bin_data(seed_data_path, data_res), 0, max_part_size)

    composite = strig_num + data_num + numpy.clip(seed_int, 0, max_part_size)

    if composite != 0:
        return int(composite)
    else:
        return random.randint(10000000, 1000000000000)
