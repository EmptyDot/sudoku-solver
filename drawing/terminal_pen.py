import curses
import numpy as np

from aliases import Coord
from grid import Grid

class TerminalPen:
    """
    Is created by Grid class. Each Grid object has a TerminalPen object.
    """
    def __init__(self, stdscr):
        self.stdscr = stdscr

        curses.init_pair(100, curses.COLOR_RED, curses.COLOR_BLACK)
        self.red = curses.color_pair(100)

        self.clear()

    def draw_grid(self, grid: Grid, info: str = ''):
        """
        Draw the grid
        :param grid:
        :param info: status message to show in the terminal
        """

        self.clear()
        if info:
            self.display_info(len(grid), info=info)

        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                self.stdscr.addstr(i, j*3, str(grid[i, j]))
        self.refresh()

    def put(self, grid: Grid, coords: Coord, n: int, info: str = ''):

        y, x = coords

        self.clear()
        if info:
            self.display_info(len(grid), info=info)

        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if i == y and j == x:
                    self.stdscr.addstr(y, x * 3, str(n), self.red)
                else:
                    self.stdscr.addstr(i, j * 3, str(grid[i, j]))
        self.refresh()

    def display_info(self, offset_vertical: int = 0, offset_horizontal: int = 0, info: str = ''):
        self.stdscr.addstr(offset_vertical, offset_horizontal, info)


    def clear(self):
        self.stdscr.clear()

    def refresh(self):
        self.stdscr.refresh()

    def getch(self):
        self.stdscr.getch()
