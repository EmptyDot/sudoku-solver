from __future__ import annotations

import time
import curses
import numpy as np

class Color:
    def __init__(self):
        self.colors = {
            "BLACK": curses.COLOR_BLACK,
            "BLUE": curses.COLOR_BLUE,
            "CYAN": curses.COLOR_CYAN,
            "GREEN": curses.COLOR_GREEN,
            "MAGENTA": curses.COLOR_MAGENTA,
            "RED": curses.COLOR_RED,
            "WHITE": curses.COLOR_WHITE,
            "YELLOW": curses.COLOR_YELLOW
        }
        self.pairs = []  # initialized pairs, pair_number = self.pairs.index(name)

    def color(self, name: str, color: tuple = None):
        """
        Init a new color pair if not already initialized. Call structure: RED = self.color('RED').

        :param name: String Literal: "BLACK", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "WHITE", "YELLOW"
            or any custom color names.
        :param color: Tuple: (r, g, b) values each spanning 0-1000. Only required when defining new colors.
        """
        try:
            pair = self._get_pair(name)
        except NameError:
            # name not in self.pairs
            self._set_pair(name, color)
            pair = self._get_pair(name)

        return pair

    def _get_pair(self, name: str):
        # check if pair is initialized
        if name.upper() in self.pairs:
            pair_number = self.pairs.index(name.upper()) + 1
            return curses.color_pair(pair_number)
        else:
            raise NameError(f'{name.upper()} is not a recognized color pair')

    def _get_color(self, name: str):
        if name.upper() in self.colors:
            color_number = self.colors[name.upper()]
            return color_number
        else:
            raise NameError(f'{name} is not a recognized color')

    def _set_pair(self, name: str, color: tuple = None):
        if color is not None:
            self._add_color(name, color)

        self._add_pair(name)

    def _add_pair(self, name: str):
        color_number = self._get_color(name)
        if name.upper() not in self.pairs:
            pair_number = len(self.pairs) + 1
            curses.init_pair(pair_number, color_number, curses.COLOR_BLACK)
            self.pairs.append(name.upper())

    def _add_color(self, name: str, color: tuple):
        if not curses.can_change_color():
            raise NotImplemented('Your terminal does not support custom colors.')

        r, g, b = color
        color_number = len(self.colors) + 1
        curses.init_color(color_number, r, g, b)
        self.colors[name.upper()] = color_number


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


class Window:
    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        return self.stdscr

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def getch(self):
        return self.stdscr.getch()

    def refresh(self):
        self.stdscr.refresh()

    def clear(self):
        self.stdscr.clear()

    def addstr(self, y, x, string):
        self.stdscr.addstr(y, x, string)

    def addch(self, y, x, char):
        self.stdscr.addch(y, x, char)

    def getmaxyx(self):
        return self.stdscr.getmaxyx()

    def getbegyx(self):
        return self.stdscr.getbegyx()

    def getyx(self):
        return self.stdscr.getyx()

    def move(self, y, x):
        self.stdscr.move(y, x)



