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
    def __init__(self, stdscr=None, n_empty=50, grid=None, sleep=0.0):

        self.solutions = 0
        self.sleep = sleep
        self.stdscr = stdscr
        self.n_empty = n_empty
        if grid is None:
            self.grid = [list(np.zeros(9, dtype=int)) for _ in range(9)]
            self.generate_grid()
        else:
            self.grid = grid

    def draw_grid(self, info=''):
        WHITE = curses.color_pair(2)

        if info:
            self.stdscr.clear()
            self.stdscr.addstr(9, 0, info)

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
        for i in range(0, 9, 3):
            self.fill_square(i, i+3)
        self.fill_grid()
        self.remove_boxes()
        self.draw_grid(info='Grid generation done!\nPress any key to show solve.')
        self.stdscr.getch()
        return

    def fill_square(self, start, stop):
        lst = list(range(1, 10))

        for y in range(start, stop):
            for x in range(start, stop):
                n = random.choice(lst)
                self.grid[y][x] = n
                self.update(y, x, n, info='Filling...')
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

                            if self.set_n_solutions(as_bool=True):
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

    def set_n_solutions(self, as_bool=False):
        """
        rewrites self.solutions
        """

        _copy = copy.deepcopy(self.grid)

        if as_bool:
            return self.is_solvable(_copy)
        else:
            self.solutions = 0
            self.solve_for_solutions(_copy)


    def solve_for_solutions(self, grid):
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n, grid):
                            grid[y][x] = n
                            self.update(y, x, n)
                            self.solve_for_solutions(grid)

                            grid[y][x] = 0
                            self.update(y, x, n)
                    return
        self.solutions += 1


    def is_solvable(self, grid):
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n, grid):
                            grid[y][x] = n
                            self.update(y, x, n, info='Checking...')
                            if self.is_solvable(grid):
                                return True
                            grid[y][x] = 0
                            self.update(y, x, n, info='Checking...')
                    return False
        return True

    def remove_boxes(self):
        nums = []
        while True:
            # iterate over all boxes
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    # pick a random square in the box
                    while True:
                        y = random.randrange(i, i+3)
                        x = random.randrange(j, j+3)
                        # check if square is filled

                        if self.grid[y][x] != 0:
                            break
                    # add square to the list for removal
                    nums.append((y, x))

            while len(nums) > 0:
                # pick a random box to remove from
                y, x = random.choice(nums)
                nums.remove((y, x))
                n = self.grid[y][x]
                self.grid[y][x] = 0  # make space empty
                self.update(y, x, 0, info=f'Removing...')
                self.set_n_solutions()  # solve to get number of solutions
                if self.solutions > 1:
                    self.grid[y][x] = n
                    self.update(y, x, n)
                    return


def main(stdscr, grid=None, sleep=0):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.clear()
    s = Solver(stdscr, grid=grid, sleep=sleep)
    s.solve()
    s.draw_grid(info='Done!')
    stdscr.getch()


# pass your own grid in or leave it as None to generate a grid
# sleep is time to wait between each number changed (only used to see what is happening)
# wrapper(main, grid=None, sleep=0)
wrapper(main)

