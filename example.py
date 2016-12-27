import sys
from lib import composer
from lib import miscutils
from lib import orchestra


def gen_song(json_rqs):
    gen_settings = miscutils.json_to_dict(json_rqs)

    r_seed = miscutils.get_composite_seed(gen_settings['r_seed_num'],
                                          gen_settings['r_seed_string'],
                                          gen_settings['r_seed_data_path'],
                                          gen_settings['num_data_samples'])

    note_durations = composer.get_note_durations(gen_settings['bpm'], 10)
    song_dict = composer.gen_arp_jazz(gen_settings, r_seed)

    nms = gen_settings['artist_name'], gen_settings['song_name']
    filename = nms[0] + '_-_' + nms[1] + '_(' + miscutils.get_date_name() + ')'


    if gen_settings['write_json']:
        json_filename = filename

        miscutils.write_json(song_dict,
                             json_filename,
                             gen_settings['output_data_path'])


    if gen_settings['write_audio']:
        au_filename = filename + '.wav'

        raw_audio = orchestra.render_tracks(song_dict,
                                            gen_settings['sample_rate'],
                                            note_durations)

        mixed_audio = composer.mix_song(raw_audio[0])

        miscutils.write_audio(gen_settings['output_data_path'], au_filename,
                              mixed_audio, gen_settings['num_channels'],
                              gen_settings['sample_rate'], raw_audio[1])


gen_song(sys.argv[1])
