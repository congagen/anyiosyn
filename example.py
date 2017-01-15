import sys
from lib import composer
from lib import miscutils
from lib import orchestra


def gen_song(c_args):
    request_dct = miscutils.json_to_dict(c_args[1])

    scales = miscutils.json_to_dict('data/scales.json')
    filename = request_dct['filename'] + '_(' + miscutils.get_date_name() + ')'
    note_durations = composer.get_note_durations(request_dct['bpm'], 100)


    if len(c_args) >= 3:
        scale = list(map(lambda x: x + 1, scales[c_args[2]])) if (
            c_args[2] in scales.keys()
        ) else list(map(lambda x: x + 1, scales['CHROMATIC']))
    else:
        scale = list(map(lambda x: x + 1, scales['CHROMATIC']))


    seed_number = miscutils.get_composite_seed(request_dct['r_seed_num'],
                                               request_dct['r_seed_string'],
                                               request_dct['r_seed_data_path'],
                                               request_dct['num_data_samples'])

    data_sample = miscutils.seed_from_bin_data(request_dct['r_seed_data_path'],
                                               10000)

    song_dict = composer.compose_song(request_dct, seed_number,
                                      data_sample, scale)


    if request_dct['write_json']:
        miscutils.write_json(song_dict,
                             filename,
                             request_dct['output_data_path'])


    if request_dct['write_audio']:
        au_filename = filename + '.wav'
        raw_audio = orchestra.render_tracks(song_dict,
                                            request_dct,
                                            note_durations)

        if request_dct['mix_tracks']:
            mixed_audio = composer.mix_tracks(raw_audio[0])
            miscutils.write_audio(request_dct['output_data_path'],
                                  au_filename,
                                  mixed_audio,
                                  request_dct['num_channels'],
                                  request_dct['sample_rate'],
                                  raw_audio[1])
        else:
            for k in raw_audio[0].keys():
                audio = raw_audio[0][k][0]
                miscutils.write_audio(request_dct['output_data_path'],
                                      str(k) + au_filename,
                                      audio,
                                      request_dct['num_channels'],
                                      request_dct['sample_rate'],
                                      raw_audio[1])

gen_song(sys.argv)
#gen_song(['', 'example.json'])
