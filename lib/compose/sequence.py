import math
import sys
import statistics

# ----------------------------------------------------------------------------

def scale_seq(raw_data, scale, destall=True, note_floor=0):
    seq = []
    prev_val = 0
    seq_median = statistics.median(raw_data)

    for i in raw_data:
        idx = int(abs(math.sin(i * ( 1.0 / seq_median ) ) * len(scale) ))        
        val = scale[idx]

        if destall and prev_val == val:
            temp_s = scale.copy()
            temp_s.remove(val)
            val = temp_s[int(len(temp_s) * 0.5)]

        seq.append(val)
        prev_val = val

    return seq


def split_seq(sequence):
    seq = []

    for i in sequence:
        for n in str(int(i)):
            seq.append(int(n))

    return seq


def ordinal(sequence):
    seq = []

    for i in sequence:
        for n in str(int(i)):
            seq.append(ord(str(n)))

    return seq

# ----------------------------------------------------------------------------

def data_seq(file_path, seq_length=0):
    seq = []

    data_source = open(file_path, 'rb')
    data_bytes = data_source.read()

    while len(seq)< seq_length:
        for b in data_bytes:
            seq.append(b)

            if len(seq) == seq_length:
                break

    data_source.close()

    return seq