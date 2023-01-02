from dataclasses import dataclass
import curses



@dataclass
class ColorPair:
    pair_name: str
    pair_number: int
    foreground_color: int
    background_color: int

    def __post_init__(self):
        curses.init_pair(self.pair_number, self.foreground_color, self.background_color)


class ColorPairs:
    def __init__(self):
        self._pairs: list[ColorPair] = []

    def next_free_pair_number(self) -> int:
        pair_numbers = [pair.pair_number for pair in self._pairs]
        for i in range(max(pair_numbers) + 1):
            if i not in pair_numbers:
                return i

    def get_color_pair(self, name) -> int:
        for pair in self._pairs:
            if name == pair.pair_name:
                return pair.pair_number
        raise ValueError(f"{name} not found!")

    def add_color_pair(self, name: str, foreground_color_number: int, background_color_number: int):
        pair_number = self.next_free_pair_number()
        pair = ColorPair(name, pair_number, foreground_color_number, background_color_number)
        curses.init_pair(pair_number, foreground_color_number, background_color_number)
        self._pairs.append(pair)

    def __contains__(self, name: str) -> bool:
        return any(pair.pair_name == name for pair in self._pairs)
