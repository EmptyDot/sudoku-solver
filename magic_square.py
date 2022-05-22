import numpy as np
import math
from itertools import permutations, filterfalse
import time
from matplotlib import pyplot as plt


class MagicSquare:
    def __init__(self, target_sum=0):
        self.grid = np.zeros((3, 3), dtype=int)
        self.target_sum = target_sum
        self.zero_array = np.zeros(3, dtype=int)

    def run(self, stop):
        dt = []
        while self.target_sum <= stop:
            t0 = time.time()
            if self.solve():
                print(f'Found a magic square for sum: {self.target_sum}')
                print(self.grid)
                break
            t1 = time.time()
            delta = t1-t0
            dt.append(delta)

            print(f'No valid magic square for sum: {self.target_sum}')
            self.target_sum += 1

        plt.xlabel('Target sum')
        plt.ylabel('Time(seconds)')
        plt.scatter(range(self.target_sum), dt)
        plt.show()

    def reset_grid(self):
        self.grid = np.zeros((3, 3), dtype=int)

    def solve(self, n=None):
        for i in self.get_permutations(n):
            # print(i)
            if not n:
                # apply across row
                self.grid[0] = i
                if self.solve(i[0]):
                    return True
            else:
                # apply across column
                self.grid[:, 0] = i
                if self.fill_grid():
                    return True
                # reset for next iteration
                self.grid[1] = self.zero_array
                self.grid[2] = self.zero_array
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


class ParkerSquare(MagicSquare):
    def __init__(self, target_sum=0):
        super(ParkerSquare, self).__init__(target_sum)

    @staticmethod
    def square_arr(arr):
        return tuple(map(lambda x: x**2, arr))

    @staticmethod
    def check_if_square(n):
        if n > 0:
            if int(math.sqrt(n) + 0.5) ** 2 == n:
                return True
        return False

    def get_missing(self, arr):
        num = self.target_sum - sum(arr)
        return num if self.check_if_square(num) else 0

    def get_permutations(self, n=0):
        yield from filterfalse(lambda arr: self.constraints(arr, n),
                               permutations(range(1, math.ceil((math.sqrt(self.target_sum)))), 3))

    def constraints(self, arr, n):
        if sum(self.square_arr(arr)) != self.target_sum:
            return True
        elif n:
            if arr[0] != n:
                return True
            if self.grid[0, 2] + arr[2] > self.target_sum:
                return True
            if arr in permutations(self.grid[0]):
                return True
        return False


if __name__ == "__main__":
    p = ParkerSquare()
    p.run(10000)

"""
O(n**2)
This method is not well suited for a brute force approach
Since the number of permutations to check is not easily reduced
This would be much better for a theoretical approach instead 
    or if some algorithm can reduce the possibility space to a more time-efficient size
    
for any target_sum (t) >= 15:
you can construct any square S(t+3n) by taking S(t) and adding:
    [[0, +2n, +n]
     [+2n, +n, 0]
     [+n, 0, +2n]] 
     or any of its permutations
     
for the case of the parker square, where all elements are square numbers (int(a)**2) 
     its absolutely impossible to construct a parker square P(t) of side length 3 where t < 9**2 since we would be 
        unable to fill the grid.
checked numbers:
    0-3141

"""