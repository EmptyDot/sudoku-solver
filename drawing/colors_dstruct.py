import curses
from dataclasses import dataclass
from aliases import RGBColor

@dataclass
class Color:
    color_name: str
    color_number: int
    rgb_values: RGBColor


class Colors:
    def __init__(self):
        self._colors = {
            "BLACK": curses.COLOR_BLACK,
            "BLUE": curses.COLOR_BLUE,
            "CYAN": curses.COLOR_CYAN,
            "GREEN": curses.COLOR_GREEN,
            "MAGENTA": curses.COLOR_MAGENTA,
            "RED": curses.COLOR_RED,
            "WHITE": curses.COLOR_WHITE,
            "YELLOW": curses.COLOR_YELLOW
        }

    def __getitem__(self, name: str) -> int:
        for color_name, color_number in self._colors.items():
            if name == color_name:
                return color_number
        raise KeyError(f"{name} not found!")

    def __setitem__(self, color_name, color_number):
        self._colors[color_name] = color_number

    def __contains__(self, item):
        return item in self._colors

    def next_free_color_number(self):
        for i in range(max(self._colors.values()) + 1):
            if i not in self._colors.values():
                return i
