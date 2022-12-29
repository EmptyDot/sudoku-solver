



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
