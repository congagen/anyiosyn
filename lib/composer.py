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


def arp_pattern_gen(input_notes, step_size, max_value, pattern_length, mode):
    arp_pattern = []
    max = int(pattern_length * step_size)
    arp_val = 0

    for i in range(len(pattern_length)):
        arp_val += step_size
        arp_note_val = sum(input_notes) + arp_val if (
            mode == 1
        ) else + (max - arp_val)

        arp_pattern.append(arp_note_val)

    return arp_pattern


def rotate_pattern(pattern, shift_count):
    return pattern[-shift_count % len(pattern):] + pattern[:-shift_count % len(pattern)]


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


def iterate_f(z, maxiter):
    c = z
    for n in range(maxiter):
        if abs(z) > 2:
            return n

        z = (z ** 2) + c

    return 0


def compose_mandelbrot(gen_conf, note_index, bar, c_distance):
    sequence = []

    f_resolution = gen_conf['note_count_track'] + gen_conf['note_count_bar']
    x_dim = numpy.linspace(-2.0, 1.0, f_resolution)
    y_dim = numpy.linspace(-1.25, 1.25, f_resolution)

    iter_sum = 0
    new_note = 0
    prev_note = 0

    for i in range(gen_conf['note_count_bar']):
        xy_pos = note_index + i

        x_sin = int(abs(math.sin(xy_pos * 0.1)) * (len(x_dim) * 0.5))
        y_cos = int(abs(math.cos(xy_pos * 0.1)) * (len(y_dim) * 0.5))
        c = complex(x_dim[x_sin], y_dim[y_cos])

        iter_num = iterate_f(c, gen_conf['max_iter'])

        if gen_conf['raw_algo']:
            new_note = gen_conf['note_floor'] + iter_num
        else:
            iter_sum += iter_num
            idx = sin_index(gen_conf['scale'], [iter_sum * iter_num * 0.1])
            new_note = (gen_conf['scale'][idx] + gen_conf['note_floor'])

        if prev_note == new_note and gen_conf['destall']:
            new_note += 12

        prev_note = new_note
        sequence.append(new_note)

    return sequence


def compose_koch(gen_conf, note_index, bar_num, c_distance):
    sequence = []

    seq_sixth = int(gen_conf['note_count_bar'] / 6)
    k_range_a = range(int(seq_sixth * 2), int(seq_sixth * 3))
    k_range_b = range(int(seq_sixth * 3), int(seq_sixth * 4))

    step_pos = 0

    for i in range(gen_conf['note_count_bar']):
        raw_val = 1

        if i in k_range_a:
            step_pos += gen_conf['step_size']
            new_note = raw_val + int(step_pos)
            sequence.append(gen_conf['note_floor'] + new_note)

        elif i in k_range_b:
            step_pos -= gen_conf['step_size']
            new_note = raw_val + int(step_pos)
            sequence.append(abs(gen_conf['note_floor'] + new_note))

        else:
            sequence.append(abs(gen_conf['note_floor'] + raw_val))

    return sequence


def compose_prime(gen_conf, note_index, bar_num, c_distance):
    sequence = []

    for i in range(gen_conf['note_count_bar']):
        pass

    return sequence


def compose_fibonacci(gen_conf, note_index, bar_num, c_distance):
    sequence = []
    seed_num = gen_conf['seed_num']

    for i in range(gen_conf['note_count_bar']):
        pass

    return sequence


def compose_whitneybox():
    pass

def compose_sierpinski():
    pass


def compose_raw(gen_conf, note_index, bar_num, c_distance):
    sequence = []

    note_floor = gen_conf['note_floor'] if (
        'note_floor' in gen_conf.keys()
    ) else 0

    data_sample = gen_conf['data_sample'] if (
        'seed_pattern' in gen_conf.keys()
    ) else [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    destall = gen_conf['destall'] if (
        'destall' in gen_conf.keys()
    ) else True

    prv_note = 0
    new_note = 0

    for i in range(gen_conf['note_count_bar']):
        idx = int((abs(len(data_sample) - 1)) * abs(c_distance))
        data_note = data_sample[idx]
        new_note = int(note_floor + data_note)

        if new_note == prv_note and destall:
            new_note += 12
            prv_note = new_note
            sequence.append(new_note)
        else:
            prv_note = new_note
            sequence.append(new_note)

    return sequence


def compose_track(gen_conf):
    track = []

    for bar in range(gen_conf['bar_count']):
        c_distance = get_center_distance(gen_conf['bar_count'], bar, True)
        note_index = int(bar * gen_conf['note_count_bar'])

        if gen_conf['comp_algo'] == 0:
            track.append(compose_raw(gen_conf, note_index, bar, c_distance))
        elif gen_conf['comp_algo'] == 1:
            track.append(compose_mandelbrot(gen_conf, note_index, bar, c_distance))
        elif gen_conf['comp_algo'] == 2:
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
    seed_pattern = get_base_pattern(seed_number, 32)
    note_lens = get_note_durations(rqst['bpm'], 100)

    gen_conf = {}

    gen_conf['bar_count'] = bar_count
    gen_conf['single_bar_duration'] = single_bar_duration
    gen_conf['data_sample'] = data_sample
    gen_conf['seed_number'] = seed_number
    gen_conf['scale'] = rqst['scale']
    gen_conf['raw_algo'] = rqst['raw_algo']
    gen_conf['destall'] = rqst['destall']
    gen_conf['step_size'] = rqst['step_size']
    gen_conf['max_iter'] = rqst['max_iter']
    gen_conf['comp_algo'] = rqst['comp_algo']

    gen_conf['seed_pattern'] = seed_pattern

    for i in range(len(tracks)):
        track_conf = rqst['tracks'][i]
        note_length = int(note_lens[1][str(track_conf[0])])
        note_floor = track_conf[1]

        gen_conf['note_count_bar'] = int(note_lens[0][0] / note_length)
        gen_conf['note_count_track'] = int(bar_count * gen_conf['note_count_bar'])
        gen_conf['note_floor'] = note_floor
        gen_conf['track_number'] = i
        gen_conf['note_lens'] = note_lens

        track = compose_track(gen_conf)

        song[int(note_length)].append(track)

    return song
