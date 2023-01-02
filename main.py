import solver
from drawing.terminal_pen import TerminalPen
from grid import Grid
from curses import wrapper
from drawing.window import Window
from typing import Optional
import numpy as np
from generator import Generator


def main(stdscr, values: Optional[np.ndarray] = None):
    """
    Main function for the program.
    :param stdscr: curses window
    :param values: numpy array that stores information about the grid, leave null to generate a new sudoku board

    """
    pen = TerminalPen(stdscr)

    if values is None:
        grid, pen = Generator().generate_grid(pen)
    else:
        grid = Grid(values)


    for y, x, n in solver.solve(grid):
        pen.put(grid, (y, x), n, "Solving...")
    pen.draw_grid(grid, "Done!")
    pen.getch()


if __name__ == '__main__':
    wrapper(main)