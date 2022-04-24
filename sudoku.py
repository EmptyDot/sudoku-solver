import numpy as np
import curses
from curses import wrapper
import random
import warnings
import time
ex_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
           [6, 0, 0, 1, 9, 5, 0, 0, 0],
           [0, 9, 8, 0, 0, 0, 0, 6, 0],
           [8, 0, 0, 0, 6, 0, 0, 0, 3],
           [4, 0, 0, 8, 0, 3, 0, 0, 1],
           [7, 0, 0, 0, 2, 0, 0, 0, 6],
           [0, 6, 0, 0, 0, 0, 2, 8, 0],
           [0, 0, 0, 4, 1, 9, 0, 0, 5],
           [0, 0, 0, 0, 8, 0, 0, 7, 9]]


class Solver:
    def __init__(self, stdscr=None, grid=None, sleep=0.0):

        self.solutions = 0
        self.sleep = sleep
        self.stdscr = stdscr
        self.grid = self.generate_grid() if grid is None else grid

    def reset_grid(self):
        self.grid = [list(np.zeros(9, dtype=int)) for _ in range(9)]

    def update(self, y, x, n, grid=None, info=''):
        if self.sleep:
            time.sleep(self.sleep)

        grid = self.grid if grid is None else grid

        if info:
            self.stdscr.addstr(9, 0, info)

        RED = curses.color_pair(1)
        WHITE = curses.color_pair(2)

        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if i == y and j == x:
                    self.stdscr.addstr(y, x*3, str(n), RED)
                else:
                    self.stdscr.addstr(i, j*3, str(grid[i][j]), WHITE)
        self.stdscr.refresh()

    def possible(self, y, x, n, grid=None):

        grid = self.grid if grid is None else grid

        for i in range(9):
            if grid[y][i] == n:
                return False
        for i in range(9):
            if grid[i][x] == n:
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
                        if self.possible(y, x, n):
                            self.grid[y][x] = n
                            self.update(y, x, n, info='Solving...')
                            self.solve()
                            self.grid[y][x] = 0
                            self.update(y, x, n, info='Solving...')
                    return
        self.stdscr.getch()
        self.solutions += 1

    def generate_grid(self):
        self.generate_random_grid()
        self.remove_number()
        return self.grid

    def fill_square(self, start, stop):
        lst = list(range(1, 10))

        for y in range(start, stop):
            for x in range(start, stop):
                n = random.choice(lst)
                self.grid[y][x] = n
                self.update(y, x, n)
                lst.remove(n)

    def generate_random_grid(self):
        self.reset_grid()
        self.fill_square(0, 3)
        self.fill_square(3, 6)
        self.fill_square(6, 9)
        if self.fill_grid():
            return self.grid

    def fill_grid(self):
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for n in nums:
                    # n = random.randint(1, 9)

                        if self.possible(y, x, n):
                            if self.is_filled(self.grid):
                                return
                            self.grid[y][x] = n
                            self.update(y, x, n)
                            if self.is_solvable(self.grid):

                                self.fill_grid()
                            self.grid[y][x] = 0
                            self.update(y, x, n)
                    return
        return

    def is_solvable(self, grid) -> bool:
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n, grid):
                            grid[y][x] = n
                            self.update(y, x, n, grid, info='Checking if solvable...')
                            if self.is_filled(grid):
                                return True
                            self.is_solvable(grid)
                            grid[y][x] = 0
                            self.update(y, x, n, grid, info='Checking if solvable...')
                    return False
        return True

    def is_filled(self, grid):
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    return False
        return True

    def remove_number(self):
        while True:
            y = random.randrange(9)
            x = random.randrange(9)
            n = self.grid[y][x]
            if n != 0:
                break

        self.grid[y][x] = 0
        self.get_num_solutions(self.grid)
        self.update(y, x, 0, info=f'Removing...\nSolutions: {self.solutions}')
        if self.solutions == 0:
            self.grid[y][x] = n
            self.update(y, x, n, info=f'Removing...\nSolutions: {self.solutions}')
        elif self.solutions > 1:
            self.remove_number()
        return

    def get_num_solutions(self, grid):
        solutions = 0
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n, grid):
                            grid[y][x] = n
                            self.get_num_solutions(grid)
                            grid[y][x] = 0

                    return
        solutions += 1
        return solutions

def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.clear()
    Solver(stdscr).solve()


    stdscr.getch()

# to show the solve:
# uncomment the line below and run in terminal
wrapper(main)

# or to only show solution run:
# Solver().show_solution()









