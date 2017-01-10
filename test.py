from lib import composer

seq_len = 16
scale = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
seedlist = [1] * seq_len

center_a = composer.get_center_distance(100, 50, False)
center_b = composer.get_center_distance(100, 50, True)

mandel = composer.compose_mandelbrot(seq_len, 0, seq_len, 1, scale, 6, 50, True)
koch = composer.compose_koch_a(seedlist, 1, 12)

print("CenterDistance_A: " + str(center_a))
print("CenterDistance_B: " + str(center_b))


print("\n")
print("Seed: " + str(seedlist))
print("\n")
print("Mdel: " + str(mandel))
print("Koch: " + str(koch))
