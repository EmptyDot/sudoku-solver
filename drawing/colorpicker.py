import curses
from aliases import RGBColor
from typing import Optional
from pairs_dstruct import ColorPair, ColorPairs
from colors_dstruct import Color, Colors



# TODO add check for can change color
#         if not curses.can_change_color():


class ColorPicker:
    def __init__(self):
        self.colors = Colors()
        self.pairs = ColorPairs()

    def color(self, pair_name: str, color1: Optional[RGBColor], color2: Optional[RGBColor]) -> int:
        """
        Init a new color pair if not already initialized. Call structure: RED = self.color('RED').

        :param pair_name: String Literal: "BLACK", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "WHITE", "YELLOW"
            or any custom color names.
        :param color: Tuple: (r, g, b) values each spanning 0-1000. Only required when defining new colors.
        """

        if pair_name.upper() in self.pairs:
            return self.pairs.get_color_pair(pair_name)
        else:
            # name not in self.pairs
            raise ValueError(f"{pair_name} not found. Call add_color().")

    def add_pair(self, pair_name: str, color1: RGBColor, color2: Optional[RGBColor]):
        if color1 not in self.colors:
            self._add_color()
        if foreground_color in self.colors:
            if background_color:
                if background_color in self.colors:
                    self._set_pair(pair_name, foreground_color, background_color)
            else:
                self._set_pair(pair_name, foreground_color, curses.COLOR_BLACK)
        else:

        self._get_pair(pair_name)

    def _get_pair(self, pair_name: str) -> int:
        """
          for i, pair in enumerate(self.pairs):
              if pair.pair_name == name:
                  return curses.color_pair(i)
          """
        return curses.color_pair(self.pairs[pair_name].pair_number)



        # pair_number = self.pairs.index(name.upper()) + 1

    def _get_color(self, color_name: str) -> int:
        if color_name.upper() in self.colors:
            color_number = self.colors[color_name.upper()]
            return color_number
        else:
            raise NameError(f'{color_name} is not a recognized color')

    def _set_pair(self, name: str, foreground_color: RGBColor, background_color: Optional[RGBColor]):
        if name in self.pairs:


    def _add_pair(self, pair_name: str):
        if pair_name.upper() in self.pairs:
            color_number = self.colors[pair_name]


        else:
            pair_number = len(self.pairs)
            # TODO add ability to specify background color
            pair = ColorPair(pair_name.upper(), pair_number, color_number, curses.COLOR_BLACK)
            self.pairs.append(pair)

    def _add_color(self, name: str, color: RGBColor):

        r, g, b = color
        # outside the bounds of self.colors
        color_number = len(self.colors)
        curses.init_color(color_number, r, g, b)
        self.colors[name.upper()] = color_number
