import sys
import math
import array
import numpy
import collections

if sys.version[0] == '3':
    raw_input = input

# ----------------------------------------------------------------------------------------------------------------------
cached_notes = {'NoteValue': array.array('h')}
# ----------------------------------------------------------------------------------------------------------------------


def dbg_write(bars, curr_b, note_pitch, note_duration, track_number):
    tr = ' Rendering Track: ' + str(track_number + 1)
    br = ' | Bar: ' + str(curr_b + 1 )
    no = ' | NoteValue: ' + str(note_pitch)
    dr = ' | NoteDuration: ' + str(note_duration)

    print(tr + br + no + dr)

def fm_osc(curs, op1_note, op2_note, fm_amount, frq_env, s_rate):
    op1_freq = (s_rate * (1 / (abs(op1_note) + 1)))
    op2_freq = (s_rate * (1 / (abs(op2_note) + 1))) * frq_env

    op1_sin = math.sin((math.pi * 2 * (curs % op1_freq)) / op1_freq)
    op2_sin = math.sin((math.pi * 2 * (curs % op2_freq)) / op2_freq)

    composite = op1_sin + ((op1_sin * op2_sin) * fm_amount)

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
    else:
        if int(cursor) > int(num_a_frames + num_s_frames):
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


def get_silence(note_length, s_rate):
    num_frames = int((s_rate / 1000) * (note_length * 2))
    audio_data = array.array('h')

    for i in range(num_frames):
        audio_data.append(0)

    return audio_data, num_frames


def get_note(twelvetone_note, note_value, fm_note_value, note_length, a, s, r, s_rate):
    audio_data = array.array('h')

    num_frames = int(((s_rate / 1000) * (note_length * 2)))
    note_len_list = get_twelve_tone_list(100)
    max_amplitude = 30000


    if twelvetone_note:
        current_note = note_len_list[int(numpy.clip([int(note_value)], 1, 96))]
    else:
        current_note = note_value * 100

    for i in range(num_frames):
        amp_envelope = envelope(i, num_frames, a, s, r)
        fm_freq_env = envelope(i, num_frames, a, s, r)

        osc_audio_frame = fm_osc(i, current_note, fm_note_value,
                                 0.01, fm_freq_env, s_rate)

        note_amp = 1 / (abs(note_value * (note_value * 0.001)) + 2)
        note_amp_frame = abs(max_amplitude * note_amp)

        tot_amp = (note_amp_frame * amp_envelope)
        note_frame = int(osc_audio_frame * tot_amp)

        audio_data.append(note_frame)

    return audio_data, num_frames


def render_track(track_bars, track_number, sample_rate, note_durations):
    track_audio_data = array.array('h')
    num_frames = 0

    for i in range(len(track_bars)):
        bar_notes = track_bars[i]

        for n in range(len(bar_notes)):

            b_note = bar_notes[n]

            note_duration = float(note_durations[0][track_number])

            note_key = str(b_note) + str(note_duration)

            if note_key in cached_notes:
                note_audio_data = cached_notes[note_key]
            else:
                note_audio_data = get_note(True, b_note, b_note, note_duration,
                                           0.01, 1.0, 0.2, sample_rate)

                cached_notes[note_key] = note_audio_data

            track_audio_data += note_audio_data[0]
            num_frames += note_audio_data[1]

            dbg_write(track_bars, i, b_note, note_duration, track_number)

    return [track_audio_data, num_frames]


def render_tracks(song_dict, sample_rate, note_durations):
    song_audio_data = collections.defaultdict(list)
    num_frames = 0

    for track, bar in song_dict.items():
        c_track = render_track(song_dict[track][0], track, sample_rate, note_durations)

        song_audio_data[track].append(c_track[0])
        num_frames = c_track[1]

    return [song_audio_data, num_frames]
