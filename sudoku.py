import numpy as np
import curses
from curses import wrapper
import random

ex_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
             [6, 0, 0, 1, 9, 5, 0, 0, 0],
             [0, 9, 8, 0, 0, 0, 0, 6, 0],
             [8, 0, 0, 0, 6, 0, 0, 0, 3],
             [4, 0, 0, 8, 0, 3, 0, 0, 1],
             [7, 0, 0, 0, 2, 0, 0, 0, 6],
             [0, 6, 0, 0, 0, 0, 2, 8, 0],
             [0, 0, 0, 4, 1, 9, 0, 0, 5],
             [0, 0, 0, 0, 8, 0, 0, 7, 9]]

class Solver:
    def __init__(self):
        self.grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                     [6, 0, 0, 1, 9, 5, 0, 0, 0],
                     [0, 9, 8, 0, 0, 0, 0, 6, 0],
                     [8, 0, 0, 0, 6, 0, 0, 0, 3],
                     [4, 0, 0, 8, 0, 3, 0, 0, 1],
                     [7, 0, 0, 0, 2, 0, 0, 0, 6],
                     [0, 6, 0, 0, 0, 0, 2, 8, 0],
                     [0, 0, 0, 4, 1, 9, 0, 0, 5],
                     [0, 0, 0, 0, 8, 0, 0, 7, 9]]

        self.solutions = 0

    def reset_grid(self):
        self.grid = [list(np.zeros(9, dtype=int)) for _ in range(9)]

    def show_solve(self, y, x, n, stdscr):
        stdscr.clear()
        RED = curses.color_pair(1)
        WHITE = curses.color_pair(2)

        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if i == y and j == x:
                    stdscr.addstr(y, x*2, str(n), RED)
                else:
                    stdscr.addstr(i, j*2, str(self.grid[i][j]), WHITE)

        stdscr.refresh()

    def show_solution(self):
        self.solve(show=True)
        print('no more solutions')

    def possible(self, y, x, n):
        for i in range(9):
            if self.grid[y][i] == n:
                return False
        for i in range(9):
            if self.grid[i][x] == n:
                return False
        x0 = (x//3) * 3
        y0 = (y//3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[y0+i][x0+j] == n:
                    return False
        return True

    def solve(self, stdscr=None, show=False):
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.possible(y, x, n):
                            if stdscr is not None:
                                self.grid[y][x] = n
                                self.show_solve(y, x, n, stdscr)
                                self.solve(stdscr=stdscr)
                                self.grid[y][x] = 0
                                self.show_solve(y, x, n, stdscr)
                            else:
                                self.grid[y][x] = n
                                self.solve(show=show)
                                self.grid[y][x] = 0
                    return
        if show:
            print(np.matrix(self.grid))
            input('more?')
        else:
            # self.solutions += 1
            return True

    def find_empty(self):  # finds the first empty space in the board, which is represented by a 0
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    return y, x
        return False


    def generate_grid(self):
        pass

    def check_grid(self):
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    return False
        return True

    def generate_random_grid(self):
        self.reset_grid()

        lst = list(range(1, 10))
        for y in range(3):
            for x in range(3):
                n = random.choice(lst)
                self.grid[y][x] = n
                lst.remove(n)

        lst = list(range(1, 10))
        for y in range(3, 6):
            for x in range(3, 6):
                n = random.choice(lst)
                self.grid[y][x] = n
                lst.remove(n)

        lst = list(range(1, 10))
        for y in range(6, 9):
            for x in range(6, 9):
                n = random.choice(lst)
                self.grid[y][x] = n
                lst.remove(n)

        return self.fill_grid()

    def fill_grid(self):  # uses recursion to finish generating a random board
        print(np.matrix(self.grid))
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    n = random.randint(1, 9)

                    if self.possible(y, x, n):
                        self.grid[y][x] = n

                        if self.solve():
                            self.fill_grid()
                            return self.grid

                        self.grid[y][x] = 0
        return False

    def remove_number(self):
        while True:
            y = random.randrange(9)
            x = random.randrange(9)
            n = self.grid[y][x]
            if n != 0:
                break

        self.grid[y][x] = 0
        self.solve()
        if self.solutions == 0:
            self.grid[y][x] = n
        elif self.solutions > 1:
            self.remove_number()
        return





def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.clear()
    Solver().solve(stdscr)
    stdscr.getch()

# to show the solve:
# uncomment the line below and run in terminal
# wrapper(main)

# or to only show solution run:
# Solver().show_solution()

"""Sudoku Generator"""
Solver().generate_random_grid()









