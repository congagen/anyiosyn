import sys
import os
import json
import array
import collections
import datetime

from lib.compose import sequence
from lib.compose import misc

from lib.audio import synthesis
from lib.audio import rendering

# ----------------------------------------------------------------------------------------

with open('data/scales.json') as data:
    scales = json.load(data)

# ----------------------------------------------------------------------------------------

def render(song_comp, file_path='audio.wav'):
    audioframes_comp = []
    instr_a = synthesis.Synth(song_comp['meta']['sample_rate'], note_range=10000)
    note_durations = misc.note_durations(song_comp['meta']['bpm'], 128)
    note_cache = {}
    
    for i in song_comp['tracks']:
        track_audio_data = array.array('h')
        print("Rendering: " + str(i))

        note_len = i['note_length']
        note_floor = i['note_floor']
        fm_amount = i['fm_amount']

        for n in i['notes']:
            note_val = note_floor + n

            if note_val in note_cache.keys():
                note_audio = note_cache[note_val]
            else:
                track_amp = 30000 / ((note_floor * 0.2) + 1)

                note_audio = instr_a.render_note(
                    note_val, note_durations[note_len], fm_amount=fm_amount, max_amp=track_amp)

                note_cache[note_val] = note_audio

            track_audio_data += note_audio
        audioframes_comp.append(track_audio_data)
    
    frame_limit = int((song_comp['meta']['duration'] * 2) * song_comp['meta']['sample_rate'])
    mixed_frames = rendering.mix_frames(audioframes_comp, frame_limit)
    rendering.write_audio(file_path, mixed_frames)
    

def compose(conf):
    comp = { 'meta': conf, 'tracks': [] }

    note_durations = misc.note_durations(conf['bpm'], 128)
    max_note_count = int((conf['duration'] * 1000) / note_durations[conf['sequence_resolution']])
    input_data_path = __file__ if 'input_data_path' not in conf.keys() else conf['input_data_path']

    num_seq = sequence.data_seq(input_data_path, max_note_count)
    
    for i in conf['tracks']:
        track_spec = conf['tracks'][i]

        scale = scales['CHROMATIC'] if "scale" not in track_spec.keys() else scales[track_spec['scale']]
        note_length = 16 if 'note_length' not in track_spec.keys() else track_spec['note_length']
        note_floor = 12 if 'note_floor' not in track_spec.keys() else track_spec['note_floor']
        fm_amount = 0 if 'fm_amount' not in track_spec.keys() else track_spec['fm_amount']
        sample_step = int(conf['sequence_resolution'] / note_length)

        seq_serial = sequence.split_seq(num_seq)
        seq_sample = misc.sample_sequence(seq_serial[:max_note_count], sample_step)
        seq_scaled = sequence.scale_seq(seq_sample, scale, destall=True)

        track = {
            'note_length': note_length, 'notes': seq_scaled, 
            'note_floor':note_floor, 'fm_amount':fm_amount
        }

        comp['tracks'].append(track)

    return comp

# ----------------------------------------------------------------------------------------

def main(spec_path):
    with open(spec_path) as data:
        spec = json.load(data)
    
    input_filename = os.path.basename(spec['input_data_path'])

    comp = compose(spec)
    file_name = spec['output_filename'] + '_-_' + input_filename + '_' + str(datetime.datetime.now())

    if spec['write_comp']:
        file_path = spec['output_data_path'] + file_name + '.json'

        with open(file_path, 'w') as fp:
            json.dump(comp, fp, sort_keys = True, indent = 4)

    if spec['write_audio']:
        file_path = spec['output_data_path'] + file_name + '.wav'
        render(comp, file_path)


if __name__ == '__main__':
    main(sys.argv[1])