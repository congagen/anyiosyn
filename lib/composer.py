import math
import array
import numpy
import collections


def mix_tracks(song_dct):
    mixed_audio_data = array.array('h')
    num_dct_keys = len(song_dct.keys())
    max_amplitude = int(30000 / (num_dct_keys + 1)) # tfa: track_frame_amplitude
    count = 0

    for k, v in song_dct.items():
        track = k
        frames = song_dct[k][0]

        count += 1
        print('Mixing Track: ' + str(count) + ' | Frames: ' + str(len(frames)))

        for f in range(len(frames)):
            track_val = int(frames[f] / num_dct_keys)
            frame_val = numpy.clip(track_val, -max_amplitude, max_amplitude)

            if len(mixed_audio_data) <= f:
                mixed_audio_data.append(frame_val)
            else:
                mixed_audio_data[f] += frame_val


    return mixed_audio_data


def get_note_durations(bpm, num_durs):
    whole_note = (60000 * (1 / bpm)) * 4
    prev_note = whole_note * 2

    dur_list = []
    dur_dict = {}

    for i in range(num_durs):
        dur_val = (prev_note) * 0.5
        key_name = int(whole_note / dur_val)

        dur_list.append(dur_val)
        dur_dict[str(key_name)] = dur_val
        prev_note = dur_val

    return dur_list, dur_dict


def get_center_distance(total_count, cur_idx, inverted):
    mid = int(total_count * 0.5)
    distance = abs(mid - cur_idx) / mid if (cur_idx < mid) else ((cur_idx - (mid - 1)) + 1 ) / (mid + 1)

    return abs(1 - distance) if inverted else distance


def spin_maxmin(note_val, index_val, min_val):
    sin__val = math.sin(index_val * ((index_val * index_val) * 0.1))
    spin_val = int(abs(note_val * 0.5) * sin__val)

    return spin_val


def arp_pattern_gen(input_note, step_size, max_value, pattern_length, mode):
    arp_pattern = []
    arp_val = 0

    for i in range(len(pattern_length)):
        arp_val += step_size
        arp_note_val = input_note + arp_val
        arp_pattern.append(arp_note_val)

    return arp_pattern


def get_section_interval(root_interval, iter_count):
    cur_part = root_interval
    parts = []

    for i in range(iter_count):
        cur_part = root_interval * (2**i)
        parts.append(cur_part)

    return parts


def get_step_len(list_data, iter_len):
    return abs(int(len(list_data) / iter_len))


def rotate_pattern(lsit_data, shift_count):
    return lsit_data[-shift_count % len(lsit_data):] + lsit_data[:-shift_count % len(lsit_data)]


def note_to_scale(num_to_match, note_scale):
    return min(note_scale, key = lambda x: abs(x - num_to_match))


def get_base_pattern(seed_val, bp_length):
    base_pattern = []

    for i in range(bp_length):
        val = abs(int(12 * math.sin(seed_val * i)))
        base_pattern.append(val)

    return base_pattern


def sin_index(item_list, sin_vals):

    s_val = abs(math.sin(sum(sin_vals)))
    idx = int(len(item_list) * s_val)

    return idx


def iterate_m(z, maxiter):
    c = z
    for n in range(maxiter):
        if abs(z) > 2:
            return n

        z = (z ** 2) + c

    return 0


def compose_mandelbrot(gen_conf, note_index, bar, c_distance):
    sequence = []

    note_count_track = gen_conf['note_count_track'] if (
        'note_count_track' in gen_conf.keys()
    ) else 160

    scale = gen_conf['scale'] if (
        'scale' in gen_conf.keys()
    ) else [1,2,3,4,5,6,7,8,9,10,11,12]

    note_floor = gen_conf['note_floor'] if (
        'note_floor' in gen_conf.keys()
    ) else 0

    destall = gen_conf['destall'] if (
        'destall' in gen_conf.keys()
    ) else True

    max_iter = gen_conf['max_iter'] if (
        'max_iter' in gen_conf.keys()
    ) else 50

    raw_algo = gen_conf['raw_algo'] if (
        'raw_algo' in gen_conf.keys()
    ) else True

    x_dim = numpy.linspace(-2, 1, note_count_track + gen_conf['note_count_bar'])
    y_dim = numpy.linspace(-1.25, 1.25, note_count_track + gen_conf['note_count_bar'])

    iter_sum = 0
    new_note = 0
    prev_note = 0

    for i in range(gen_conf['note_count_bar']):
        xy_pos = note_index + i

        x_sin = int(abs(math.sin(xy_pos * 0.1)) * (len(x_dim) * 0.5))
        y_cos = int(abs(math.cos(xy_pos * 0.1)) * (len(y_dim) * 0.5))

        c = complex(x_dim[x_sin], y_dim[y_cos])

        iter_num = iterate_m(c, max_iter)

        if raw_algo:
            new_note = note_floor + iter_num
        else:
            iter_sum += iter_num
            idx = sin_index(scale, [iter_sum * iter_num * 0.1])
            new_note = (scale[idx] + note_floor)

        if prev_note == new_note and destall:
            new_note += 12

        prev_note = new_note
        sequence.append(new_note)

    return sequence


def compose_koch(gen_conf, note_index, bar, c_distance):
    sequence = []

    seq_sixth = int(gen_conf['note_count_bar'] / 6)
    k_range_a = range(int(seq_sixth * 2), int(seq_sixth * 3))
    k_range_b = range(int(seq_sixth * 3), int(seq_sixth * 4))

    step_size = gen_conf['step_size'] if (
        'step_size' in gen_conf.keys()
    ) else 3

    note_floor = gen_conf['note_floor'] if (
        'note_floor' in gen_conf.keys()
    ) else 0

    step_pos = 0

    for i in range(gen_conf['note_count_bar']):
        raw_val = 1

        if i in k_range_a:
            step_pos += step_size
            new_note = raw_val + int(step_pos)
            sequence.append(note_floor + new_note)

        elif i in k_range_b:
            step_pos -= step_size
            new_note = raw_val + int(step_pos)
            sequence.append(abs(note_floor + new_note))

        else:
            sequence.append(abs(note_floor + raw_val))

    return sequence


def compose_prime(gen_conf, note_index, bar, c_distance):
    sequence = []

    for i in range(gen_conf['note_count_bar']):
        pass

    return sequence


def compose_fibonacci(gen_conf, note_index, bar, c_distance):
    sequence = []
    seed_num = gen_conf['seed_num']



    for i in range(gen_conf['note_count_bar']):
        pass

    return sequence


def compose_raw(gen_conf, note_index, bar, c_distance):
    sequence = []

    note_floor = gen_conf['note_floor'] if (
        'note_floor' in gen_conf.keys()
    ) else 0

    seed_pattern = gen_conf['data_sample'] if (
        'seed_pattern' in gen_conf.keys()
    ) else [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    destall = gen_conf['destall'] if (
        'destall' in gen_conf.keys()
    ) else True

    prv_note = 0
    new_note = 0

    for i in range(gen_conf['note_count_bar']):
        idx = int((abs(len(seed_pattern) - 1)) * abs(c_distance))
        data_note = seed_pattern[idx]
        new_note = int(note_floor + data_note)

        if new_note == prv_note and destall:
            prv_note = new_note + 12
            sequence.append(new_note + 12)
        else:
            prv_note = new_note
            sequence.append(new_note)

    return sequence


def gen_track(rqst, track_number, bar_count, note_length, note_floor):
    track = []

    seed_pattern = get_base_pattern(rqst['seed_number'], 32)
    note_lens = get_note_durations(rqst['bpm'], 100)
    note_count_bar = int(note_lens[0][0] / note_length)
    note_count_track = int(bar_count * note_count_bar)

    step_size = rqst['step_size'] if ('note_floor' in rqst.keys()) else 1
    destall = rqst['destall'] if ('destall' in rqst.keys()) else True
    max_iter = rqst['max_iter'] if ('max_iter' in rqst.keys()) else 10
    raw_algo = rqst['raw_algo'] if ('raw_algo' in rqst.keys()) else True

    gen_conf = {'seed_num': rqst['seed_number'],
                'data_sample': rqst['data_sample'],
                'seed_pattern': seed_pattern,
                'scale': rqst['scale'],
                'bar_count': bar_count,
                'note_count_bar': note_count_bar,
                'note_count_track': note_count_track,
                'note_floor': note_floor,
                'track_number': track_number,
                'raw_algo': raw_algo,
                'destall': destall,
                'step_size': step_size,
                'max_iter': max_iter}

    for bar in range(bar_count):
        c_distance = get_center_distance(bar_count, bar, True)
        note_index = int(bar * note_count_bar)

        if rqst['comp_algo'] == 0:
            track.append(compose_raw(gen_conf, note_index, bar, c_distance))
        elif rqst['comp_algo'] == 1:
            track.append(compose_mandelbrot(gen_conf, note_index, bar, c_distance))
        elif rqst['comp_algo'] == 2:
            track.append(compose_koch(gen_conf, note_index, bar, c_distance))
        # elif rqst['comp_algo'] == 3:
        #     track.append(compose_prime(gen_conf, note_index, bar, c_distance))
        # elif rqst['comp_algo'] == 4:
        #     track.append(compose_fibonacci(gen_conf, note_index, bar, c_distance))
        else:
            track.append(compose_raw(gen_conf, note_index, bar, c_distance))

    return track


def compose_song(rqst, seed_number, data_sample, scale):
    song = collections.defaultdict(list)
    tracks = rqst['tracks']

    bpm = rqst['bpm'] if 'bpm' in rqst.keys() else 120
    note_lens = get_note_durations(bpm, 100)
    single_bar_duration = note_lens[0][0]
    bar_count = int((rqst['comp_length'] * 1000) / single_bar_duration)

    rqst['bar_count'] = bar_count
    rqst['single_bar_duration'] = single_bar_duration
    rqst['seed_number'] = seed_number
    rqst['data_sample'] = data_sample
    rqst['scale'] = scale

    for i in range(len(tracks)):
        track_conf = rqst['tracks'][i]
        note_length = int(note_lens[1][str(track_conf[0])])
        note_floor = track_conf[1]

        track = gen_track(rqst,
                          i,
                          bar_count,
                          note_length,
                          note_floor)

        song[int(note_length)].append(track)

    return song
