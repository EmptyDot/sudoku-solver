import numpy as np
import random
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
    def __init__(self, grid=None):
        self.solutions = 0
        if grid is None:
            self.grid = [list(np.zeros(9, dtype=int)) for _ in range(9)]
            self.generate_grid()
        else:
            self.grid = grid

    def possible(self, y, x, n, grid):
        for i in range(9):
            if grid[y][i] == n or grid[i][x] == n:
                return False
        x0 = (x//3)*3
        y0 = (y//3)*3
        for i in range(3):
            for j in range(3):
                if grid[y0 + i][x0 + j] == n:
                    return False
        return True

    def solve(self):
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

    def generate_grid(self):
        for i in range(0, 9, 3):
            self.fill_square(i, i + 3)
        self.fill_grid()
        self.remove_boxes()
        return

    def fill_square(self, start, stop):
        lst = list(range(1, 10))

        for y in range(start, stop):
            for x in range(start, stop):
                n = random.choice(lst)
                self.grid[y][x] = n
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
                            if self.set_n_solutions(as_bool=True):
                                self.fill_grid()
                            if self.is_filled():
                                return
                            self.grid[y][x] = 0
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
                            self.solve_for_solutions(grid)

                            grid[y][x] = 0
                    return
        self.solutions += 1

    def is_solvable(self, grid):
        for y in range(9):
            for x in range(9):
                if grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n, grid):
                            grid[y][x] = n
                            if self.is_solvable(grid):
                                return True
                            grid[y][x] = 0
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
                        y = random.randrange(i, i + 3)
                        x = random.randrange(j, j + 3)
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
                self.set_n_solutions()  # solve to get number of solutions
                if self.solutions > 1:
                    self.grid[y][x] = n
                    return


def main():
    s = Solver()
    s.solve()


# or to only show solution run:
# Solver().show_solution()
main()










