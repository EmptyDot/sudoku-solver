import curses
from dataclasses import dataclass
from aliases import RGBColor


@dataclass
class ColorPair:
    name: str
    number: int
    text_color: int
    background_color: int


# TODO add check for can change color
#         if not curses.can_change_color():

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
        self.pairs: list[ColorPair] = []  # initialized pairs, pair_number = self.pairs.index(name) + 1

    def color(self, name: str, color: tuple = None):
        """
        Init a new color pair if not already initialized. Call structure: RED = self.color('RED').

        :param name: String Literal: "BLACK", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "WHITE", "YELLOW"
            or any custom color names.
        :param color: Tuple: (r, g, b) values each spanning 0-1000. Only required when defining new colors.
        """
        if name.upper() in self.pairs:
            pair = self._get_pair(name)
        else:
            # name not in self.pairs
            # set a new pair with the specified color
            self._set_pair(name, color)
            pair = self._get_pair(name)

        return pair

    def _get_pair(self, name: str):
        for i, pair in enumerate(self.pairs):
            if pair.name == name:
                return curses.color_pair(i)
        raise ValueError(f"Value: {name} not found!")

        # pair_number = self.pairs.index(name.upper()) + 1

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
            pair_number = len(self.pairs)
            # TODO add ability to specify background color
            curses.init_pair(pair_number, color_number, curses.COLOR_BLACK)
            pair = ColorPair(name.upper(), pair_number, color_number, curses.COLOR_BLACK)
            self.pairs.append(pair)

    def _add_color(self, name: str, color: RGBColor):

        r, g, b = color
        # outside the bounds of self.colors
        color_number = len(self.colors)
        curses.init_color(color_number, r, g, b)
        self.colors[name.upper()] = color_number
