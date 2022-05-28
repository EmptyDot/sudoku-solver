from collections import deque
import numpy as np
from sudoku import Solver
import curses
from curses import wrapper
import random
import time
import copy


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
        self.current_possibility = []

    def set_possibilities(self):
        """
        Add all possible numbers (1-9) of (y, x) to the list in the corresponding position.
        """
        for y in range(9):
            for x in range(9):
                self.possibilities[y][x] = self.update_possibilities(y, x)

    def update_possibilities(self, y, x):

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
                    if self.possibilities[y][x][0] != self.grid[y][x]:
                        if smallest == 1:
                            positions.append((y, x))
                        else:
                            smallest = 1
                            positions = [(y, x)]

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
        """
        self.draw_grid('New iteration')
        y, x = self.get_min_entropy_coords()
        self.collapse_at(y, x)
        self.propagate(y, x)


    def collapse_at(self, y, x):
        """
        Choose a possible number and put it in
        """
        self.current_possibility = copy.deepcopy(self.possibilities[y][x])
        n = random.choice(self.possibilities[y][x])
        self.put(y, x, n, info=f'{y=}, {x=}, {self.possibilities[y][x]}')
        self.possibilities[y][x] = [n]

    def propagate(self, y, x):
        """
        Propagate the changes from a collapsed cell to the rest of the grid

        :param y:
        :param x:
        :return:
        """
        stack = [(y, x)]  # maybe use deque?
        while len(stack) > 0:
            cur_y, cur_x = stack.pop()
            # get neighbours of cur_coords if along base_coords row or column or in the same box
            for d in self.valid_dirs(cur_y, cur_x, y, x):

                other_y, other_x = tuple((cur_y, cur_x) + d)

                self.highlight(other_y, other_x, f'Look for {self.grid[y, x]} in {self.possibilities[other_y][other_x]}')
                # get possibilities list at neighbour cell
                other_possibilities = self.get_possibilities(other_y, other_x)  # might contain num
                # get an updated list of possibilities at neighbour cell
                valid_possibilities = self.update_possibilities(other_y, other_x)
                # compare possibilities
                for other_num in other_possibilities:
                    if other_num not in valid_possibilities:
                        self.constrain(other_y, other_x, other_num)
                        if not self.check_if_valid(other_y, other_x):
                            return False
                        # if the resulting list has length of 0 this means the collapsed cell can not be solved
                        # and we need to backtrack to the point before the cell is collapsed and try a different cell.
                        # if a cell is modified: add it to the stack
                        if (other_y, other_x) not in stack:
                            stack.append((other_y, other_x))
        return True

    def check_if_valid(self, y, x):
        if len(self.possibilities[y][x]) == 0:
            return False
        return True

    def constrain(self, y, x, num):
        self.highlight(y, x, f'Constrain {num} in {self.possibilities[y][x]}')
        if num in self.possibilities[y][x]:
            self.possibilities[y][x].remove(num)

    def get_possibilities(self, y, x) -> list:
        return self.possibilities[y][x]

    @staticmethod
    def valid_dirs(cy, cx, by, bx):
        UP = np.array((-1, 0))
        LEFT = np.array((0, -1))
        DOWN = np.array((1, 0))
        RIGHT = np.array((0, 1))
        UP_LEFT = np.array((-1, -1))
        UP_RIGHT = np.array((-1, 1))
        DOWN_LEFT = np.array((1, -1))
        DOWN_RIGHT = np.array((1, 1))

        valid_directions = []
        if cy == by:
            if cx < 8:
                valid_directions.append(RIGHT)
            if cx > 0:
                valid_directions.append(LEFT)
        if cx == bx:
            if cy < 8:
                valid_directions.append(DOWN)
            if cy > 0:
                valid_directions.append(UP)
        if cx // 3 == bx // 3 and cy // 3 == by // 3:
            if cx % 3 < 2:
                if cy % 3 < 2:
                    valid_directions.append(DOWN_RIGHT)
                if cy % 3 > 0:
                    valid_directions.append(UP_RIGHT)
            if cx % 3 > 0:
                if cy % 3 < 2:
                    valid_directions.append(DOWN_LEFT)
                if cy % 3 > 0:
                    valid_directions.append(UP_LEFT)

        return valid_directions


def main(stdscr):
    w = Wave(stdscr, sleep=1)
    w.solve()


if __name__ == '__main__':
    wrapper(main)