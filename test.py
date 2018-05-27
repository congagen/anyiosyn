import sys
import json

from lib.compose import sequences
from lib.compose import filters
from lib.compose import misc


def test_seq():
    print("")
    # def mandelbroth_seq(seq_len, max_iter=100, start_offset=0, unstall=True):

    mndl = sequences.mandelbrot_seq(10)
    print("Mandelbroth: " + str(mndl))

    print("")

    linear = sequences.linear_seq(10, 11)
    print("Linear: " + str(linear))

    print("")

    prime = sequences.prime_seq(10, 10, False)
    print("Prime: " + str(prime))

    print("")

    fibo = sequences.fibonacci_seq(10, 10)
    print("Fibonacci: " + str(fibo))

    print("")

    catalan = sequences.catalan_seq(10, 10)
    print("Catalan: " + str(catalan))

    recaman = sequences.recaman_seq(10, 10)
    print("Recaman: " + str(recaman))
    print("")

    data = sequences.data_seq("test.py", 100)
    print("Data: " + str(data))
    print("")


def test_filter():
    scale = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    mndl = sequences.mandelbrot_seq(100)
    m = filters.seq_to_scale(mndl, scale)
    print(str(mndl) + ": " + str(m))

    prime = sequences.prime_seq(10, 100, False)
    p = filters.seq_to_scale(prime, scale)
    print(str(prime) + ": " + str(p))

    fibo = sequences.fibonacci_seq(10, 100)
    f = filters.seq_to_scale(fibo, scale)
    print(str(fibo) + ": " + str(f))

    catalan = sequences.catalan_seq(10, 100)
    c = filters.seq_to_scale(catalan, scale)
    print(str(catalan) + ": " + str(c))
    
    data = sequences.data_seq("test.py", 100)
    d = filters.seq_to_scale(data, scale)
    print(str(data) + ": " + str(d))



if __name__ == "__main__":
    test_seq()
    test_filter()
