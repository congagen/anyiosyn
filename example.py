import sys
from lib import composer
from lib import miscutils
from lib import orchestra


def gen_song(json_rqs):
    scales = miscutils.json_to_dict("data/scales.json")
    scale = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    song_conf = miscutils.json_to_dict(json_rqs)

    r_seed = miscutils.get_composite_seed(song_conf['r_seed_num'],
                                          song_conf['r_seed_string'],
                                          song_conf['r_seed_data_path'],
                                          song_conf['num_data_samples'])

    note_durations = composer.get_note_durations(song_conf['bpm'], 100)

    song_dict = composer.compose_song(song_conf, r_seed, scale)

    nms = song_conf['artist_name'], song_conf['song_name']
    filename = nms[0] + '_-_' + nms[1] + '_(' + miscutils.get_date_name() + ')'

    if song_conf['write_json']:
        miscutils.write_json(song_dict,
                             filename,
                             song_conf['output_data_path'])


    if song_conf['write_audio']:
        au_filename = filename + '.wav'
        raw_audio = orchestra.render_tracks(song_dict,
                                            song_conf,
                                            note_durations)

        if song_conf['mix_tracks']:
            mixed_audio = composer.mix_tracks(raw_audio[0])
            miscutils.write_audio(song_conf['output_data_path'],
                                  au_filename,
                                  mixed_audio,
                                  song_conf['num_channels'],
                                  song_conf['sample_rate'],
                                  raw_audio[1])
        else:
            for k in raw_audio[0].keys():
                audio = raw_audio[0][k][0]
                miscutils.write_audio(song_conf['output_data_path'],
                                      str(k) + au_filename,
                                      audio,
                                      song_conf['num_channels'],
                                      song_conf['sample_rate'],
                                      raw_audio[1])

gen_song(sys.argv[1])
