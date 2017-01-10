from lib import composer

seq_len = 32
scale = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
seedlist = [1] * seq_len

cds = composer.get_center_distance(100, 0, False)

mandel = composer.compose_mandelbrot(seq_len, 0, seq_len, 1, scale, 6, 50, True)
koch = composer.compose_koch_a(seedlist, 1, 2)

print("CenterDistance: " + str(cds))
print("\n")
print("Seed: " + str(seedlist))
print("\n")
print("Mdel: " + str(mandel))
print("Koch: " + str(koch))
