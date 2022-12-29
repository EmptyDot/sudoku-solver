from grid import Grid


def solve(grid: Grid) -> Grid:
    """
    Solve grid
    """
    for y in range(9):
        for x in range(9):
            if grid[y, x] == 0:
                for n in range(1, 10):
                    if grid.possible(y, x, n):
                        grid[y, x] = n
                        yield y, x, n
                        solve(grid)
                        if grid.is_filled():
                            return grid
                        yield y, x, 0
                return grid
    return grid
