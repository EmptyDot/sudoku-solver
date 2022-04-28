from timeit import timeit
import numpy as np


def time_file(filename, number=1000000):
    with open(filename, 'r') as f:
        content = f.read()
        times = []
        for _ in range(number):
            times.append(timeit(stmt=content, number=1))
        print(f'mean: {np.mean(times)}')
        print(f'median: {np.median(times)}')
        print(f'std: {np.std(times)}')
        print(f'min: {np.min(times)}')
        print(f'max: {np.max(times)}')


time_file('sudoku_for_speed_test.py', number=100)


