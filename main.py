import solver
from drawing.terminal_pen import TerminalPen
from grid import Grid
from curses import wrapper

def main(stdscr, grid: Optional[np.ndarray] = None, sleep: int | float = 0, difficulty: int = 0):
    """
    Main function for the program.

    :param grid: Grid object that stores information about the grid and the pen
    :param sleep: time to sleep between updates
    :param difficulty: difficulty of the grid: 0 = easy, 1 = medium, 2 = hard (default: 0)
    """
    grid = Grid()  # Optional generation here
    pen = TerminalPen(stdscr, grid)
    for y, x, n in solver.solve(grid):
        pen.put(y, x, n)

    pen.draw_grid()
    pen.getch()




def get_grid():
    if grid is None:
        grid = Grid(stdscr, sleep=sleep)
        gen = Generator(grid, difficulty)
        grid = gen.generate_grid()
    else:
        grid = Grid(stdscr, values=grid, sleep=sleep)


if __name__ == '__main__':
    wrapper(main, )