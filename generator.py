import numpy as np
import random
from drawing.terminal_pen import TerminalPen
from grid import Grid

class Generator:
    """
    Generator will be created by main if grid is None
    """
    def __init__(self, pen: TerminalPen):
        self.grid = Grid(np.zeros((9, 9), dtype=int))
        self.pen = pen
        self.solutions = 0

    def generate_grid(self) -> Grid:
        """
        Generate a solvable sudoku board.
        """
        for i in range(3):
            self.fill_box(i)
        self.fill_grid()
        self.remove_boxes()
        self.remove_cells()
        self.pen.draw_grid(self.grid)
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
                self.pen.put(self.grid, (y, x), n, 'Filling boxes...')
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
                            self.pen.put(y, x, n, 'Filling grid...')
                            self.fill_grid()
                            if self.grid.is_filled():
                                return
                            self.pen.put(y, x, 0, 'Filling grid...')
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
