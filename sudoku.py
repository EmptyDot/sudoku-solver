import numpy as np
import curses
from curses import wrapper
import random
import time
import copy

ex_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
           [6, 0, 0, 1, 9, 5, 0, 0, 0],
           [0, 9, 8, 0, 0, 0, 0, 6, 0],
           [8, 0, 0, 0, 6, 0, 0, 0, 3],
           [4, 0, 0, 8, 0, 3, 0, 0, 1],
           [7, 0, 0, 0, 2, 0, 0, 0, 6],
           [0, 6, 0, 0, 0, 0, 2, 8, 0],
           [0, 0, 0, 4, 1, 9, 0, 0, 5],
           [0, 0, 0, 0, 8, 0, 0, 0, 0]]


class Solver:
    def __init__(self, stdscr=None, grid=None, sleep=0.0):

        self.solutions = 0
        self.sleep = sleep
        self.layer = 0
        self.stdscr = stdscr

        if grid is None:
            self.grid = [list(np.zeros(9, dtype=int)) for _ in range(9)]
            self.generate_grid()
        else:
            self.grid = grid

    def draw_grid(self):
        WHITE = curses.color_pair(2)
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                self.stdscr.addstr(i, j*3, str(self.grid[i][j]), WHITE)
        self.stdscr.refresh()

    def update(self, y, x, n, info=''):
        if self.sleep:
            time.sleep(self.sleep)

        if info:
            self.stdscr.clear()
            self.stdscr.addstr(9, 0, info)

        RED = curses.color_pair(1)
        WHITE = curses.color_pair(2)

        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if i == y and j == x:
                    self.stdscr.addstr(y, x*3, str(n), RED)
                else:
                    self.stdscr.addstr(i, j*3, str(self.grid[i][j]), WHITE)
        self.stdscr.refresh()

    def possible(self, y, x, n, grid):
        for i in range(9):
            if grid[y][i] == n or grid[i][x] == n:
                return False

        x0 = (x//3) * 3
        y0 = (y//3) * 3
        for i in range(3):
            for j in range(3):
                if grid[y0+i][x0+j] == n:
                    return False
        return True

    def solve(self):
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n, self.grid):
                            self.grid[y][x] = n
                            self.update(y, x, n, info='Solving...')
                            self.solve()
                            if self.is_filled():
                                return

                            self.grid[y][x] = 0
                            self.update(y, x, n, info='Solving...')
                    return

    def generate_grid(self):
        for i in range(0, 3, 3):
            self.fill_square(i, i+3)
        self.fill_grid()
        self.remove_number()
        self.draw_grid()
        self.stdscr.getch()
        return

    def fill_square(self, start, stop):
        lst = list(range(1, 10))

        for y in range(start, stop):
            for x in range(start, stop):
                n = random.choice(lst)
                self.grid[y][x] = n
                self.update(y, x, n)
                lst.remove(n)
        return

    def fill_grid(self):
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for n in nums:
                        if self.possible(y, x, n, self.grid):
                            self.grid[y][x] = n
                            self.update(y, x, n, info='Filling...')

                            self.set_n_solutions()
                            if self.solutions:
                                self.fill_grid()
                                if self.is_filled():
                                    return
                            self.grid[y][x] = 0
                            self.update(y, x, n, info='Filling...')
                    return
        return

    def is_filled(self):
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    return False
        return True

    def remove_number(self):
        """
        removes random numbers until there is only one solution
        """

        while True:
            # find a random space which is not empty
            y = random.randrange(9)
            x = random.randrange(9)
            n = self.grid[y][x]
            if n != 0:
                break

        self.grid[y][x] = 0  # make space empty
        self.update(y, x, 0, info=f'Removing...')
        self.set_n_solutions()  # solve to get number of solutions

        if self.solutions >= 1:
            self.remove_number()  # keep going
        elif self.solutions == 0:  
            self.update(y, x, n, info=f'Removing...')
            self.grid[y][x] = n  # revert change
            self.remove_number()  # try another number

    def set_n_solutions(self):
        """
        rewrites self.solutions
        """

        _copy = copy.deepcopy(self.grid)
        self.solutions = 0
        self.solve_for_solutions(_copy)
        self.solutions -= 1

    def solve_for_solutions(self, grid):
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n, grid):
                            grid[y][x] = n
                            self.solve_for_solutions(grid)
                            grid[y][x] = 0
                    return
        self.solutions += 1


def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.clear()
    s = Solver(stdscr)
    stdscr.getch()
    s.solve()
    stdscr.getch()

# to show the solve:
# uncomment the line below and run in terminal
wrapper(main)

# or to only show solution run:
# Solver().show_solution()









