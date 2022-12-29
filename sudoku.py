from __future__ import annotations
from curses import wrapper
import numpy as np
import random
from draw import TerminalPen
from typing import Optional
import time


ex_grid = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                    [6, 0, 0, 1, 9, 5, 0, 0, 0],
                    [0, 9, 8, 0, 0, 0, 0, 6, 0],
                    [8, 0, 0, 0, 6, 0, 0, 0, 3],
                    [4, 0, 0, 8, 0, 3, 0, 0, 1],
                    [7, 0, 0, 0, 2, 0, 0, 0, 6],
                    [0, 6, 0, 0, 0, 0, 2, 8, 0],
                    [0, 0, 0, 4, 1, 9, 0, 0, 5],
                    [0, 0, 0, 0, 8, 0, 0, 0, 0]])

ex_grid2 = np.array([[4, 1, 0, 0, 0, 0, 0, 0, 6],
                     [0, 0, 6, 0, 0, 0, 0, 0, 1],
                     [0, 7, 0, 0, 0, 0, 0, 9, 0],
                     [0, 0, 0, 3, 0, 0, 5, 1, 9],
                     [7, 0, 0, 0, 4, 0, 0, 0, 0],
                     [0, 0, 0, 0, 9, 0, 0, 0, 8],
                     [0, 0, 4, 6, 0, 3, 0, 0, 0],
                     [8, 0, 0, 0, 0, 0, 0, 0, 0],
                     [6, 0, 0, 0, 7, 9, 1, 0, 0]])


# pass your own grid in or leave it as None to generate a grid
# sleep is time to wait between each number changed (only used to see what is happening)
# wrapper(main, grid=None, sleep=0)
if __name__ == '__main__':
    wrapper(main)
