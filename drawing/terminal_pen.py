import time
import numpy as np




class TerminalPen:
    """
    Is created by Grid class. Each Grid object has a TerminalPen object.
    """
    def __init__(self, stdscr, grid: np.ndarray, sleep: int | float = 0.0):
        self.sleep = sleep
        self.grid = grid
        self.stdscr = stdscr

        self.colorPicker = Color()

        self.clear()

    def update(self, y: int, x: int, n: int, info: str = ''):
        """
        Update the terminal to show a change in self.grid

        :param y: y-coordinate in the grid (0-8)
        :param x: x-coordinate in the grid (0-8)
        :param n: a number to update to (1-9)
        :param info: status message to show in the terminal
        """
        if self.sleep:
            time.sleep(self.sleep)

        self.clear()
        self.display_info(info, len(self.grid))

        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if i == y and j == x:
                    self.stdscr.addstr(y, x*3, str(n), self.colorPicker.color('RED'))
                else:
                    self.stdscr.addstr(i, j*3, str(self.grid[i, j]))
        self.stdscr.refresh()

    def draw_grid(self, info: str = ''):
        """
        Show self.grid in the terminal

        :param info: status message to show in the terminal
        """

        self.clear()
        self.display_info(info, len(self.grid))

        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                self.stdscr.addstr(i, j*3, str(self.grid[i, j]))
        self.refresh()

    def put(self, y: int, x: int, n: int, info: str = ''):
        """
        Change a number in grid and update the terminal.

        :param y: y-coordinate in the grid (0-8)
        :param x: x-coordinate in the grid (0-8)
        :param n: a number to change (1-9)
        :param info: status message to show in the terminal
        """
        self.grid[y, x] = n
        self.update(y, x, n, info=info)

    def display_info(self, info='', y=None):
        if y is None:
            y = len(self.grid)
        self.stdscr.addstr(y, 0, info)

    def clear(self):
        self.stdscr.clear()

    def refresh(self):
        self.stdscr.refresh()

    def getch(self):
        self.stdscr.getch()
