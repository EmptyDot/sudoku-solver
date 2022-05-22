from timeit import timeit
import numpy as np
import curses
from curses import wrapper


def time_file(stdscr, filename, number=1000000):
    with open(filename, 'r') as f:
        content = f.read()
        times = []
        percent = 0
        for i in range(number):
            times.append(timeit(stmt=content, number=1))

            if i % (number/100) == 0:
                stdscr.clear()
                percent += 1
                stdscr.addstr(0, 0, f'{percent}%')
                stdscr.refresh()
        stdscr.clear()
        stdscr.addstr(0, 0, f'number: {number}\n'
                            f'total: {sum(times)}\n'
                            f'mean: {np.mean(times)}\n'
                            f'median: {np.median(times)}\n'
                            f'std: {np.std(times)}\n'
                            f'min: {np.min(times)}\n'
                            f'max: {np.max(times)}')
        stdscr.refresh()
        stdscr.getch()

# wrapper(time_file, filename='sudoku_for_speed_test.py', number=100000)

"""
number: 100000
total: 7989.790536999913
mean: 0.07989790536999912
median: 0.025036000000000058
std: 0.2406041492989288
min: 0.002986699999837583
max: 23.329247399999986
"""

def compare_two(a: str, b: str, setup='pass'):
    ta = timeit(a, setup)
    tb = timeit(b, setup)
    print(f'fastest: {a if ta == min(ta, tb) else b}\n'
          f'a: {ta}\n'
          f'b: {tb}\n')
