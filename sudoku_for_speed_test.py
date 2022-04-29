import numpy as np
import random
import copy

"""
Used by speed_test.py
A copy of sudoku.py with all curses calls removed
"""


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
    def __init__(self, grid=None):

        self.solutions = 0
        if grid is None:
            self.grid = [list(np.zeros(9, dtype=int)) for _ in range(9)]
            self.generate_grid()
        else:
            self.grid = grid

    def possible(self, y: int, x: int, n: int, grid):
        """
        check if a number can be placed at the specified position.
        :param y: y-coordinate in the grid (0-8)
        :param x: x-coordinate in the grid (0-8)
        :param n: a number to check (1-9)
        :param grid: the grid to check
        :return: boolean
        """
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
        """
        solve self.grid
        """
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n, self.grid):
                            self.grid[y][x] = n
                            self.solve()
                            if self.is_filled():
                                return
                            self.grid[y][x] = 0
                    return
        return

    def is_filled(self) -> bool:
        """
        check if self.grid is full.
        """
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    return False
        return True

    def generate_grid(self):
        """
        generate a solvable sudoku board.
        """
        for i in range(0, 9, 3):
            self.fill_box(i, i + 3)
        self.fill_grid()
        self.remove_boxes()
        return

    def fill_box(self, start: int, stop: int):
        """
        fill a 3x3 box with random numbers.
        :param start: integer: top left corner of the box is (start, start)
        :param stop: integer: bottom right corner of the box is (stop, stop)
        """
        lst = list(range(1, 10))

        for y in range(start, stop):
            for x in range(start, stop):
                n = random.choice(lst)
                self.grid[y][x] = n
                lst.remove(n)
        return

    def fill_grid(self):
        """
        fills self.grid with random but valid numbers.
        """
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for n in nums:
                        if self.possible(y, x, n, self.grid):
                            self.grid[y][x] = n
                            self.fill_grid()
                            if self.is_filled():
                                return
                            self.grid[y][x] = 0
                    return
        return

    def remove_boxes(self):
        """
        remove the most possible numbers while still having only one solution evenly distributed across all boxes.
        :return:
        """
        squares = []
        while True:
            # iterate over all boxes
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    # pick a random square in the box
                    while True:
                        y = random.randrange(i, i + 3)
                        x = random.randrange(j, j + 3)
                        # check if square is filled
                        if self.grid[y][x] != 0:
                            break
                    # add square to the list for removal
                    squares.append((y, x))

            while len(squares) > 0:
                # pick a random box to remove from
                y, x = random.choice(squares)
                squares.remove((y, x))
                n = self.grid[y][x]
                self.grid[y][x] = 0  # make space empty
                _copy = copy.deepcopy(self.grid)  # make a copy
                self.solutions = 0
                self.solve_for_solutions(_copy)  # solve to get number of solutions
                if self.solutions > 1:
                    # revert the last step and return
                    self.grid[y][x] = n
                    return

    def solve_for_solutions(self, grid):
        """
        solve a copy of self.grid and set self.solutions
        """
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


# pass your own grid in or leave it as None to generate a grid
# sleep is time to wait between each number changed (only used to see what is happening)
# wrapper(main, grid=None, sleep=0)
Solver().solve()










