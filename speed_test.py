from timeit import timeit
import numpy as np



def time_file(filename, number=1000000):
    with open(filename, 'r') as f:
        content = f.read()
        times = []
        percent = 0
        for i in range(number):
            times.append(timeit(stmt=content, number=1))

            if i % (number/100) == 0:
                percent += 1
                print(f'{percent}%')

        print(0, 0, f'number: {number}\n'
                            f'total: {sum(times)}\n'
                            f'mean: {np.mean(times)}\n'
                            f'median: {np.median(times)}\n'
                            f'std: {np.std(times)}\n'
                            f'min: {np.min(times)}\n'
                            f'max: {np.max(times)}')

# wrapper(time_file, filename='sudoku_for_speed_test.py', number=100000)


def compare_two(a: str, b: str, setup='pass'):
    ta = timeit(a, setup)
    tb = timeit(b, setup)
    print(f'fastest: {a if ta == min(ta, tb) else b}\n'
          f'a: {ta}\n'
          f'b: {tb}\n')
