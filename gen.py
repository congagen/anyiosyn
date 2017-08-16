from lib import compose_tools
from lib import data_mgmt
from lib import instruments


def gen_song(c_args):
    request_dct = data_mgmt.json_to_dict(c_args)

    scales = data_mgmt.json_to_dict('data/scales.json')
    filename = request_dct['filename'] + '_(' + data_mgmt.get_datetime() + ')'
    note_durations = compose_tools.get_note_durations(request_dct['bpm'], 100)


    scale = scales['CHROMATIC'] if "scale" not in request_dct.keys() else scales[request_dct["scale"]]


    seed_number = data_mgmt.get_composite_seed(request_dct['r_seed_num'],
                                               request_dct['r_seed_string'],
                                               request_dct['r_seed_data_path'],
                                               request_dct['num_data_samples'])

    data_sample = data_mgmt.seed_from_bin_data(request_dct['r_seed_data_path'],
                                               10000)

    song_comp = compose_tools.compose_song(request_dct, seed_number,
                                           data_sample, scale)


    if request_dct['write_json']:
        data_mgmt.write_json(song_comp,
                             filename,
                             request_dct['output_data_path'])


    if request_dct['write_audio']:
        au_filename = filename + '.wav'
        raw_audio = instruments.render_tracks(song_comp,
                                              request_dct,
                                              note_durations)

        if request_dct['mix_tracks']:
            mixed_audio = compose_tools.mix_tracks(raw_audio[0])
            data_mgmt.write_audio(request_dct['output_data_path'],
                                  au_filename,
                                  mixed_audio,
                                  request_dct['num_channels'],
                                  request_dct['sample_rate'],
                                  raw_audio[1])
        else:
            for k in raw_audio[0].keys():
                audio = raw_audio[0][k][0]
                track_filename = "0" + str(k) + "_" + au_filename + '.wav'

                data_mgmt.write_audio(request_dct['output_data_path'],
                                      track_filename,
                                      audio,
                                      request_dct['num_channels'],
                                      request_dct['sample_rate'],
                                      raw_audio[1])

                
gen_song(sys.argv[1])
