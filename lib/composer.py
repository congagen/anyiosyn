import math
import array
import numpy
import collections


def mix_song(song_dct):
    mixed_audio_data = array.array('h')
    num_dct_keys = len(song_dct.keys())
    max_amplitude = int(30000 / (num_dct_keys + 1)) # tfa: track_frame_amplitude

    for k, v in song_dct.items():
        track = k
        frames = song_dct[k][0]

        print('Mixing Track: ' + str(track + 1) + ' | Frames: ' + str(len(frames)))

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


def iterate_j(z, maxiter):
    c = z

    for n in range(maxiter):
        if abs(z) > 2:
            return n

        z = (z ** 2) + c

    return 0


def iterate_m(z, maxiter):
    c = z

    for n in range(maxiter):
        if abs(z) > 2:
            return n

        z = (z ** 2) + c

    return 0


def compose_mandelbrot(track_l, track_x, seq_l, c_distance, scale, note_floor, max_iter, destall):
    mandel_seq = []

    x_dim = numpy.linspace(-2, 1, track_l + seq_l)
    y_dim = numpy.linspace(-1.25, 1.25, track_l + seq_l)

    iter_sum = 0
    new_note = 0
    prev_note = 0

    for i in range(seq_l):
        xy_pos = track_x + i

        x_sin = int(abs(math.sin(xy_pos * 0.1)) * (len(x_dim) * 0.5))
        y_cos = int(abs(math.cos(xy_pos * 0.1)) * (len(y_dim) * 0.5))

        c = complex(x_dim[x_sin], y_dim[y_cos])

        iter_num = iterate_m(c, max_iter)
        iter_sum += iter_num

        idx = sin_index(scale, [iter_sum * iter_num * 0.1])

        if prev_note == new_note and destall:
            new_note = (scale[idx] + note_floor) + 1
        else:
            new_note = (scale[idx] + note_floor)

        prev_note = prev_note

        mandel_seq.append(new_note)

    return mandel_seq


def compose_koch(track_l, track_x, seq_l, c_distance, scale, step_size):
    koch_seq = []
    seq_sixth = int(seq_l / 6)

    k_range_a = range(int(seq_sixth * 2), int(seq_sixth * 3))
    k_range_b = range(int(seq_sixth * 3), int(seq_sixth * 5))

    step_pos = 0

    for i in range(seq_l):
        raw_val = 1

        if i in k_range_a:
            step_pos += step_size

            kch_val = raw_val + int(step_pos)
            koch_seq.append(kch_val)
        elif i in k_range_b:
            step_pos -= step_size

            kch_val = raw_val + int(step_pos)
            koch_seq.append(abs(kch_val))
        else:
            koch_seq.append(abs(raw_val))

    return koch_seq


def basic_arp(seed_pattern, num_notes, track_number, bar_num, c_distance):
    bar = []

    for i in range(num_notes):
        init_note = seed_pattern[numpy.clip(i, 0, len(seed_pattern))]
        cent_val = abs(math.sin((c_distance * num_notes) * (c_distance * num_notes)))
        arp_num = int((((((i + bar_num) % (track_number + 1)))) * cent_val) * 12)

        bar.append(int(init_note + arp_num))

    return bar


def gen_track(s_settings, seed_data, track_number, bar_count, note_lens, scale):
    track = []
    seed_pattern = get_base_pattern(seed_data, 32)

    track_count = s_settings['num_tracks']
    note_lens = get_note_durations(s_settings['bpm'], track_count)
    note_count_bar = int(note_lens[0][0] / note_lens[0][track_number])


    for b in range(bar_count):
        center_distance = get_center_distance(bar_count, b, False)
        tot_num_notes = int(bar_count * note_count_bar)
        song_note_count = int(b * note_count_bar)

        if s_settings['comp_algo'] <= 0:
            bar = basic_arp(seed_pattern,
                            note_count_bar,
                            track_number,
                            b,
                            center_distance)

            track.append(bar)

        if s_settings['comp_algo'] == 1:
            bar = compose_koch([1] * note_count_bar,
                                center_distance,
                                1,
                                1)
            track.append(bar)

        if s_settings['comp_algo'] >= 2:
            n_floor = int(track_number * 12)

            bar = compose_mandelbrot(tot_num_notes,
                                     song_note_count,
                                     note_count_bar,
                                     center_distance,
                                     scale,
                                     n_floor,
                                     50,
                                     True)

            track.append(bar)

    return track


def compose_song(s_settings, seed_data, scale):
    song = collections.defaultdict(list)
    bpm = numpy.clip(s_settings['bpm'], 1, 9999)

    note_lens = get_note_durations(bpm, 100)
    single_bar_duration = note_lens[0][0]

    bar_count = int((s_settings['song_length'] * 1000) / single_bar_duration)

    for i in range(s_settings['num_tracks']):
        track = gen_track(s_settings,
                          seed_data,
                          i,
                          bar_count,
                          note_lens[0],
                          scale)

        song[i].append(track)

    return song
