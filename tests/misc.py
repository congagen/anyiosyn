from lib import composer
from lib import miscutils


seq_len = 32
scale = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
seedlist = [1] * seq_len

gen_conf = {'seed_data': [1,654,3,87,3,85,987,4,43,98,5,3,76,3,54],
            'seed_pattern': [54,6,4356,8,43,845,9,65,64,64,654,39],
            'scale': [1,2,3,4,5,6,7,8,9,10,11,12],
            'note_count_bar': seq_len,
            'note_count_track': seq_len,
            'note_floor': 0,
            'track_number': 0,
            'bar_count': 0,
            'raw_algo': True,
            'destall': True,
            'step_size': 2,
            'max_iter': 20}

note_lens = composer.get_note_durations(60, 10)

print("\n")
print(note_lens[0])
print(note_lens[1])
print("\n")
print(note_lens[1]["1"])
print(note_lens[1]["2"])
print(note_lens[1]["4"])
print(note_lens[1]["8"])
print(note_lens[1]["16"])
print(note_lens[1]["32"])
print("\n")

center_a = composer.get_center_distance(1000, 500, False)
center_b = composer.get_center_distance(1000, 500, True)

mandel = composer.compose_mandelbrot(
    gen_conf, 0, 0, 1
)

koch = composer.compose_koch(
    gen_conf, 0, 0, 1
)

prim = composer.compose_prime(
    gen_conf, 0, 0, 1
)

fibo = composer.compose_fibonacci(
    gen_conf, 0, 0, 0.5
)

raw = composer.compose_raw(
    gen_conf, 0, 0, 1
)

print("CenterDistance_A: " + str(center_a))
print("CenterDistance_B: " + str(center_b))

print("\n")
print("Seed: " + str(seedlist))
print("Mdel: " + str(mandel))
print("Prim: " + str(prim))
print("Fibo: " + str(fibo))
print("Raw: " + str(raw))