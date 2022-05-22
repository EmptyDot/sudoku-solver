from collections import deque
import numpy as np
from sudoku import Solver
import curses
from curses import wrapper
import random
import time

ex_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
           [6, 0, 0, 1, 9, 5, 0, 0, 0],
           [0, 9, 8, 0, 0, 0, 0, 6, 0],
           [8, 0, 0, 0, 6, 0, 0, 0, 3],
           [4, 0, 0, 8, 0, 3, 0, 0, 1],
           [7, 0, 0, 0, 2, 0, 0, 0, 6],
           [0, 6, 0, 0, 0, 0, 2, 8, 0],
           [0, 0, 0, 4, 1, 9, 0, 0, 5],
           [0, 0, 0, 0, 8, 0, 0, 0, 0]]



class Wave(Solver):
    def __init__(self, stdscr, sleep):
        self.stdscr = stdscr
        super(Wave, self).__init__(stdscr=stdscr, grid=np.array(ex_grid), sleep=sleep)
        self.possibilities = [[[] for _ in range(9)] for _ in range(9)]

    def set_possibilities(self):
        """
        Add all possible numbers of (y, x) to the list in the corresponding position.
        """
        for y in range(9):
            for x in range(9):
                self.possibilities[y][x] = self.update_possibilities((y, x))

    def update_possibilities(self, coords):
        y, x = coords
        possible = []
        if self.grid[y][x] == 0:
            for n in range(1, 10):
                if self.possible(y, x, n, self.grid):
                    possible.append(n)
        else:
            return [self.grid[y][x]]
        return possible

    def solve(self):
        """
        Main method: call starts here
        :return:
        """
        self.set_possibilities()
        while not self.is_filled():
            self.iterate()
        print('DONE!')
        print(self.grid)

    def get_min_entropy_coords(self):
        """
        Find the cell with the lowest number of possibilities. In case of a tie: choose randomly between them.
        :return Lowest entropy coordinates (y, x)
        """
        smallest = 9
        positions = []
        for y in range(9):
            for x in range(9):
                # print(f'{y=}, {x=}, {self.possibilities[y][x]}')
                if len(self.possibilities[y][x]) == 1:
                    """
                    n = self.possibilities[y][x][0]
                    if self.grid[y][x] != n:
                        self.put(y, x, n)
                    """
                    continue
                elif len(self.possibilities[y][x]) < smallest:
                    positions = [(y, x)]
                    smallest = len(self.possibilities[y][x])
                elif len(self.possibilities[y][x]) == smallest:
                    positions.append((y, x))
        if len(positions) != 0:
            return random.choice(positions)
        else:
            print('GRID SHOULD BE FILLED')

    def iterate(self):
        """
        Gets called once per iteration. Collapses a cell and propagates the possibility to all affected cells.
        :return:
        """
        self.draw_grid('New iteration')
        coords = self.get_min_entropy_coords()
        self.collapse_at(coords)
        self.propagate(coords)

    def collapse_at(self, coords):
        """
        Choose a possible number and put it in
        :param coords:
        :return:
        """
        y, x = coords
        try:
            n = random.choice(self.possibilities[y][x])
        except IndexError as exc:
            self.clear()
            curses.endwin()
            time.sleep(1)
            print(self.grid)

            raise exc
        self.put(y, x, n, info=f'{y=}, {x=}, {self.possibilities[y][x]}')
        self.possibilities[y][x] = [n]

    def propagate(self, coords):
        """
        :param coords: y, x coordinates of a collapsed cell.
        :return:
        """
        stack = [coords]  # maybe use deque?
        while len(stack) > 0:
            cur_coords = stack.pop()
            # get neighbours of cur_coords if along base_coords row or column or in the same box
            for d in self.valid_dirs(cur_coords, coords):

                other_coords = tuple(cur_coords + d)
                # get possibilities list at neighbour cell
                other_possibilities = self.get_possibilities(other_coords)  # might contain num
                # get an updated list of possibilities at neighbour cell
                valid_possibilities = self.update_possibilities(other_coords)
                # check if num in neighbour, if so: remove it from neighbour and add it to the stack
                for other_num in other_possibilities:
                    if other_num not in valid_possibilities:
                        self.constrain(other_coords, other_num)
                        # if the resulting list has length of 0 this means the collapsed cell can not be solved
                        # and we need to backtrack to the point before the cell is collapsed and try a different cell.
                        # if a cell is modified: add it to the stack
                        if other_coords not in stack:
                            stack.append(other_coords)







    def constrain(self, coords, num):
        y, x = coords
        self.highlight(y, x, f'{num=}, {self.possibilities[y][x]}')
        if num in self.possibilities[y][x]:
            self.possibilities[y][x].remove(num)
        

    def get_possibilities(self, coords) -> list:
        y, x = coords
        return self.possibilities[y][x]


    @staticmethod
    def valid_dirs(coords, base_coords):
        UP = np.array((-1, 0))
        LEFT = np.array((0, -1))
        DOWN = np.array((1, 0))
        RIGHT = np.array((0, 1))
        UP_LEFT = np.array((-1, -1))
        UP_RIGHT = np.array((-1, 1))
        DOWN_LEFT = np.array((1, -1))
        DOWN_RIGHT = np.array((1, 1))

        y, x = coords
        by, bx = base_coords

        valid_directions = []
        if y == by:
            if x < 8:
                valid_directions.append(RIGHT)
            if x > 0:
                valid_directions.append(LEFT)
        if x == bx:
            if y < 8:
                valid_directions.append(DOWN)
            if y > 0:
                valid_directions.append(UP)
        if x // 3 == bx // 3 and y // 3 == by // 3:
            if x % 3 < 2:
                if y % 3 < 2:
                    valid_directions.append(DOWN_RIGHT)
                if y % 3 > 0:
                    valid_directions.append(UP_RIGHT)
            if x % 3 > 0:
                if y % 3 < 2:
                    valid_directions.append(DOWN_LEFT)
                if y % 3 > 0:
                    valid_directions.append(UP_LEFT)

        return valid_directions


def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.clear()
    w = Wave(stdscr, sleep=1)
    w.solve()



if __name__ == '__main__':
    wrapper(main)