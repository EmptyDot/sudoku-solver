import numpy as np
from itertools import permutations, filterfalse
from curses import wrapper
from draw import Grid
import time
from matplotlib import pyplot as plt


class MagicSquare(Grid):
    def __init__(self, stdscr=None, target_sum=0, sleep=0.0):
        self.grid = np.zeros((3, 3), dtype=int)
        super(MagicSquare, self).__init__(stdscr, sleep, self.grid)
        self.target_sum = target_sum
        self.zero_array = np.zeros(3, dtype=int)
        self.x = []
        self.y = []

    def run(self, stop):
        while self.target_sum <= stop:
            t0 = time.time()
            if self.solve():
                print(f'{self.target_sum} has a magic square:')
                print(self.grid)
            else:
                print(f'{self.target_sum} has no magic square.')
            t1 = time.time()
            delta = t1-t0
            print(f'Time delta: {delta}')
            self.x.append(self.target_sum)
            self.y.append(delta)
            plt.xlabel('Target sum')
            plt.ylabel('Time(seconds)')
            plt.plot(self.x, self.y)
            plt.show()

            self.reset_grid()
            self.target_sum += 1

    def reset_grid(self):
        self.grid = np.zeros((3, 3), dtype=int)

    def solve_start(self):
        """
        Solve the grid and show it. To be called inside main.
        """
        if self.solve():
            self.draw_grid(info=f'Found a magic square for sum: {self.target_sum}')
        else:
            self.clear()
            self.display_info(info=f'No valid magic square for sum: {self.target_sum}')
        self.stdscr.getch()

    def solve(self, n=None):
        for i in self.get_permutations(n):
            # print(i)
            if not n:
                # apply across row
                self.grid[0] = i
                if self.stdscr:
                    self.draw_grid()

                if self.solve(i[0]):
                    return True
            else:
                # apply across column
                self.grid[:, 0] = i
                if self.stdscr:
                    self.draw_grid()

                if self.fill_grid():
                    return True
                # reset for next iteration
                self.grid[1] = self.zero_array
                self.grid[2] = self.zero_array
                if self.stdscr:
                    self.draw_grid()
        self.reset_grid()
        return False

    def fill_grid(self):
        """
        called after self.grid[0, :] and self.grid[:, 0] is filled
        """
        # TODO this is ugly, rewrite it
        idxs = ((1, 1), (2, 2), (1, 2), (2, 1))
        axs = (np.flipud(self.grid).diagonal(),
               self.grid.diagonal(),
               (self.grid[1], self.grid[:, 2]),
               (self.grid[2], self.grid[:, 1]))
        order = zip(idxs, axs)
        for idx, ax in order:
            if type(ax) == tuple:
                n = self.compare(ax)
            else:
                n = self.get_missing(ax)
            if n > 0 and not self.in_grid(n):
                y, x = idx
                self.grid[y, x] = n
                if self.stdscr:
                    self.update(y, x, n)
            else:
                return False
        return True

    def compare(self, arrs):
        arr1, arr2 = arrs
        result = self.get_missing(arr1)
        if result == self.get_missing(arr2):
            return result
        return 0

    def get_missing(self, arr):
        return self.target_sum - sum(arr)

    def in_grid(self, n):
        for i in self.grid:
            if n in i:
                return True
        return False

    def get_permutations(self, n=0):
        yield from filterfalse(lambda arr: self.constraints(arr, n), permutations(range(1, self.target_sum-2), 3))

    def constraints(self, arr, n):
        if sum(arr) != self.target_sum:
            return True
        elif n:
            if arr[0] != n:
                return True
            if self.grid[0, 2] + arr[2] > self.target_sum:
                return True
            if arr in permutations(self.grid[0]):
                return True
        return False


def main(stdscr, target_sum, sleep=0.0):
    MagicSquare(stdscr, target_sum, sleep).solve_start()


if __name__ == "__main__":
    wrapper(main, target_sum=19, sleep=0.1)
    #m = MagicSquare(target_sum=15)
    #if m.solve():
        #print(m.grid)
    # m.run(100)


"""
O(n**2)
This method is not well suited for a brute force approach
Since the number of permutations to check is not easily reduced
This would be much better for a theoretical approach instead 
    or if some algorithm can reduce the possibility space to a more time-efficient size
"""