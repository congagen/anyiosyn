
import os
import sys

import os
import sys
import json
import math
from midiutil import MIDIFile


# ----------------------------------------------------------------------------------------

# GM Instruments:

# 1-8	    Piano
# 9-16	    Chromatic Percussion
# 17-24	    Organ
# 25-32	    Guitar
# 33-40	    Bass
# 41-48	    Strings
# 49-56	    Ensemble
# 57-64	    Brass
# 65-72	    Reed
# 73-80	    Pipe
# 81-88	    Synth Lead
# 89-96	    Synth Pad
# 97-104	Synth Effects
# 105-112	Other
# 113-120	Percussive
# 121-128	Sound Effects

# ----------------------------------------------------------------------------------------

def render_midi(spec_path, o_path="", cycle_instr=False):
    with open(spec_path) as data:
        spec = json.load(data)

    tempo = spec['bpm']
    tracks = spec['tracks']


    for idx, t in enumerate(tracks):
        nts = [(x + 1) + t['note_floor'] for x in t['notes']]
        midi_track = MIDIFile(1)
        note_dur = 4 / t['note_length']

        track_notes = list(nts)
        track = 0
        channel = idx
        time = note_dur
        duration = note_dur

        volume = 127 if 'midi_volume' not in t.keys() else t['midi_volume']
        cycle_instr = False if 'cycle_instr' not in t.keys() else t['cycle_instr']
        instr_range = 1 if 'instr_range' not in t.keys() else t['instr_range']

        instrument = 1 if 'midi_instrument' not in t.keys() else t['midi_instrument']
        instrument = int(instrument-instr_range) if (instrument + instr_range) > 127 else instrument

        midi_track.addTempo(track, time, tempo)

        for i, pitch in enumerate(track_notes):
            instrument_add = 0
            if cycle_instr and instr_range > 0:
                instrument_add = int(int(abs(math.sin((i * i * math.pi * 0.1) * i)) * instr_range))

            midi_track.addProgramChange(track, channel, time * i, int(instrument + instrument_add))
            midi_track.addNote(track, channel, pitch, time * i, duration, volume)

        with open(o_path + "_" + t["track_name"] + ".mid", "wb") as output_file:
            midi_track.writeFile(output_file)


def main(spec_path, output_path):
    input_filename = os.path.basename(spec_path)

    render_midi(spec_path, output_path + input_filename)


if __name__ == "__main__":
    spec_path = sys.argv[1]
    output_path = sys.argv[2]

    main(spec_path, output_path)