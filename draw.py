import time
import curses



class Grid:
    def __init__(self, stdscr, sleep, grid):
        self.stdscr = stdscr
        self.sleep = sleep
        self.grid = grid
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

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

        if info:
            self.stdscr.clear()
            self.stdscr.addstr(9, 0, info)

        RED = curses.color_pair(1)

        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if i == y and j == x:
                    self.stdscr.addstr(y, x*3, str(n), RED)
                else:
                    self.stdscr.addstr(i, j*3, str(self.grid[i, j]))
        self.stdscr.refresh()

    def draw_grid(self, info: str = ''):
        """
        Show self.grid in the terminal
        :param info: status message to show in the terminal
        """

        if info:
            self.stdscr.clear()
            self.stdscr.addstr(9, 0, info)

        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                self.stdscr.addstr(i, j*3, str(self.grid[i, j]))
        self.stdscr.refresh()

