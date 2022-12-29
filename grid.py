from typing import Optional
import numpy as np



class Grid:
    def __init__(self, values: Optional[np.ndarray] = None):
        self.grid = np.zeros((9, 9), dtype=int) if values is None else values

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

    def get_pen(self) -> TerminalPen:
        return self.pen

    def __getitem__(self, coords: tuple[int, int]) -> int:
        return self.grid[coords]

    def __setitem__(self, key: tuple[int, int], value: int):
        self.grid[key] = value