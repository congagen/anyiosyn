import numpy
import math
import sys
import statistics

# ----------------------------------------------------------------------------

def scale_seq(raw_data, scale, destall=True, note_floor=0):
    seq = []
    prev_val = 0
    seq_median = statistics.median(raw_data)

    for i in raw_data:
        idx = int(abs(math.sin(i * ( 1.0 / seq_median ) ) * len(scale) ))        
        val = scale[idx]

        if destall and prev_val == val:
            temp_s = scale.copy()
            temp_s.remove(val)
            val = temp_s[int(len(temp_s) * 0.5)]

        seq.append(val)
        prev_val = val

    return seq


def split_seq(sequence):
    seq = []

    for i in sequence:
        for n in str(int(i)):
            seq.append(int(n))

    return seq


def ordinal(sequence):
    seq = []

    for i in sequence:
        for n in str(int(i)):
            seq.append(ord(str(n)))

    return seq

# ----------------------------------------------------------------------------

def iterate_f(z, maxiter):
    c = z
    for n in range(maxiter):
        if abs(z) > 2:
            return n

        z = (z ** 2) + c

    return 0


def mandelbrot_seq(seq_length, start_offset=0, resolution=1, zoom=0.5, max_iter=100):
    seq = []

    x_dim = numpy.linspace(-2.0, 1.0, seq_length )
    y_dim = numpy.linspace(-1.25, 1.25, seq_length)

    prev_note = 0

    for i in range(start_offset, sys.maxsize**100):
        if len(seq) == seq_length:
            break        
        else:
            xy_pos = start_offset + int(i*i)

            x_sin = int(abs(math.sin(xy_pos * resolution)) * (len(x_dim) * zoom))
            y_cos = int(abs(math.cos(xy_pos * resolution)) * (len(y_dim) * zoom))
            c = complex(x_dim[x_sin], y_dim[y_cos])

            num = iterate_f(c, max_iter)
            seq.append(num)

    return seq

# ----------------------------------------------------------------------------

def linear_seq(seq_len, peak_val, mirror=True, peaks=1.0):
    sequence = []

    step_size = peak_val / ((seq_len * 0.5)-1)
    part_len = int(seq_len / (peaks * 2) )
    k_range_a = range(0, int(part_len * (peaks * 1)))

    step_pos = 0.0

    if mirror:
        seq_len = int(seq_len * 0.5)


    for i in range(seq_len):
        new_val = i * step_size
        sequence.append(new_val)

    return sequence+sequence[::-1]

# ----------------------------------------------------------------------------

def is_mersenne(n):
    k = 0
    m = 0

    while m <= n:
        m = 2**k-1
        if(n == m):
            return True
        k += 1

    return False


def prime_seq(seq_length, start_offset=0, mersenne_filter=False):
    seq = []

    for i in range(start_offset, sys.maxsize**10):  
        if len(seq) == seq_length:
            break
        else:
            is_p = i > 1

            if is_p:
                for x in range(2, i):
                    if not (i % x) and is_p:
                        is_p = False

                if mersenne_filter:
                    if is_mersenne(i):
                        seq.append(i)
                        print(i)
                else:
                    seq.append(i)

    return seq

# ----------------------------------------------------------------------------

def fibonacci_seq(seq_length, start_offset=0):
    seq = []

    for i in range(0, sys.maxsize**10):
        if len(seq) == seq_length + start_offset:
            break
        else:
            if len(seq) == 0:
                seq.append(0)
            elif len(seq) == 1:
                seq.append(1)                
            else:
                a = seq[len(seq)-1]
                b = seq[len(seq)-2]
                c = a + b

                seq.append(c)        
        
    return seq[start_offset:]

# ----------------------------------------------------------------------------

def catalan(n):
    ans = 1.0
    
    for k in range(2, n+1):
        ans = ans * (n + k) / k
    
    return ans


def catalan_seq(seq_length, start_offset=0):
    seq = []
    ans = 1.0

    for i in range(0, sys.maxsize**10):
        if len(seq) == seq_length + start_offset:
            break
        else:
            if i > 0:
                ca = int(catalan(i))
                seq.append(ca)

    return seq[start_offset:]

# ----------------------------------------------------------------------------

def recaman(n):
    def recurs(seen, i, term):
        if i > n:
            return []
        elif term > i and term - i not in seen:
            return [term - i] + recurs(seen.union({term - i}), i + 1, term - i)
        else:
            return [term + i] + recurs(seen.union({term + i}), i + 1, term + i)

    return list(recurs(set(), 1, 0))


def recaman_seq(seq_length, start_offset=0):
    sys.setrecursionlimit(seq_length*500)

    rs = [0] + recaman(abs(seq_length-1)+start_offset)

    return rs[start_offset:]

# ----------------------------------------------------------------------------

def data_seq(file_path, seq_length=0):
    seq = []

    data_source = open(file_path, 'rb')
    data_bytes = data_source.read()

    while len(seq)< seq_length:
        for b in data_bytes:
            seq.append(b)

            if len(seq) == seq_length:
                break

    data_source.close()

    return seq