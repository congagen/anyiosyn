import os
import array
import numpy
import wave 

# ----------------------------------------------------------------------------------

def write_audio(file_path, audio_data, frame_count=0, num_chan=2, s_rate=44100):
    n_chan = numpy.clip(num_chan, 1, 2)
    frame_count = len(audio_data) if frame_count == 0 else frame_count
    
    f = wave.open(file_path, 'w')
    f.setparams((n_chan, 2, s_rate, frame_count, "NONE", "Uncompressed"))
    f.writeframes(audio_data.tostring())
    f.close()


def mix_frames(frametracks, frame_limit, max_amplitude=30000):
    mixed_audio_data = array.array('h')
    track_count = len(frametracks)

    max_amplitude = int(max_amplitude / abs(track_count + 1))

    for i in range(len(frametracks)):
        frames = frametracks[i][:frame_limit]

        for f in range(len(frames)):
            track_val = int(frames[f] / track_count)
            frame_val = numpy.clip(track_val, -max_amplitude, max_amplitude)

            if len(mixed_audio_data) <= f:
                mixed_audio_data.append(frame_val)
            else:
                mixed_audio_data[f] += frame_val

    return mixed_audio_data