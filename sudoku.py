from __future__ import annotations

import numpy as np
import curses
from curses import wrapper
import random
import copy
from draw import TerminalPen
from typing import Optional


ex_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
           [6, 0, 0, 1, 9, 5, 0, 0, 0],
           [0, 9, 8, 0, 0, 0, 0, 6, 0],
           [8, 0, 0, 0, 6, 0, 0, 0, 3],
           [4, 0, 0, 8, 0, 3, 0, 0, 1],
           [7, 0, 0, 0, 2, 0, 0, 0, 6],
           [0, 6, 0, 0, 0, 0, 2, 8, 0],
           [0, 0, 0, 4, 1, 9, 0, 0, 5],
           [0, 0, 0, 0, 8, 0, 0, 0, 0]]

ex_grid2 = np.array([[4, 1, 0, 0, 0, 0, 0, 0, 6],
                     [0, 0, 6, 0, 0, 0, 0, 0, 1],
                     [0, 7, 0, 0, 0, 0, 0, 9, 0],
                     [0, 0, 0, 3, 0, 0, 5, 1, 9],
                     [7, 0, 0, 0, 4, 0, 0, 0, 0],
                     [0, 0, 0, 0, 9, 0, 0, 0, 8],
                     [0, 0, 4, 6, 0, 3, 0, 0, 0],
                     [8, 0, 0, 0, 0, 0, 0, 0, 0],
                     [6, 0, 0, 0, 7, 9, 1, 0, 0]])


def main(stdscr: curses.window, grid: Optional[np.ndarray] = None, sleep: int | float = 0) -> None:
    if not grid:
        grid = Generator(Grid(stdscr)).generate_grid()
    else:
        grid = Grid(stdscr, values=grid, sleep=sleep)

    s = Solver(grid)
    s.solve_start()


class Grid:
    def __init__(self, stdscr: curses.window, values: Optional[np.ndarray] = None, sleep: int | float = 0) -> None:
        self.grid = np.zeros((9, 9), dtype=int) if values is None else values
        self.pen = TerminalPen(stdscr, self.grid, sleep=sleep)
        self.stdscr = stdscr

    def possible(self, y: int, x: int, n: int) -> bool:
        """
        Check if a number can be placed at the specified position.
        :param y: y-coordinate in the grid (0-8)
        :param x: x-coordinate in the grid (0-8)
        :param n: a number to check (1-9)
        :return: boolean
        """
        for i in range(9):
            if self.grid[y, i] == n or self.grid[i, x] == n:
                return False

        x0 = (x // 3) * 3
        y0 = (y // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.grid[y0 + i, x0 + j] == n:
                    return False
        return True

    def is_filled(self) -> bool:
        """
        Check if grid is full.
        """
        for y in range(9):
            for x in range(9):
                if self.grid[y, x] == 0:
                    return False
        return True

    def deepcopy(self):
        return Grid(self.stdscr, self.grid)

    def get_pen(self) -> TerminalPen:
        return self.pen

    def get_window(self) -> curses.window:
        return self.stdscr

    def __getitem__(self, coords: tuple[int, int]) -> int:
        return self.grid[coords]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.grid[key] = value


class Generator:
    """
    Generator will be created by main if grid is None
    """
    def __init__(self, grid: Grid):
        self.grid = grid
        self.pen = grid.get_pen()
        self.solutions = 0

    def generate_grid(self):
        """
        Generate a solvable sudoku board.
        """
        for i in range(3):
            self.fill_box(i)
        self.fill_grid()
        self.remove_boxes()
        self.pen.draw_grid(info='Grid generation done!\nPress any key to show solve.')
        self.pen.getch()
        return self.grid

    def fill_box(self, box: int):
        """
        Fill a 3x3 box with random numbers.

        :param box: int, in range 0-2, inclusive.
        """
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        start = box * 3
        stop = start + 3

        for y in range(start, stop):
            for x in range(start, stop):
                n = random.choice(numbers)
                self.pen.put(y, x, n, 'Filling...')
                numbers.remove(n)
        return

    def fill_grid(self):
        """
        Fill grid with random but valid numbers.
        """
        for y in range(9):
            for x in range(9):
                if self.grid[y, x] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for n in nums:
                        if self.grid.possible(y, x, n):
                            self.pen.put(y, x, n, 'Filling...')
                            self.fill_grid()
                            if self.grid.is_filled():
                                return
                            self.pen.put(y, x, 0, 'Filling...')
                    return
        return

    def remove_boxes(self):
        """
        Remove the most possible numbers while still having only one solution evenly distributed across all boxes.
        """
        cells = []
        while True:
            # iterate over all boxes
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    # pick a random cell in the box
                    while True:
                        y = random.randrange(i, i + 3)
                        x = random.randrange(j, j + 3)
                        # check if cell is filled
                        if self.grid[y, x] != 0:
                            break
                    # add cell to the list for removal
                    cells.append((y, x))

            while len(cells) > 0:
                # pick a random box to remove from
                y, x = random.choice(cells)
                cells.remove((y, x))
                n = self.grid[y, x]
                self.pen.put(y, x, 0, 'Removing...')

                _copy = self.grid.deepcopy()  # make a copy

                self.solutions = 0
                self.solve_for_solutions(_copy)  # solve to get number of solutions

                if self.solutions > 1:
                    # revert the last step and return
                    self.pen.put(y, x, n)
                    return

    def solve_for_solutions(self, grid_copy: Grid):
        """
        Solve a copy of grid and set solutions
        """
        for y in range(9):
            for x in range(9):
                if grid_copy[y, x] == 0:
                    for n in range(1, 10):
                        if grid_copy.possible(y, x, n):
                            grid_copy[y, x] = n
                            self.solve_for_solutions(grid_copy)
                            grid_copy[y, x] = 0
                    return
        self.solutions += 1


class Solver:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.pen = grid.get_pen()

    def solve_start(self):
        """
        Solve the grid and show it. To be called by main.
        """
        self.solve()
        self.pen.draw_grid(info='Done!')
        self.pen.getch()

    def solve(self):
        """
        Solve self.grid
        """
        for y in range(9):
            for x in range(9):
                if self.grid[y, x] == 0:
                    for n in range(1, 10):
                        if self.grid.possible(y, x, n):
                            self.pen.put(y, x, n, 'Solving...')
                            self.solve()
                            if self.grid.is_filled():
                                return
                            self.pen.put(y, x, 0, 'Solving...')
                    return
        return


# pass your own grid in or leave it as None to generate a grid
# sleep is time to wait between each number changed (only used to see what is happening)
# wrapper(main, grid=None, sleep=0)
if __name__ == '__main__':
    wrapper(main, sleep=0)
