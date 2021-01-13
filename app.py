import sys
import os
import json
import array
import time
import pprint

from lib.compose import sequence
from lib.compose import misc
from lib.audio import synthesis
from lib.audio import rendering
from lib.midi import render_mid

# ----------------------------------------------------------------------------------------

with open('data/scales.json') as data:
    scales = json.load(data)

# ----------------------------------------------------------------------------------------

def test():
    print("Any!")

def render(song_comp, file_path='audio.wav'):
    audioframes_comp = []
    instr_a = synthesis.Synth(song_comp['sample_rate'], note_range=10000)
    note_durations = misc.note_durations(song_comp['bpm'], 128)
    note_cache = {}

    for i in song_comp['tracks']:
        track_audio_data = array.array('h')
        print("Rendering: " + str(i))

        note_len = i['note_length']
        note_floor = 0 #i['note_floor']
        fm_amount = 0 if 'fm_amount' not in i.keys() else i['fm_amount']

        for n in i['notes']:
            note_val = note_floor + n

            if note_val in note_cache.keys():
                note_audio = note_cache[note_val]
            else:
                track_amp = 30000 / ((note_floor * 0.2) + 1)

                note_audio = instr_a.render_note(
                    note_val, note_durations[note_len],
                    fm_amount=fm_amount, max_amp=track_amp
                )

                note_cache[note_val] = note_audio # array.array('h')

            track_audio_data += note_audio
        audioframes_comp.append(track_audio_data)

    frame_limit = int((song_comp['duration'] * 2) * song_comp['sample_rate'])
    mixed_frames = rendering.mix_frames(audioframes_comp, frame_limit)
    rendering.write_audio(file_path, mixed_frames)


def compose(conf):
    comp = {}
    comp.update(conf)
    comp['tracks'] = []

    note_durations = misc.note_durations(conf['bpm'], 128)
    max_note_count = int((conf['duration'] * 1000) / note_durations[conf['sequence_resolution']])
    input_data_path = __file__ if 'input_data_path' not in conf.keys() else conf['input_data_path']

    raw_data_seq = sequence.data_seq(input_data_path, max_note_count)
    print("Raw Data Seq: " + str(raw_data_seq))
    print("-")

    for i in conf['tracks']:
        print("Track: " + str(i).capitalize())
        comp_track = {}

        track_spec = conf['tracks'][i]

        scale = scales['CHROMATIC'] if "scale" not in track_spec.keys() else scales[track_spec['scale']]
        note_length = 16 if 'note_length' not in track_spec.keys() else track_spec['note_length']
        fm_amount = 0 if 'fm_amount' not in track_spec.keys() else track_spec['fm_amount']
        mirror_sym = 0 if 'mirror' not in track_spec.keys() else track_spec['mirror']
        destall = True if 'destall' not in track_spec.keys() else track_spec['destall']
        struct_mode = 0 if 'comp_struct' not in track_spec.keys() else track_spec['comp_struct']
        sample_step = int(conf['sequence_resolution'] / note_length)

        seq_serial = sequence.split_seq(raw_data_seq)
        print("Seq Serial: " + str(len(seq_serial)) + ": " + str(seq_serial) + "_")

        seq_sample = sequence.sample_sequence(seq_serial[:max_note_count], sample_step)
        print("Seq Sample: " + str(len(seq_sample)) + ": " + str(seq_sample))

        mirr_seq = sequence.mirror_seq(seq_sample, mirror_sym)
        print("Seq Mirror: " + str(len(mirr_seq)) + ": " + str(mirr_seq))

        seq_struct = sequence.struct_seq(mirr_seq, track_spec["note_length"], struct_mode)
        print("Seq Struct: " + str(len(seq_struct)) + ": " + str(seq_struct))

        seq_scaled = sequence.scale_seq(seq_struct, scale, destall=destall)
        print("Seq Scaled: " + str(len(seq_scaled)) + ": " + str(seq_scaled))

        final = seq_scaled

        if "arpeggiate" in track_spec.keys():
            final = sequence.arp_seq(seq_scaled, track_spec["note_floor"], track_spec["arpeggiate"]["oct"], track_spec["arpeggiate"]["mode_a-z"])


        print("Seq Arped: " + str(len(final)) + ": " + str(final))

        comp_track.update(track_spec)
        comp_track['notes'] = final

        comp['tracks'].append(comp_track)

    return comp


# ----------------------------------------------------------------------------------------

def main(spec_path):
    with open(spec_path) as data:
        spec = json.load(data)

    input_filename = os.path.basename(spec['input_data_path'])

    comp = compose(spec)
    file_name = spec['output_filename'] + '_-_' + input_filename.capitalize() + '_-_' + str(int(time.time()))

    if spec['write_comp'] or spec['write_midi']:
        comp_file_path = spec['output_data_path'] + file_name + '.json'
        midi_dir_path = spec['output_data_path']

        with open(comp_file_path, 'w') as fp:
            json.dump(comp, fp, sort_keys=True, indent=4)

        if spec['write_midi']:
            render_mid.main(comp_file_path, midi_dir_path)


    if spec['write_audio']:
        file_path = spec['output_data_path'] + file_name + '.wav'
        render(comp, file_path)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("examples/midi_raw.json")
        main("examples/midi_arp.json")
        #main("examples/song_raw.json")
        #main("examples/song_arp.json")