import math
import random
import statistics

# ----------------------------------------------------------------------------


def sample_sequence(input_data, sample_distance):
    sample = input_data[::sample_distance]

    return sample


def mirror_seq(seq, mirror_sym):
    seq_a = seq[:int(len(seq) * mirror_sym)]
    seq_b = seq[:int(len(seq) * (1.0 - mirror_sym))]

    return seq_a + seq_b


def arp_seq(seq, note_floor, arp_s, mode="a", oct_size=12):
    arp_seq = []
    current_oct_multi = 1
    arp_steps = arp_s

    if mode in "cd":
        arp_steps = int(2 * arp_s)
        arp_steps = arp_steps + 1 if (arp_steps % 2 != 0) else arp_steps

    for i in range(len(seq)):
        note = seq[i]

        current_oct_multi = current_oct_multi + 1 if current_oct_multi < arp_steps else 1
        arp_val = 0

        up_max = int((oct_size * arp_steps))
        up_mid = int((oct_size * int(arp_steps * 0.5)))

        up_val = int(oct_size * current_oct_multi)
        do_val = up_max - int(oct_size * (current_oct_multi - 1))

        mode = mode.lower()

        if mode == "a":
            arp_val = up_val
        elif mode == "b":
            arp_val = up_max - (int(oct_size * (current_oct_multi - 1)))
        elif mode == "c":
            arp_val = up_val if current_oct_multi < int(arp_steps * 0.5) else do_val
        elif mode == "d":
            arp_val = do_val if current_oct_multi > int(arp_steps * 0.5) else up_val
        elif mode == "e":
            arp_sine = int(math.sin(i * 0.1) * arp_s)
            arp_val  = abs(int(oct_size * arp_sine))
        elif mode == "f":
            x_arp, y_arp = math.sin(i * 0.1), math.cos(i * 0.1)
            circl = int(abs(x_arp + y_arp) * arp_s)
            arp_val = abs(int(oct_size * circl))
        elif mode == "g":
            arp_val = abs(int(oct_size * random.randint(1, arp_s)))
        else:
            z = sum([ord(i) for i in mode])
            arp_sin = int(math.sin(i * z * 0.1) * arp_s)
            arp_val = abs(int(oct_size * arp_sin))

        arp_seq.append(note_floor + note + arp_val)

    return arp_seq


def struct_seq(seq, note_len, s_mode=0):
    stru_seq = []
    bar_len = (note_len * 4)
    bar_count = int(len(seq) / bar_len)

    sample_seq = list(seq[::int(note_len)])

    if s_mode == 0:
        return seq

    if s_mode == 1:
        for bar in range(bar_count):
            for i in range(4):
                for note in range(note_len):
                    n_val = seq[bar + note]
                    stru_seq.append(n_val)

    if s_mode == 2:
        for bar in range(bar_count):
            for i in range(4):
                for note in range(note_len):
                    idx = bar + note + i
                    n_val = sample_seq[idx]

                    print("SampleSeq Len: " + str(len(sample_seq)))
                    print("IDX: " + str(idx))

                    stru_seq.append(n_val)

    remain = len(seq) - len(stru_seq)
    return stru_seq + stru_seq[:remain]


def destall_seq(raw_data, music_scale):
    seq = []
    prev_val = 0

    for i in range(len(raw_data)):
        note_val = raw_data[i]

        if prev_val == note_val:
            temp_s = music_scale.copy()
            temp_s.remove(note_val)
            note_val = temp_s[int(len(temp_s) * math.sin(i * 0.1))]

        seq.append(note_val)
        prev_val = note_val

    return seq


def scale_seq(raw_data, music_scale, destall=True):
    seq = []

    for note in raw_data:
        idx = min(range(len(music_scale)), key=lambda i: abs(music_scale[i]-note))
        val = music_scale[idx]
        seq.append(val)

    if destall:
        de_seq = destall_seq(seq, music_scale)
        return de_seq

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

    while len(seq) < seq_length:
        for b in data_bytes:
            seq.append(b)

            if len(seq) == seq_length:
                break

    data_source.close()

    return seq