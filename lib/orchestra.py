import sys
import math
import array
import numpy
import collections

if sys.version[0] == '3':
    raw_input = input

# ------------------------------------------------------------------------------
cached_notes = {'NoteValue': array.array('h')}
# ------------------------------------------------------------------------------

def dbg_write(bars, curr_b, note_pitch, note_duration, track_number):
    tr = ' Rendering Track: ' + str(track_number + 1)
    br = ' | Bar: ' + str(curr_b + 1 )
    no = ' | NoteValue: ' + str(note_pitch)
    dr = ' | NoteDuration: ' + str(note_duration)

    print(tr + br + no + dr)


def fm_osc(curs, op1_note, op2_note, fm_amount, s_rate):
    op1_freq = (s_rate * (1 / (abs(op1_note) + 1)))
    op2_freq = (s_rate * (1 / (abs(op2_note) + 1)))

    op1_sin = math.sin((math.pi * 2 * (curs % op1_freq)) / op1_freq)
    op2_sin = math.sin((math.pi * 2 * (curs % op2_freq)) / op2_freq)

    composite = op1_sin - ((op1_sin * op2_sin) * fm_amount)

    return composite


def additive_osc(curs, note, harmonics, s_rate):

    harmonics_sum = sum(harmonics)
    harmonics_normalized = [h / harmonics_sum for h in harmonics]

    op1_freq = (s_rate * (1 / (abs(note) + 1)))
    h_count = len(harmonics_normalized)

    oscs = [math.sin((math.pi * 2 * (curs % op1_freq * i)) / op1_freq * i) *
            harmonics_normalized[i - 1] for i in range(1, h_count + 1)]

    composite = sum(oscs)

    return composite


def sin_osc(curs, op1_freq, frq_env, s_rate):
    op1_freq /= 2

    cur_frq = int(s_rate / op1_freq) * frq_env
    sine_val = math.sin((math.pi * 2 * (curs % cur_frq)) / cur_frq)

    return sine_val


def envelope(cursor, num_frames, a, s, r):
    num_a_frames = int((num_frames * a))
    num_s_frames = int((num_frames * (s - (a + r))))
    num_r_frames = int((num_frames * r))

    if int(cursor) < int(num_a_frames):
        current_envelope = cursor * (1 / num_a_frames)
    elif int(cursor) > int(num_a_frames + num_s_frames):
        dec_val = (1.0 / num_r_frames) * (cursor - (num_a_frames + num_s_frames))
        current_envelope = 1.0 - dec_val
    else:
        current_envelope = 1.0

    envelope_value = numpy.clip([current_envelope], 0.0001, 1.0000)

    return envelope_value


def get_twelve_tone_freq(note):
    note_val = 27.500 * (1.0594630943592952645618252949463 ** int(note))

    return int(note_val)


def get_twelve_tone_list(num_octaves):
    num_notes = int(abs(num_octaves * 12))
    note_list = []

    for i in range(num_notes):
        note_val = 27.500 * (1.0594630943592952645618252949463 ** int(i + 1))
        note_list.append(note_val)

    return note_list


def validate_dctval(dict, key_name, min_val, default_value, check_listsum):
    val = dict[key_name] if key_name in dict.keys() else default_value

    if check_listsum:
        return val if sum(val) > min_val else default_value
    else:
        return val


def get_note(rqst, use_twelvetone, note_value, fm_note_value, note_length, a, s, r, s_rate):
    audio_data = array.array('h')

    num_frames = int(((s_rate / 1000) * (note_length * 2)))
    note_freq_list = get_twelve_tone_list(100)
    max_amplitude = 30000

    harmonics = validate_dctval(rqst, 'harmonics', 0, [1], True)
    synt = validate_dctval(rqst, 'synth', 0, 0, False)
    fm_amount = validate_dctval(rqst, 'fm_amount', 0, 0, False)
    multi = validate_dctval(rqst, 'fm_multiplier', 1, 1, False)
    twelvetone = validate_dctval(rqst, 'use_twelvetone', 0, True, False)

    if twelvetone:
        current_note = note_freq_list[note_value]
    else:
        current_note = note_value * 100

    for i in range(num_frames):
        amp_envelope = envelope(i, num_frames, a, s, r)
        fm_freq_env = envelope(i, num_frames, a, s, r)
        fmn = int(fm_note_value * multi)

        osc_audio_frame = fm_osc(i, current_note, fmn,
                                 fm_amount, s_rate) if (
            synt == 0
        ) else additive_osc(i, current_note, harmonics, s_rate)

        note_amp = 1 / (abs(note_value * (note_value * 0.001)) + 2)
        note_amp_frame = abs(max_amplitude * note_amp)

        tot_amp = (note_amp_frame * amp_envelope)
        note_frame = int(osc_audio_frame * tot_amp)

        audio_data.append(note_frame)

    return audio_data, num_frames


def render_track(track_bars, track_dur, sample_rate, note_len, track_num, rqst):
    track_audio_data = array.array('h')
    num_frames = 0

    for i in range(len(track_bars)):
        bar_notes = track_bars[i]

        for n in range(len(bar_notes)):
            b_note = bar_notes[n]
            note_key = str(b_note) + str(note_len)

            if note_key in cached_notes:
                note_audio_data = cached_notes[note_key]
            else:
                note_audio_data = get_note(rqst,
                                           True,
                                           b_note,
                                           b_note,
                                           note_len,
                                           0.01,
                                           1.0,
                                           0.2,
                                           sample_rate)

                cached_notes[note_key] = note_audio_data

            track_audio_data += note_audio_data[0]
            num_frames += note_audio_data[1]

            dbg_write(track_bars, i, b_note, note_len, track_num)

    return [track_audio_data, num_frames]


def render_tracks(song_dict, rqst, note_durations):
    song_audio_data = collections.defaultdict(list)
    num_frames = 0

    sample_rate = rqst['sample_rate']
    count = 0

    for k, v in song_dict.items():
        itm = song_dict[k]
        note_len = k

        c_track = render_track(itm[0],
                               k,
                               sample_rate,
                               note_len,
                               count,
                               rqst)

        count += 1
        song_audio_data[k].append(c_track[0])
        num_frames = c_track[1]

    return [song_audio_data, num_frames]