

def note_durations(bpm, num_durs):
    whole_note = (60000 * (1 / bpm)) * 4
    prev_note = whole_note * 2

    dur_dict = {}

    for i in range(num_durs):
        dur_val = (prev_note) * 0.5
        key_name = int(whole_note / dur_val)

        dur_dict[key_name] = dur_val
        prev_note = dur_val

    return dur_dict
