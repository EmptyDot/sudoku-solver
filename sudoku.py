from __future__ import annotations

import numpy as np
import random
from draw import TerminalPen, Window
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


def main(grid: Optional[np.ndarray] = None, sleep: int | float = 0, difficulty: int = 0):
    """
    Main function for the program.

    :param grid: Grid object that stores information about the grid and the pen
    :param sleep: time to sleep between updates
    :param difficulty: difficulty of the grid: 0 = easy, 1 = medium, 2 = hard (default: 0)
    """
    with Window() as window:
        if grid is None:
            grid = Grid(window, sleep=sleep)
            gen = Generator(grid, difficulty)
            grid = gen.generate_grid()
        else:
            grid = Grid(window, values=grid, sleep=sleep)

        s = Solver(grid)
        s.solve_start()


class Grid:
    def __init__(self, stdscr, values: Optional[np.ndarray] = None, sleep: int | float = 0):
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

<<<<<<< HEAD
    def get_box(self, coords: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Return the coordinates of the box that the cell is inside
        :param coords: the coordinates of a cell
        :return: a list of two tuples with (start, start) and (stop, stop). top left and bottom right cells
        """
        y, x = coords
        start_y = (y // 3) * 3
        start_x = (x // 3) * 3
        stop_y = start_y + 3
        stop_x = start_x + 3
        return [(start_y, start_x), (stop_y, stop_x)]


    def get_random_in_box(self, coords: tuple[int, int]) -> tuple[int, int]:
        start, stop = self.get_box(coords)
        start_y, start_x = start
        stop_y, stop_x = stop
        rand_y = random.randint(start_y, stop_y)
        rand_x = random.randint(start_x, stop_x)
        return rand_y, rand_x


    def iter_box(self, coords: tuple[int, int]) -> tuple[int, int]:
        start, stop = self.get_box(coords)
        start_y, start_x = start
        stop_y, stop_x = stop
        for y in range(start_y, stop_y):
            for x in range(start_x, stop_x):
                yield y, x

    def iter_all_boxes(self):
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                for k in self.iter_box((i, j)):
                    yield k


    def deepcopy(self):
        return Grid(self.stdscr, self.grid)
=======
    def count_around(self, y: int, x: int) -> int:
        """
        Get the sum of all numbers around a cell.
        :param y: y-coordinate in the grid (0-8)
        :param x: x-coordinate in the grid (0-8)
        :return: sum of all numbers around the cell
        """

        count = 0
        for i in range(9):
            if self.grid[y, i] != 0 or self.grid[i, x] != 0:
                count += 1

        x0 = (x // 3) * 3
        y0 = (y // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.grid[y0 + i, x0 + j] != 0:
                    count += 1
        return count

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """
        Get all empty cells in the grid.
        :return: list of tuples (y, x)
        """
        empty_cells = []
        for y in range(9):
            for x in range(9):
                if self.grid[y, x] == 0:
                    empty_cells.append((y, x))
        return empty_cells

    def deepcopy(self) -> Grid:
        return Grid(self.stdscr, self.grid, sleep=self.pen.sleep)
>>>>>>> 2b7f4f42222023e8a536af4e6825312a704f4a86

    def get_pen(self) -> TerminalPen:
        return self.pen

    def __getitem__(self, coords: tuple[int, int]) -> int:
        return self.grid[coords]

    def __setitem__(self, key: tuple[int, int], value: int):
        self.grid[key] = value


class Generator:
    """
    Generator will be created by main if grid is None
    """
    def __init__(self, grid: Grid, difficulty: int = 0):
        self.grid = grid
        self.pen = grid.get_pen()
        self.solutions = 0
        self.difficulty = difficulty

    def generate_grid(self) -> Grid:
        """
        Generate a solvable sudoku board.
        """
        for i in range(3):
            self.fill_box(i)
        self.fill_grid()
        self.remove_boxes()
<<<<<<< HEAD
        self.remove_cells()
        self.pen.draw_grid()
=======
        self.pen.draw_grid(info=f'Grid generation done!\nPress any key to show solve. {len(self.grid.get_empty_cells())} empty cells.')
>>>>>>> 2b7f4f42222023e8a536af4e6825312a704f4a86
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
        counter = 0
        start_counter = False
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
                self.pen.put(y, x, 0, f'Removing... {counter}')

                self.get_solutions()

                if self.solutions > 1:
                    start_counter = True
                    if counter >= self.difficulty:
                        # revert the last step and return
                        self.pen.put(y, x, n)
                        return
            if start_counter:
                counter += 1


    def remove_cells(self):

        while True:
            removed = []
            dt = 0
            maxtime = 5
            for y in range(9):
                for x in range(9):
                    if self.grid[y, x] != 0:

                        n = self.grid[y, x]
                        self.pen.put(y, x, 0)
                        t0 = time.time()
                        self.get_solutions()
                        t1 = time.time()
                        dt = max(dt, t1 - t0)
                        if self.solutions > 1:
                            self.pen.put(y, x, n)
                        else:
                            removed.append((y, x))

            if not removed or dt > maxtime:
                break

    def get_solutions(self):
        """
        Make a copy of the grid and solve the copy
        :return: The number of solutions
        """
        _copy = self.grid.deepcopy()  # make a copy
        self.solutions = 0
        self.solve_for_solutions(_copy)  # solve to get number of solutions
        return self.solutions

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
    main()
