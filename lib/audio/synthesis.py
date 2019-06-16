import math
import array


class Synth(object):
    def __init__(self,sample_rate, note_range=10000):
        self.sample_rate = sample_rate
        self.note_freq_list = []

        for i in range(note_range):
            note_freq = 27.500 * (1.0594630943592952645618252949463 ** (i + 1))
            self.note_freq_list.append(note_freq)


    def osc(self, frame_index, op1_note, op2_note, fm_multi=1, fm_amount=0):
        op1_freq = (self.sample_rate * (1 / ((self.note_freq_list[op1_note]))))
        op2_freq = (self.sample_rate * (1 / ((self.note_freq_list[op2_note])))) 

        op1_sin = math.sin((math.pi * 2 * (frame_index % op1_freq)) / op1_freq)
        op2_sin = math.sin((math.pi * 2 * (frame_index % op2_freq)) / op2_freq) * fm_multi

        composite = op1_sin - ((op1_sin * op2_sin) * fm_amount)

        return composite

    
    def envelope(self, cursor, num_frames, a, s, r):
        
        num_a_frames = int((num_frames * a))
        num_r_frames = int((num_frames * r))

        num_s_frames = num_frames - (num_a_frames + num_r_frames)
        num_s_frames = 0 if num_s_frames < 0 else num_s_frames

        current_envelope = s

        if int(cursor) < int(num_a_frames):
            current_envelope = (cursor * (s / num_a_frames)) * s

        if int(cursor) > int(num_a_frames + num_s_frames):
            c_offset = abs((num_frames - cursor)) + 0.000000001
            current_envelope = (( c_offset / (num_r_frames) ) ) * s

        e_val = max(min((current_envelope), 0.9999), 0.0)

        return e_val



    def render_note(self, note_value, note_length, adr=[0.1,1.0,0.1], fm_multi=2, fm_amount=0, max_amp=30000):
        note_audio_frames = array.array('h')
        num_frames = int(((self.sample_rate / 1000) * (note_length * 2)))
        max_amplitude = max_amp

        for i in range(num_frames):
            amp_envelope = self.envelope(i, num_frames, adr[0], adr[1], adr[2])
            audio_frame = self.osc(i, note_value, note_value, fm_multi=1, fm_amount=fm_amount)

            note_amp = 1 / (abs(note_value * (note_value * 0.001)) + 2)
            note_amp_frame = abs(max_amplitude * note_amp)

            tot_amp = (note_amp_frame * amp_envelope)
            note_frame = int(audio_frame * tot_amp)

            note_audio_frames.append(note_frame)

        return note_audio_frames
