import math
import array
import numpy
import collections

# ------------------------------------------------------------------------------

def mix_song(song_dct):
    mixed_audio_data = array.array('h')
    num_dct_keys = len(song_dct.keys())
    max_tfa = int(30000 / (num_dct_keys + 1)) # tfa: track_frame_amplitude

    for k, v in song_dct.items():
        track = k
        frames = song_dct[k][0]

        print('Writing Track: ' + str(track) + ' | NumFrames: ' + str(len(frames)))

        for f in range(len(frames)):
            val_a = int(frames[f] / num_dct_keys)
            val_v = numpy.clip(val_a, -max_tfa, max_tfa)

            if len(mixed_audio_data) <= f:
                mixed_audio_data.append(val_v)
            else:
                mixed_audio_data[f] += val_v

    return mixed_audio_data


def get_note_durations(bpm, num_durs):
    whole_note = (60000 * (1 / bpm)) * 4
    prv_note = whole_note * 2

    dur_list = []
    dur_dict = {}

    for i in range(num_durs):
        dur_val = (prv_note) * 0.5
        key_name = int(whole_note / dur_val)

        dur_list.append(dur_val)
        dur_dict[str(key_name)] = dur_val
        prv_note = dur_val

    return dur_list, dur_dict


def get_structpos(c_bar):
    structure_position = 0

    if c_bar % 4 == 0:
        structure_position = 1

    if c_bar % 8 == 0:
        structure_position = 2

    if c_bar % 16 == 0:
        structure_position = 3

    if c_bar % 32 == 0:
        structure_position = 4

    return structure_position


def get_center_distance(total_count, cur_idx, inverted):
    mid = int(total_count * 0.5)
    distance = (abs(mid - cur_idx) / mid if (cur_idx < mid) else (cur_idx - (mid - 1))+1) / (mid+1)

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


def compose_bar(track, instrument, note_lens, current_bar, bar_count, track_data_notes):
    cur_bar = []
    print('Current instrument: ' + str(instrument))
    cur__note___len = float(note_lens[4])
    center_distance = get_center_distance(bar_count, current_bar, True)

    prv_bar_note = 0
    bar_note__count = int(note_lens[0] / cur__note___len)

    step_size = int(abs(len(track_data_notes) - 1) / bar_note__count)
    data_______curs = int(((len(track_data_notes) * 0.8)) * center_distance)

    max_note_pitch = int((track + 1) * 12)
    arp_val = 0

    # TODO: Get Avg Top(barnote_count) in range(step_size)

    for note in range(bar_note__count):
        # TODO: structure_pos = get_structpos(current_bar)
        # TODO: Noteprob from centerdistance

        raw_index_pos = abs(numpy.clip((data_______curs + note), 1, len(track_data_notes)) - 1)
        raw_data_note = track_data_notes[raw_index_pos]
        track_oct = int((abs(track * 12)))

        scaled_bar_note = numpy.clip((raw_data_note), 0, max_note_pitch)
        final_note = int((scaled_bar_note + track_oct) * center_distance)

        if final_note == prv_bar_note:
            cur_bar_note = int(abs(prv_bar_note - 12))
            prv_bar_note = cur_bar_note


        cur_bar.append([track, [abs(final_note), cur__note___len]])

    return cur_bar


def get_step_len(list_data, iter_len):
    return abs(int(len(list_data) / iter_len))


def rotate_pattern(lsit_data, shift_count):
    return lsit_data[-shift_count % len(lsit_data):] + lsit_data[:-shift_count % len(lsit_data)]


def compose_drone_bar(seed_data, track_number, scale, center_distance):
    pass


def note_to_scale(num_to_match, note_scale):
    return min(note_scale, key = lambda x: abs(x - num_to_match))


def get_base_pattern(seed_val, bp_length):
    base_pattern = []
    for i in range(bp_length):
        val = abs(int(12 * math.sin(seed_val * i)))

        base_pattern.append(val)

    return base_pattern


def gen_note_bar(seed_data, base_pattern, note_lens, track_number, scale, center_distance, bar_num):
    bar = []

    num_notes = int(note_lens[0] / note_lens[numpy.clip(track_number,
                                                        0, (len(note_lens) - 1))])

    for i in range(num_notes):
        init_note = base_pattern[numpy.clip(i, 0, len(base_pattern))]

        # TODO: th.pow
        cent_val = abs(math.sin((center_distance * num_notes) * (center_distance * num_notes)))
        arp_num = int((((((i + bar_num) % (track_number + 1)) )) * cent_val) * 12)

        bar.append(init_note + arp_num)

    return bar


def gen_note_track(seed_data, track_number, bar_count, note_lens):
    composed_track = []
    scale = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    base_pattern = get_base_pattern(seed_data, 32)

    for b in range(bar_count):
        cur_raw_note = abs(int(12 * math.sin(b * seed_data)))

        center_distance = get_center_distance(bar_count, b, True)
        bar = gen_note_bar(cur_raw_note, base_pattern,
                           note_lens,track_number, scale,
                           center_distance, b)

        composed_track.append(bar)

    return composed_track


def compose_song(seed_data, track_count, song_length, song_mode, bpm):
    song = collections.defaultdict(list)
    bpm = numpy.clip(bpm, 1, 9999)

    note_lens_list = get_note_durations(bpm, 7)[0]
    bar_count = int((song_length * 1000) / note_lens_list[0])

    for i in range(track_count):
        inst_track = gen_note_track(seed_data, i, bar_count, note_lens_list)
        song[i].append(inst_track)

    return song


def gen_arp_jazz(song_settings, seed_data):
    song_dict = compose_song(seed_data,
                             song_settings['num_tracks'],
                             song_settings['song_length'],
                             song_settings['song_mode'],
                             song_settings['bpm'])

    return song_dict
