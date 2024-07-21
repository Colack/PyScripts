#!/usr/bin/env python3

import os
import time
import shutil

def initialize_grid(rows, cols):
    from random import randint
    grid = [[randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    return grid

def print_grid(grid):
    for row in grid:
        print(' '.join(['█' if cell else ' ' for cell in row]))
    print('\n' * 2)

def count_neighbors(grid, row, col):
    rows, cols = len(grid), len(grid[0])
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if 0 <= r < rows and 0 <= c < cols:
                count += grid[r][c]
    return count

def next_generation(grid):
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = count_neighbors(grid, r, c)
            if grid[r][c] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[r][c] = 0
                else:
                    new_grid[r][c] = 1
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1
    return new_grid

def get_terminal_size():
    size = shutil.get_terminal_size((80, 20))
    return size.lines - 2, size.columns - 2

def main():
    rows, cols = get_terminal_size()
    grid = initialize_grid(rows, cols)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_grid(grid)
        grid = next_generation(grid)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
