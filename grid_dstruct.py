from abc import ABC, abstractmethod
import numpy as np
from drawing.terminal_pen import TerminalPen


class Grid(ABC):
    def __init__(self):
        self.grid = np.zeros((9, 9), dtype=int)
        self.pen = TerminalPen()

