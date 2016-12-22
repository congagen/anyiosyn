import sys
from modules import composer
from modules import miscutils
from modules import orchestra

# ------------------------------------------------------------------------------

def gen_song(request_json):
    gen_settings = miscutils.json_to_dict(request_json)

    r_seed = miscutils.get_composite_seed(gen_settings['r_seed_num'],
                                          gen_settings['r_seed_string'],
                                          gen_settings['r_seed_data_path'],
                                          gen_settings['r_seed_data_samples'])

    note_durations = composer.get_note_durations(gen_settings['bpm'], 10)
    song_dict = composer.gen_arp_jazz(gen_settings, r_seed)

    raw_audio = orchestra.render_tracks(song_dict,
                                        gen_settings['sample_rate'],
                                        note_durations)

    mixed_audio = composer.mix_song(raw_audio[0])


    filename = gen_settings['artist_name'] + '_-_' + gen_settings['song_name'] + \
               '_-_' + miscutils.get_date_name('wav')

    miscutils.write_audio(gen_settings['output_data_path'], filename,
                          mixed_audio, gen_settings['num_channels'],
                          gen_settings['sample_rate'], raw_audio[1])

    if gen_settings['write_json'] == 1:
        json_filename = miscutils.get_date_name('json')

        miscutils.dict_to_json(song_dict,
                               json_filename,
                               gen_settings['output_data_path'])

# ------------------------------------------------------------------------------


gen_song(sys.argv[1])
